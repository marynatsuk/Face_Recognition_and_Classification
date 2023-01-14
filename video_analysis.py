import cv2
import numpy as np
from datetime import datetime
from keras.models import load_model

from trained_models.wide_resnet import WideResNet
from results_analyser import ResultsAnalysis
from db_manager import DBManager

db_man = DBManager()
res_analysis = ResultsAnalysis()


class VideoAnalysis:
    def get_labels(self, dataset_name):
        if dataset_name == 'emotions':
            return {0: 'Angry', 1: 'Disgusted', 2: 'Scared', 3: 'Happy',
                    4: 'Sad', 5: 'Surprised', 6: 'Neutral'}
        elif dataset_name == 'gender':
            return {0: 'Female', 1: 'Male'}
        else:
            raise Exception('Invalid dataset name')

    def apply_offsets(self, face_coordinates, offsets):
        x, y, width, height = face_coordinates
        x_off, y_off = offsets
        return x - x_off, x + width + x_off, y - y_off, y + height + y_off

    def draw_text(self, coordinates, image_array, text, color, x_offset=0, y_offset=0,
                  font_scale=2, thickness=2):
        x, y = coordinates[:2]
        cv2.putText(image_array, text, (x + x_offset, y + y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, color, thickness, cv2.LINE_AA)

    def preprocess_input(self, x, v2=True):
        x = x.astype('float32')
        x = x / 255.0
        if v2:
            x = x - 0.5
            x = x * 2.0
        return x

    def start_analysing(self, video_path):
        video_capture = cv2.VideoCapture(video_path)
        # find id of video based on path
        video_id = db_man.get_video_id_from_path(video_path)
        if video_id is not None:
            print(video_id)

            model_folder_path = 'C:/Users/serg/PycharmProjects/cpe_desktop_coursework/trained_models/'
            result_crop_photo_f = 'C:/Users/serg/PycharmProjects/cpe_desktop_coursework/results_crop/'
            result_full_f = 'C:/Users/serg/PycharmProjects/cpe_desktop_coursework/results_full/'
            detection_model_path = model_folder_path + 'haarcascade_frontalface_default.xml'
            emotion_model_path = model_folder_path + 'emotion_model.hdf5'
            weights_file = model_folder_path + 'weights.28-3.73.hdf5'
            emotion_labels = self.get_labels('emotions')
            gender_labels = self.get_labels('gender')
            emotion_offsets = (20, 40)

            face_detection = cv2.CascadeClassifier(detection_model_path)
            emotion_classifier = load_model(emotion_model_path, compile=False)
            emotion_target_size = emotion_classifier.input_shape[1:3]
            model = WideResNet(64, depth=16, k=8)()
            model.load_weights(weights_file)

            cv2.namedWindow('window_frame')

            process_this_frame = True
            while True:
                if process_this_frame:
                    image = video_capture.read()[1]
                    try:
                        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        gray_image = np.squeeze(gray_image)
                        gray_image = gray_image.astype('uint8')
                    except cv2.error:
                        continue

                    faces = face_detection.detectMultiScale(gray_image, 1.3, 5)
                    for face_coordinates in faces:
                        x1, x2, y1, y2 = self.apply_offsets(face_coordinates, emotion_offsets)
                        x, y, w, h = face_coordinates
                        gray_face = gray_image[y1:y2 + 1, x1:x2 + 1]
                        try:
                            gray_face = cv2.resize(gray_face, emotion_target_size)
                        except cv2.error:
                            continue

                        margin = 0.4
                        img_h, img_w, _ = np.shape(rgb_image)
                        xw1 = max(int(x1 - margin * w), 0)
                        yw1 = max(int(y1 - margin * h), 0)
                        xw2 = min(int(x2 + margin * w), img_w - 1)
                        yw2 = min(int(y2 + margin * h), img_h - 1)
                        img_h, img_w, _ = np.shape(rgb_image)
                        rgb_face = rgb_image[yw1:yw2, xw1:xw2, :]
                        faces = np.empty((1, 64, 64, 3))
                        faces[0, :, :, :] = cv2.resize(rgb_face, (64, 64))

                        # emotion classification
                        gray_face = self.preprocess_input(gray_face, True)
                        gray_face = np.expand_dims(gray_face, 0)
                        emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
                        # age and gender classification
                        age_gender_pred = model.predict(faces)
                        predicted_gender = age_gender_pred[0]
                        ages = np.arange(0, 101).reshape(101, 1)
                        predicted_age = age_gender_pred[1].dot(ages).flatten()

                        gender = 0 if predicted_gender[0][0] > 0.4 else 1
                        gender = gender_labels[gender]
                        age = int(predicted_age[0])
                        emotion = emotion_labels[emotion_label_arg]
                        datetime_now = datetime.now()
                        timestamp = datetime_now.timestamp()
                        cv2.rectangle(rgb_image, (x, y), (x + w, y + h), 2)

                        crop_img = rgb_image[y:y + h, x:x + w]
                        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)

                        label = "{}, {}, {}".format(age, gender, emotion)

                        fullname = str(str(gender.lower()) + '_' + str(age) + '_' + str(emotion.lower()) + '_' + str(
                            int(timestamp)) + '.jpg')
                        print(fullname)
                        fullname_4_crop = str(
                            str(gender.lower()) + '_' + str(age) + '_' + str(emotion.lower()) + '_' + str(
                                int(timestamp)) + '_cr.jpg')

                        db_man.add_entry_results(video_id, gender, age, emotion, fullname_4_crop)

                        color = (255, 0, 0)
                        self.draw_text(face_coordinates, rgb_image, label, color, 0, -20, 1, 2)
                        cv2.rectangle(rgb_image, (x, y), (x + w, y + h), color, 2)

                        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                        cv2.imwrite(result_crop_photo_f + fullname_4_crop, crop_img)
                        cv2.imwrite(result_full_f + fullname, bgr_image)
                        cv2.imshow('window_frame', bgr_image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        video_capture.release()
                        res_analysis.analyse_results(video_id)
                        cv2.destroyAllWindows()

                process_this_frame = not process_this_frame

    def repeat_analysis(self, video_id):
        video_path = db_man.get_path_from_video_id(video_id)
        print(video_path)
        db_man.clear_results(video_id)
        self.start_analysing(video_path)

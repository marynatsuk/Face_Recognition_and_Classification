from tkinter import messagebox
import cv2
from db_manager import DBManager
from yt_manager import YoutubeManager

yt_man = YoutubeManager()
db_man = DBManager()


class TableManager:

    # def __init__(self):
    #     self.tree = tree
    #     self.count = 0

    def deselect(self, tree):
        selected = tree.focus()
        tree.selection_remove(selected)

    def query_videos_database(self, tree):
        for record in tree.get_children():
            tree.delete(record)

        records = db_man.videos_for_tree()
        count = 0

        for record in records:
            if count % 2 == 0:
                tree.insert(parent='', index='end', iid=count, text='',
                            values=(record[0], record[1], record[2], record[3]))
            else:
                tree.insert(parent='', index='end', iid=count, text='',
                            values=(record[0], record[1], record[2], record[3]))
            count += 1

    def query_results_database(self, tree, video_id):
        for record in tree.get_children():
            tree.delete(record)

        records = db_man.results_for_tree(video_id)
        count = 0

        for record in records:
            if count % 2 == 0:
                tree.insert(parent='', index='end', iid=count, text='',
                            values=(record[0], record[1], record[2], record[3], record[4], record[5]))
            else:
                tree.insert(parent='', index='end', iid=count, text='',
                            values=(record[0], record[1], record[2], record[3], record[4], record[5]))
            count += 1

    def see_video_result(self, tree, video_id):
        try:
            video_path = db_man.get_path_from_video_id(video_id)
            cap = cv2.VideoCapture(video_path)

            if video_path == '':
                messagebox.showerror('showerror', 'Empty address. Try again')
            elif not cap.isOpened():
                messagebox.showinfo('showinfo', 'Downloading video. Wait a minute!')
                video_link = db_man.get_link_from_id(video_id)
                yt_man.download_video(video_link)
                self.see_video_result(tree, video_id)
            else:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        cv2.imshow('Frame', frame)
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                    else:
                        break
                cap.release()
        except IndexError:
            messagebox.showerror('showerror', 'Choose an entry')
        except cv2.error:
            messagebox.showerror('showerror', 'OpenCV error')

        self.deselect(tree)

    def remove_one(self, tree, video_id):
        try:
            x = tree.selection()[0]
            tree.delete(x)
            db_man.delete_entry(video_id)
            self.deselect(tree)
            messagebox.showinfo('showinfo', 'Record successfully deleted')
        except IndexError:
            self.deselect(tree)
            messagebox.showerror('showerror', 'Choose an entry')

    def view_photo(self, tree):
        try:
            folder_path = 'C:/Users/serg/PycharmProjects/cpe_desktop_coursework/results_crop/'
            selected = tree.focus()
            values = tree.item(selected, 'values')
            img_path = folder_path + values[5]

            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if values[5] == '':
                messagebox.showerror('showerror', 'Empty address. Try again')
            elif img is None:
                messagebox.showerror('showerror', 'Could not file photo')
            else:
                scale_percent = 50
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
                dim = (width, height)

                name = values[5]
                resized_img = cv2.resize(img, dim)
                cv2.imshow(name, resized_img)
                cv2.waitKey(0)

        except IndexError:
            messagebox.showerror('showerror', 'Choose an entry')
        except cv2.error:
            messagebox.showerror('showerror', 'OpenCV error')
        self.deselect(tree)

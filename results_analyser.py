import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db_manager import DBManager

db_man = DBManager()


class ResultsAnalysis:
    def analyse_results(self, video_id):
        data = db_man.get_detailed_data(video_id)
        df = pd.DataFrame(data)
        video_id = int(video_id)
        df.columns = ['Result ID', 'Video ID', 'Gender', 'Age', 'Emotion', 'Path']
        df = df.drop('Video ID', axis=1)
        df = df.drop('Path', axis=1)

        stats_folder = 'C:/Users/serg/PycharmProjects/cpe_desktop_coursework/stats_folder/'
        gender = df['Gender'].value_counts()
        print('Gender occ. :\n', gender)
        sns.countplot(x='Gender', data=df)
        plt.title('Number of Male and Female occurrences')
        gender_path = str(video_id) + '_gender.png'
        plt.savefig(stats_folder + gender_path)
        plt.show()

        genders = ['Male', 'Female']
        g_counts = [0, 0]
        for i in range(len(genders)):
            if genders[i] not in df.values:
                g_counts[i] = 0
            else:
                g_counts[i] = df['Gender'].value_counts()[genders[i]]
            i += 1

        print(g_counts)
        male_count = int(g_counts[0])
        female_count = int(g_counts[1])


        emotion = df['Emotion'].value_counts()
        print('Emotion occ. :\n', emotion)
        sns.countplot(x='Emotion', data=df)
        plt.title('Number of each emotion occurrences')
        emotion_path = str(video_id) + '_emotion.png'
        plt.savefig(stats_folder + emotion_path)
        plt.show()

        emotions = ['Angry', 'Scared', 'Happy', 'Sad', 'Surprised', 'Neutral']
        counts = [0, 0, 0, 0, 0, 0]
        for i in range(len(emotions)):
            if emotions[i] not in df.values:
                counts[i] = 0
            else:
                counts[i] = df['Emotion'].value_counts()[emotions[i]]
            i += 1

        print(counts)
        angry_count = int(counts[0])
        scared_count = int(counts[1])
        happy_count = int(counts[2])
        sad_count = int(counts[3])
        surprised_count = int(counts[4])
        neutral_count = int(counts[5])

        age_mean = df['Age'].mean().item()
        print('Mean age:', age_mean)
        sns.countplot(x='Age', data=df)
        plt.title('Number of each age occurrences')
        age_count_path = str(video_id) + '_age_count.png'
        plt.savefig(stats_folder + age_count_path)
        plt.show()
        sns.boxplot(x='Age', data=df)
        plt.title('Age boxplot')
        age_box_path = str(video_id) + '_age_box.png'
        plt.savefig(stats_folder + age_box_path)
        plt.show()
        db_man.add_gen_data(video_id, male_count, female_count, angry_count, scared_count, happy_count,
                            sad_count, surprised_count, neutral_count, age_mean, gender_path, age_count_path,
                            age_box_path,
                            emotion_path)



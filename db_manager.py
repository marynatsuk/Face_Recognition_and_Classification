from tkinter import messagebox
import mysql.connector
import os


class DBManager:

    def check_video_ex(self, video_yt_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute('''SELECT * FROM videos WHERE video_yt_id = (%s) ''', [video_yt_id])
            video_id = cursor.fetchone()
            if video_id is not None:
                cursor.close()
                db.close()
                print('Already exists')
                return True
            else:
                print('New entry')
                return False
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def check_channel_ex(self, channel_yt_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute('''SELECT * FROM channels WHERE channel_yt_id = (%s) ''', [channel_yt_id])
            channel_id = cursor.fetchone()
            if channel_id is not None:
                channel_id = channel_id[0]
                cursor.close()
                db.close()
                print('Channel already exists')
                return channel_id
            else:
                print('New channel entry')
                return None
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def add_entry_channels(self, channel_yt_id, channel_name):
        try:
            channel_id = self.check_channel_ex(channel_yt_id)
            if channel_id is None:
                db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
                cursor = db.cursor(buffered=True)
                cursor.execute(''' INSERT INTO channels (channel_yt_id, channel_id) VALUES (%s,%s)''',
                               (channel_yt_id, channel_name))
                print('New channel added')
                db.commit()
                channel_id = self.check_channel_ex(channel_yt_id)
                cursor.close()
                db.close()
                return channel_id
            else:
                return channel_id
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def add_entry_videos(self, video_yt_id, video_name, channel_yt_id, channel_name, video_yt_link, video_path):
        try:
            channel_id = self.add_entry_channels(channel_yt_id, channel_name)
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute(''' INSERT INTO videos (video_yt_id, video_name, channel_id, video_yt_link, video_path)
                        VALUES (%s,%s, %s,%s,%s)''',
                           (video_yt_id, video_name, channel_id, video_yt_link, video_path))
            print('Value added')
            db.commit()
            cursor.close()
            db.close()
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def get_gen_res_data(self, video_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute('''SELECT * FROM final_results WHERE res_vid_id = (%s) ''', [video_id])
            data = cursor.fetchall()
            cursor.close()
            db.close()
            return data
        except IndexError:
            messagebox.showerror('showerror', 'Choose an entry')
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def get_detailed_data(self, video_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor()
            cursor.execute('''SELECT * FROM results WHERE video_id_fk = %s''', [video_id])
            data = cursor.fetchall()
            cursor.close()
            db.close()
            return data
        except IndexError:
            messagebox.showerror('showerror', 'Choose an entry')
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def add_gen_data(self, video_id, male_count, female_count, angry_count, scared_count, happy_count,
                     sad_count, surprised_count, neutral_count, age_mean, gender_path, age_count_path,
                     age_box_path, emotion_path):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor()
            cursor.execute(''' INSERT INTO final_results (res_vid_id, male_count, female_count, angry_count, scared_count, happy_count,
                        sad_count, surprised_count,	neutral_count,avg_age, gender_path,	age_count_path,	age_box_path, emotion_path)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                           (video_id, male_count, female_count, angry_count, scared_count, happy_count,
                            sad_count, surprised_count, neutral_count, age_mean, gender_path, age_count_path, age_box_path,
                            emotion_path))
            db.commit()
            cursor.close()
            db.close()
            print('General Data added to table')
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def videos_for_tree(self):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute(
                "SELECT video_id, video_name, channel_name, video_yt_link FROM videos INNER JOIN channels ON videos.channel_id = channels.channel_id")
            records = cursor.fetchall()
            cursor.close()
            db.close()
            return records
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def results_for_tree(self, video_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute("SELECT * FROM results WHERE video_id_fk = %s LIMIT 200", [video_id])
            records = cursor.fetchall()
            cursor.close()
            db.close()
            return records
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def get_path_from_video_id(self, video_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute(''' SELECT video_path FROM videos WHERE video_id = %s''', [video_id])
            video_path = cursor.fetchone()
            if video_path is not None:
                video_path = video_path[0]
            else:
                video_path = ''
            return video_path
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def get_video_id_from_path(self, video_path):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute('''SELECT video_id FROM videos WHERE video_path = (%s) ''', [video_path])
            video_id = cursor.fetchone()
            video_id = video_id[0]
            print('Analysing video with ID:' + str(video_id))
            cursor.close()
            db.close()
            return video_id
        except mysql.connector.Error:
            print('MySql.Connector.Error')
            return None

    def delete_entry(self, video_id):
        video_path = self.get_path_from_video_id(video_id)
        try:
            os.remove(video_path)
            print('Deleted file')
        except FileNotFoundError:
            print('File was not found')

        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor(buffered=True)
            cursor.execute("DELETE from videos WHERE video_id = %s", [video_id])
            db.commit()
            db.close()
            print('Entry successfully deleted.')
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def add_entry_results(self, video_id, gender, age, emotion, fullname_4_crop):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor()
            cursor.execute(
                '''INSERT INTO results (video_id_fk, res_gender, res_age, res_emotion, res_address) VALUES (%s, %s, %s, %s, %s)''',
                (video_id, gender, age, emotion, fullname_4_crop))
            db.commit()
            cursor.close()
            db.close()
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def clear_results(self, video_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor()
            cursor.execute('''DELETE FROM results WHERE video_id_fk = %s''', [video_id])
            db.commit()
            cursor.execute('''DELETE FROM final_results WHERE res_vid_id = %s''', [video_id])
            db.commit()
            cursor.close()
            db.close()
        except mysql.connector.Error:
            print('MySql.Connector.Error')

    def get_link_from_id(self, video_id):
        try:
            db = mysql.connector.connect(host='localhost', user='root', password='', db='cpe_coursework')
            cursor = db.cursor()
            cursor.execute(
                '''SELECT video_yt_link FROM videos WHERE video_id = %s''', [video_id])
            video_link = cursor.fetchone()[0]
            cursor.close()
            db.close()
            return video_link
        except mysql.connector.Error:
            print('MySql.Connector.Error')

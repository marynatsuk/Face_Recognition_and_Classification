import tkinter
from tkinter import ttk, messagebox
from tkinter import *
import mysql.connector

from yt_manager import YoutubeManager
from db_manager import DBManager
from video_analysis import VideoAnalysis
from table_manager import TableManager
from PIL import Image, ImageTk


class WindowsManager:

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

    def youtube_window(self, root, frame):
        frame.grid_forget()
        youtube_window_frame = Frame(root)
        youtube_window_frame.grid(row=0, column=0)

        yt_label = Label(youtube_window_frame, text='Enter Youtube link', font=("Arial", 12))
        yt_label.grid(row=0, column=0)
        yt_entry = Entry(youtube_window_frame, width=105, font=("Arial", 12))
        yt_entry.grid(row=1, column=0, padx=10, pady=10)
        analyse_button = Button(youtube_window_frame, text="Analyse video",
                                command=lambda: yt_man.parse_yt_data(yt_entry), font=("Arial", 12))
        analyse_button.grid(row=2, column=0, padx=10, pady=10)

        done_button = Button(youtube_window_frame, text="To my videos",
                             command=lambda: self.my_videos(root, youtube_window_frame), font=("Arial", 12))
        done_button.grid(row=3, column=0, padx=10, pady=10)

        return youtube_window_frame

    def my_videos(self, root, frame):
        frame.grid_forget()
        my_videos_frame = Frame(root)
        my_videos_frame.grid(row=0, column=0)

        style = ttk.Style()
        style.configure("Treeview", background="#D3D3D3", foreground="black",
                        rowheight=25, fieldbackground="#D3D3D3")
        tree_frame = Frame(my_videos_frame)
        tree_frame.pack(pady=25, padx=25)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        res_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
        res_tree.pack()
        tree_scroll.config(command=res_tree.yview)

        res_tree['columns'] = ("ID", "Video Name", "Channel Name", 'Youtube Link')

        # Format Our Columns
        res_tree.column("#0", width=0, stretch=NO)
        res_tree.column("ID", anchor=CENTER, width=50)
        res_tree.column("Video Name", anchor=CENTER, width=300)
        res_tree.column("Channel Name", anchor=CENTER, width=250)
        res_tree.column("Youtube Link", anchor=CENTER, width=350)

        # Create Headings
        res_tree.heading("#0", text="", anchor=W)
        res_tree.heading("ID", text="ID", anchor=CENTER)
        res_tree.heading("Video Name", text="Video Name", anchor=CENTER)
        res_tree.heading("Channel Name", text="Channel Name", anchor=CENTER)
        res_tree.heading("Youtube Link", text="Youtube Link", anchor=CENTER)

        def select_record(self):
            try:
                selected = res_tree.focus()
                values = res_tree.item(selected, 'values')
                watch_button['state'] = tkinter.NORMAL
                delete_button['state'] = tkinter.NORMAL
                gen_res_button['state'] = tkinter.NORMAL
                det_res_button['state'] = tkinter.NORMAL
                analyse_ag_btn['state'] = tkinter.NORMAL
                return values[0]

            except IndexError:
                messagebox.showerror('showerror', 'Choose an entry')
            except mysql.connector.Error:
                tb_man.deselect(res_tree)
                watch_button['state'] = tkinter.DISABLED
                delete_button['state'] = tkinter.DISABLED
                gen_res_button['state'] = tkinter.DISABLED
                det_res_button['state'] = tkinter.DISABLED
                analyse_ag_btn['state'] = tkinter.DISABLED
                messagebox.showerror('showerror', 'DatabaseError')

        button_frame = LabelFrame(my_videos_frame, text="Commands", font=("Arial", 12))
        button_frame.pack(fill="x", expand="yes", padx=25, anchor=CENTER)

        watch_button = Button(button_frame, text='Watch video',
                              command=lambda: tb_man.see_video_result(res_tree, select_record(my_videos_frame)),
                              state=tkinter.DISABLED, font=("Arial", 12))
        watch_button.grid(row=0, column=0, padx=10, pady=10)

        delete_button = Button(button_frame, text='Delete video',
                               command=lambda: tb_man.remove_one(res_tree, select_record(
                                   my_videos_frame)), state=tkinter.DISABLED, font=("Arial", 12))
        delete_button.grid(row=0, column=1, padx=10, pady=10)

        gen_res_button = Button(button_frame, text='To general results',
                                command=lambda: self.general_res_page(root, my_videos_frame,
                                                                      video_id=select_record(my_videos_frame)),
                                state=tkinter.DISABLED, font=("Arial", 12))
        gen_res_button.grid(row=0, column=2, padx=10, pady=10)

        det_res_button = Button(button_frame, text='To detailed results',
                                command=lambda: self.detailed_res_page(root, my_videos_frame,
                                                                       video_id=select_record(my_videos_frame)),
                                state=tkinter.DISABLED, font=("Arial", 12))
        det_res_button.grid(row=0, column=3, padx=10, pady=10)

        to_main_button = Button(button_frame, text='To analysis page',
                                command=lambda: self.youtube_window(root, my_videos_frame), font=("Arial", 12))
        to_main_button.grid(row=0, column=4, padx=10, pady=10)

        analyse_ag_btn = Button(button_frame, text='Analyse again',
                                command=lambda: vid_analysis.repeat_analysis(video_id=select_record(my_videos_frame)),
                                state=tkinter.DISABLED, font=("Arial", 12))
        analyse_ag_btn.grid(row=0, column=5)

        res_tree.bind("<ButtonRelease-1>", select_record)
        tb_man.query_videos_database(res_tree)
        root.mainloop()

    def general_res_page(self, root, frame, video_id):
        frame.grid_forget()
        general_res_frame = Frame(root)
        general_res_frame.grid(row=0, column=0)
        general_label = Label(general_res_frame, text='General results of video №' + str(video_id), font=("Arial", 12))
        general_label.grid(row=0, column=1)
        to_main_button = Button(general_res_frame, text='To my videos',
                                command=lambda: self.my_videos(root, general_res_frame),
                                font=("Arial", 12))
        to_main_button.grid(row=1, column=1)

        data = db_man.get_gen_res_data(video_id)
        male_count = data[0][2]
        female_count = data[0][3]
        gender_img = data[0][11]

        angry_count = data[0][4]
        scared_count = data[0][5]
        happy_count = data[0][6]
        sad_count = data[0][7]
        surprised_count = data[0][8]
        neutral_count = data[0][9]
        emotion_img = data[0][14]

        avg_age = data[0][10]
        age_count_img = data[0][12]
        age_box_img = data[0][13]

        image_folder = 'C:/Users/serg/PycharmProjects/cpe_desktop_coursework/stats_folder/'
        gender_frame = LabelFrame(general_res_frame, text='Gender stats', font=("Arial", 12))
        male_label = Label(gender_frame, text='Male had ' + str(male_count) + ' occurrences.', font=("Arial", 12))
        male_label.grid(row=0, column=0)
        female_label = Label(gender_frame, text='Female had ' + str(female_count) + ' occurrences.', font=("Arial", 12))
        female_label.grid(row=1, column=0)
        g_img = Image.open(image_folder + gender_img)
        g_img = g_img.resize((300, 300))
        g_img = ImageTk.PhotoImage(g_img)
        gender_img = Label(gender_frame, image=g_img)
        gender_img.grid(row=2, column=0)

        age_frame = LabelFrame(general_res_frame, text='Age stats', font=("Arial", 12))
        age_label = Label(age_frame, text='Average age is ' + str(avg_age), font=("Arial", 12))
        age_label.grid(row=0, column=0, sticky='ew')
        a_b_img = Image.open(image_folder + age_box_img)
        a_b_img = a_b_img.resize((300, 300))
        a_b_img = ImageTk.PhotoImage(a_b_img)
        age_box_img = Label(age_frame, image=a_b_img)
        age_box_img.grid(row=1, column=0)
        a_c_img = Image.open(image_folder + age_count_img)
        a_c_img = a_c_img.resize((300, 300))
        a_c_img = ImageTk.PhotoImage(a_c_img)
        age_count_img = Label(age_frame, image=a_c_img)
        age_count_img.grid(row=1, column=1)

        emotion_frame = LabelFrame(general_res_frame, text='Emotion stats', font=("Arial", 12))
        angry_label = Label(emotion_frame, text='Angry people had ' + str(angry_count) + ' occurrences.',
                            font=("Arial", 12))
        angry_label.grid(row=0, column=0)
        scared_label = Label(emotion_frame, text='Scared people had ' + str(scared_count) + ' occurrences.',
                             font=("Arial", 12))
        scared_label.grid(row=1, column=0)
        happy_label = Label(emotion_frame, text='Happy people had ' + str(happy_count) + ' occurrences.',
                            font=("Arial", 12))
        happy_label.grid(row=2, column=0)
        sad_label = Label(emotion_frame, text='Sad people had ' + str(sad_count) + ' occurrences.', font=("Arial", 12))
        sad_label.grid(row=0, column=1)
        surprised_label = Label(emotion_frame, text='Surprised people had ' + str(surprised_count) + ' occurrences.',
                                font=("Arial", 12))
        surprised_label.grid(row=1, column=1)
        neutral_label = Label(emotion_frame, text='Neutral people had ' + str(neutral_count) + ' occurrences.',
                              font=("Arial", 12))
        neutral_label.grid(row=2, column=1)
        em_img = Image.open(image_folder + emotion_img)
        em_img = em_img.resize((300, 300))
        em_img = ImageTk.PhotoImage(em_img)
        emotion_img = Label(emotion_frame, image=em_img)
        emotion_img.grid(row=3, column=0)

        def show_frame(gender, age, emotion):
            if gender == 1:
                age_frame.grid_forget()
                emotion_frame.grid_forget()
                gender_frame.grid(row=3, column=1)
            elif age == 1:
                emotion_frame.grid_forget()
                gender_frame.grid_forget()
                age_frame.grid(row=3, column=1)
            else:
                age_frame.grid_forget()
                gender_frame.grid_forget()
                emotion_frame.grid(row=3, column=1)

        gender_button = Button(general_res_frame, text='Show gender stats',
                               command=lambda: show_frame(1, 0, 0), font=("Arial", 12))
        gender_button.grid(row=2, column=0)
        age_button = Button(general_res_frame, text='Show age stats', command=lambda: show_frame(0, 1, 0),
                            font=("Arial", 12))
        age_button.grid(row=2, column=1)
        emotion_button = Button(general_res_frame, text='Show emotion stats', command=lambda: show_frame(0, 0, 1),
                                font=("Arial", 12))
        emotion_button.grid(row=2, column=2)

        detailed_button = Button(general_res_frame, text='To detailed results',
                                 command=lambda: self.detailed_res_page(root, general_res_frame, video_id),
                                 font=("Arial", 12))
        detailed_button.grid(row=4, column=1)

        root.mainloop()

    def detailed_res_page(self, root, frame, video_id):
        frame.grid_forget()
        detailed_res_frame = Frame(root)
        detailed_res_frame.grid(row=0, column=0)

        style = ttk.Style()
        style.configure("Treeview", background="#D3D3D3", foreground="black",
                        rowheight=25, fieldbackground="#D3D3D3")
        res_tree_frame = Frame(detailed_res_frame)
        res_tree_frame.pack(pady=25, padx=50)

        res_tree_scroll = Scrollbar(res_tree_frame)
        res_tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        det_res_tree = ttk.Treeview(res_tree_frame, yscrollcommand=res_tree_scroll.set, selectmode="browse")
        det_res_tree.pack()
        res_tree_scroll.config(command=det_res_tree.yview)

        det_res_tree['columns'] = ("ID", "Video ID", "Gender", 'Age', 'Emotion', 'Photo path')

        # Format Our Columns
        det_res_tree.column("#0", width=0, stretch=NO)
        det_res_tree.column("ID", anchor=CENTER, width=70)
        det_res_tree.column("Video ID", anchor=CENTER, width=70)
        det_res_tree.column("Gender", anchor=CENTER, width=100)
        det_res_tree.column("Age", anchor=CENTER, width=100)
        det_res_tree.column("Emotion", anchor=CENTER, width=100)
        det_res_tree.column("Photo path", anchor=CENTER, width=300)

        # Create Headings
        det_res_tree.heading("#0", text="", anchor=W)
        det_res_tree.heading("ID", text="ID", anchor=CENTER)
        det_res_tree.heading("Video ID", text="Video ID", anchor=CENTER)
        det_res_tree.heading("Gender", text="Gender", anchor=CENTER)
        det_res_tree.heading("Age", text="Age", anchor=CENTER)
        det_res_tree.heading("Emotion", text="Emotion", anchor=CENTER)
        det_res_tree.heading("Photo path", text="Photo path", anchor=CENTER)

        def select_record(self):
            try:
                selected = det_res_tree.focus()
                values = det_res_tree.item(selected, 'values')
                photo_button['state'] = tkinter.NORMAL
                return values[0]
            except IndexError:
                messagebox.showerror('showerror', 'Choose an entry')
            except mysql.connector.Error:
                tb_man.deselect(det_res_tree)
                photo_button['state'] = tkinter.DISABLED
                messagebox.showerror('showerror', 'DatabaseError')

        button_frame = LabelFrame(detailed_res_frame, text="Commands", font=("Arial", 12))
        button_frame.pack(fill="x", expand="yes", padx=20)

        photo_button = Button(button_frame, text='View photo', command=lambda: tb_man.view_photo(det_res_tree),
                              state=tkinter.DISABLED, font=("Arial", 12))
        photo_button.grid(row=0, column=0, padx=10, pady=10)

        gen_res_button = Button(button_frame, text='To general results',
                                command=lambda: self.general_res_page(root, detailed_res_frame, video_id=video_id),
                                font=("Arial", 12))
        gen_res_button.grid(row=0, column=2, padx=10, pady=10)

        my_videos_btn = Button(button_frame, text='To my videos',
                               command=lambda: self.my_videos(root, detailed_res_frame), font=("Arial", 12))
        my_videos_btn.grid(row=0, column=3, padx=10, pady=10)

        det_res_tree.bind("<ButtonRelease-1>", select_record)
        tb_man.query_results_database(det_res_tree, video_id)
        root.mainloop()





if __name__ == "__main__":
    db_man = DBManager()
    vid_analysis = VideoAnalysis()
    yt_man = YoutubeManager()
    tb_man = TableManager()

    root = Tk()
    root.title('Video analyser')
    root.geometry("1000x550")
    frame = Frame(root)
    win = WindowsManager(root, frame)
    win.my_videos(root, frame)
    root.mainloop()



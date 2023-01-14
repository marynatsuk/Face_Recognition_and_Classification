import tkinter

from pytube import YouTube
import requests
import json
from urllib.parse import urlparse, parse_qs
from db_manager import DBManager
from video_analysis import VideoAnalysis
from tkinter import messagebox
import os

db_man = DBManager()
vid_analysis = VideoAnalysis()


class YoutubeManager:
    def __init__(self):
        self.folder_path = 'C:/Users/serg/PycharmProjects/cpe_desktop_coursework/downloaded_videos'
        self.api_key = 'AIzaSyDLtCySc1gSpyguuzcl16ij-4x7QwJp0R4'

    def parse_yt_data(self, yt_entry):
        try:
            video_link = yt_entry.get()
            if video_link == '':
                messagebox.showerror('showerror', 'Enter Youtube link')
            else:
                video_yt_id = self.get_video_id(video_link)
                if video_yt_id is None:
                    messagebox.showerror('showerror', 'Incorrect link. Try again!')
                    yt_entry.delete(0, tkinter.END)
                else:
                    video_id = db_man.check_video_ex(video_yt_id)
                    if video_id is False:
                        video_path = self.download_video(video_link)
                        video_name, channel_id = self.get_video_data(video_yt_id, self.api_key)
                        channel_name = self.get_channel_stats(channel_id, self.api_key)
                        print(video_path, video_yt_id, video_name, channel_name, channel_id)
                        db_man.add_entry_videos(video_yt_id, video_name, channel_id, channel_name, video_link, video_path)
                        vid_analysis.start_analysing(video_path)
                        messagebox.showinfo('showinfo', 'Analysis complete!')
                    else:
                        messagebox.showinfo('showinfo', 'This video has already been analysed!')
        except requests.exceptions.RequestException:
            print('Could not get id')

    def download_video(self, video_link):
        try:
            youtubeObject = YouTube(video_link)
            youtubeObject = youtubeObject.streams.get_highest_resolution()
            downloaded_video = youtubeObject.download(self.folder_path)
            messagebox.showinfo('showinfo', "Download is completed successfully")
            downloaded_path = os.path.abspath(downloaded_video)
            return downloaded_path
        except KeyError:
            print("An error has occurred")
            return None

    def get_video_id(self, link):
        query = urlparse(link)
        if query.hostname == 'youtu.be':
            video_id = query.path[1:]
            return video_id
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                video_id = p['v'][0]
                return video_id
            if query.path[:7] == '/embed/':
                video_id = query.path.split('/')[2]
                return video_id
            if query.path[:3] == '/v/':
                video_id = query.path.split('/')[2]
                return video_id

        return None

    def get_video_data(self, video_id, api_key):
        snippet_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
        print(snippet_url)
        json_url_snippet = requests.get(snippet_url)
        data = json.loads(json_url_snippet.text)
        try:
            video_name = data['items'][0]['snippet']['title']
            channel_id = data['items'][0]['snippet']['channelId']

            return video_name, channel_id
        except KeyError:
            print(f'Error! Could not get data.')

    def get_channel_stats(self, channel_id, api_key):
        snippet_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={api_key}"
        print(snippet_url)
        json_url_snippet = requests.get(snippet_url)
        data = json.loads(json_url_snippet.text)
        try:
            channel_name = data['items'][0]['snippet']['title']
            return channel_name
        except KeyError:
            print(f'Error! Could not get data.')

import requests
from bs4 import BeautifulSoup as bs
import re
import os
from pytube import YouTube as yt

class Playlist():
    def __init__(self, title, playlist_link,):
        self.title = title
        self.link = playlist_link
        self.data = []

    def add_vids(self, vids):
        self.data = vids

class Video():
    def __init__(self, thumbnail, title, vid_link):
        self.thumbnail = thumbnail
        self.title = title
        self.link = vid_link


def download_all_pl_from_channel():
    page = requests.get("https://www.youtube.com/channel/UCcqyp9jK9eV8hlouDY5bSfw/playlists")
    chow = bs(page.content,'html.parser')
    playlists = []
    chow
    b=chow.select('.yt-lockup-content .yt-lockup-title .yt-uix-sessionlink ')
    b
    listofb = list(b)
    for each in listofb:
        playlists.append(Playlist(each['title'], each['href']))
    return playlists

download_all_pl_from_channel()

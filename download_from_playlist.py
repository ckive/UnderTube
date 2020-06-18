import requests
import re
from bs4 import BeautifulSoup as bs
from pytube import YouTube as yt

class Video():
    def __init__(self, thumbnail, title, link):
        self.thumbnail = thumbnail
        self.title = title
        self.link = link

#input = ("Enter playlist link: ")
#Nmap 5 vids
input = "https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBsINfLVidNVaZ-7_v1NJIo"

page = requests.get(input)
soup = bs(page.content,"html.parser")

#gets the main page with all other elements within it
main_page = soup.find("div", id="content")

#for sanity check: should be <class 'bs4.element.Tag'>
main_page_type = type(main_page)
#print(main_page)

#Get thumbnail files
thumbnails = soup.find_all("img", alt="", )

tn_list = []
print(len(tn_list))
#link of thumbnail img
for thumb in thumbnails:                #length 147 are vid thumbnails
    if thumb.has_attr('data-thumb') and len(thumb['data-thumb'])==147:
        #print(thumb['data-thumb'])
        tn_list.append(thumb['data-thumb'])


#find individual elements of title + links
titles = main_page.find_all("a", class_="pl-video-title-link")
titles_type = (type(titles))        # Should be ResultSet
titles_length = len(titles)         # Should be # of vids in playlist

title_list = []
vid_link_list = []
#Grab title text and video link
for title in titles:
    title_list.append(title.text)
    vid_link_list.append(title['href'])

play_list = []
for i in range(len(title_list)):
    play_list.append(Video(tn_list[i],title_list[i],vid_link_list[i]))

print(len(play_list))
###############Organized --> play_list --> a list of Videos###############
for vid in vid_link_list:
    yt(vid).streams.first().download("/Users/Dan/Desktop/Projects/UnderTube-sinAlgo/ytvids")

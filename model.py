# UnderTube: accessing YouTube Under GFW (+ no ads, + no algorithms)

# Dependencies
import requests
from bs4 import BeautifulSoup as bs
import re
import os
from pytube import YouTube as yt

class Channel():
    def __init__(self, title, id_link, tn):
        self.title = name
        self.id_link = id_link
        self.tn = tn
        self.playlists = []
        self.videos = []

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def add_videos(self, video):
        self.videos.append(video)

class Playlist():
    def __init__(self, title, playlist_link, channel):
        self.title = title
        self.link = playlist_link
        self.channel = channel
        self.data = []

    def add_vids(self, vids):
        self.data = vids

class Video():
    def __init__(self, title, vid_link):
        #self.thumbnail = thumbnail
        self.title = title
        self.link = vid_link

class Buffer():
    def __init__(self):
        self.data = []

    def add_to_buffer(self, element):
        self.data.append(element)

    def show_contents(self):
        return self.data

    def remove_from_buffer(self, index):
        self.data.pop(index)


BASE = "https://www.youtube.com/"

#YT search filter!
#   video:      &sp=EgIQAQ%253D%253D
#   playlist:   &sp=EgIQAw%253D%253D
#   channel:    &sp=EgIQAg%253D%253D
#                        ^ that's the only difference

# TODO: abstract for either from search_query or from channel's playlist page


# query_videos(): string --> listof Videos
# given string to search, searches and returns a list of videos
def query_videos(term):
    page = requests.get("https://www.youtube.com/results?search_query=" + str(term) + "&sp=EgIQAQ%253D%253D")
    chow = bs(page.content, 'html.parser')
    videos = []
    info = chow.select(".yt-uix-tile-link")
    for i in range(len(info)):
        videos.append(Video(info[i].text, info[i]['href']))


# query_playlists(): string --> listof Playlists
# gets a string input as search term and searches for all related playlists
# from the YouTube search page
def query_playlists(term):
    page = requests.get("https://www.youtube.com/results?search_query=" + str(term) + "&sp=EgIQAw%253D%253D")
    chow = bs(page.content, 'html.parser')
    playlists = []

    # parsing page for part describing playlist information
    title=chow.select(".yt-lockup-content .yt-lockup-title")
    link=chow.select(".yt-lockup-content .yt-lockup-meta .yt-uix-sessionlink ")
    channel=chow.select(".yt-lockup-content .yt-lockup-byline .yt-uix-sessionlink")
    listof_titles = list(title)
    temp_link_list = list(link)
    listof_links = []
    listof_channels = list(channel)

    # matching # of links to # of titles & channel names
    for i in range(len(temp_link_list)):
        if '/playlist' in temp_link_list[i]['href']:
            listof_links.append(temp_link_list[i]['href'])

    # creating Playlist Objects
    for i in range(len(listof_links)):
        # create dict for channel name & id
        channel_dict = {"name": listof_channels[i].text, "id": listof_channels[i]['href']}
        playlists.append(Playlist(listof_titles[i], listof_links[i], channel_dict))
    return playlists


# query_channels(): string --> listof Channels
# given string to search, searches and returns a list of videos
def query_channels(term):
    term = 'dan dan yang'
    page = requests.get("https://www.youtube.com/results?search_query=" + str(term) + "&sp=EgIQAg%253D%253D")
    chow = bs(page.content, 'html.parser')
    channels = []
    channel_tn = chow.select(".yt-thumb-simple")
    channel_info = chow.select(".yt-lockup-title .yt-uix-tile-link")
    #CAUTION: sometimes an element (0th) can be an AD
    for i in range(len(channel_info)):
        channels.append(Channel(channel_info[i].text), channel_info[i]['href'], sanitize(channel_tn[i].img['src']))
    return channels


# TODO: MERGE this with the above and add more functionality to abstract "Search"
# grab_playlists_from_channel: string --> listof Playlists
# given link to channel's playlist tab, crawls to find all playlists returns
def grab_playlists_from_channel(channel_id):
    page = requests.get(BASE + channel_id + "/playlists")
    chow = bs(page.content,'html.parser')
    playlists = []
    b=chow.select('.yt-lockup-content .yt-lockup-title .yt-uix-sessionlink ')
    listofb = list(b)
    for each in listofb:
        playlists.append(Playlist(each['title'], each['href']))
    return playlists


# fill_playlist(): Playlist --> None
# given link to playlist, parses page and creates a Video for each video,
# append all Videos to Playlist.data
def fill_playlist(playlist):
    pl_link = playlist.link
    #pl_link = "https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBsINfLVidNVaZ-7_v1NJIo"
    input = "https://www.youtube.com" + str(pl_link)
    #Nmap 5 vids for testing:
    #"https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBsINfLVidNVaZ-7_v1NJIo"

    page = requests.get(input)
    soup = bs(page.content,"html.parser")

    #gets the main page with all other elements within it
    main_page = soup.find("div", id="content")

    #for sanity check: should be <class 'bs4.element.Tag'>
    #main_page_type = type(main_page)

    #Get thumbnail links        !deprecated_feature!
    #thumbnails = soup.find_all("img", alt="", )
    #tn_list = []
    #for thumb in thumbnails:                #length 147 are vid thumbnails
    #    if thumb.has_attr('data-thumb') and len(thumb['data-thumb'])==147:
    #        #print(thumb['data-thumb'])
    #        tn_list.append(thumb['data-thumb'])

    #find individual elements of title + links
    titles = main_page.find_all("a", class_="pl-video-title-link")
    #Sanity check --> titles_type = (type(titles))        Should be ResultSet

    title_list = []
    vid_link_list = []
    #Grab title text and video link
    for title in titles:
        title_list.append(title.text)
        vid_link_list.append(title['href'])

    play_list = []
    for i in range(len(title_list)):
        play_list.append(Video(title_list[i], vid_link_list[i]))
    playlist.add_vids(play_list)


# string --> string
# sanitize to keep alphanumeric & chinese characters
def sanitize(line):
    rule = re.compile("[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
    return line


# download: OrC(Playlist, Video) --> None
# given a Video download the Video in dir 'default' under 'ytvids'.
# given a Playlist, fill the playlist, then download its videos into a directory
# with Playlist title

def download(to_do):
    #TODO: check if video
    dst = os.getcwd()+'/defaults'
    # TODO: incorporate download_all_playlist inhere
    if isinstance(to_do, Video):
        yt("https://www.youtube.com" + to_do.link).streams.first().download(dst)
    elif isinstance(to_do, Playlist):       #what about if playlist already downloaded, if download into same dir again, what will happen?
        fill_playlist(to_do)
        vids = to_do.data
        if not os.path.exists(os.getcwd() + '/ytvids/' + to_do.title.select('.yt-uix-tile-link')[0].text):
            #sanitize title for directory creation
            dir_name = sanitize(to_do.title.select('.yt-uix-tile-link')[0].text)
            #os.mkdir('./ytvids/' + dir_name)
            os.chdir('./ytvids')
            os.mkdir(dir_name)
            dst = os.getcwd() + '/' + dir_name
        for vid in vids:
            yt("https://www.youtube.com" + vid.link).streams.first().download(dst)
        os.chdir('..')



# download_all_playlist: listof Playlists --> None
# loops download() on each playlist of list of Playlists
def download_all_playlist(many_playlists):
    for playlist in many_playlists:
        download(playlist)

#download_all_playlist(grab_playlists_from_channel("channel_id"))

# term = "Metasploit for Network Security Tutorials"
# a = query_playlists(term)
# show_search(a)              #show results & index
# selection = int(input("Enter index of which playlist you'd like to download: "))
# fill_playlist(a[selection]) #fill the selection
# download(a[selection])




#YT search filter!
#   video:      &sp=EgIQAQ%253D%253D
#   playlist:   &sp=EgIQAw%253D%253D
#   channel:    &sp=EgIQAg%253D%253D

#if __name__ == "__main__":
#    main()

# good way of verifying contents in list
# all(isinstance(element, Playlist) for element in to_show):
# vids is Playlist --> False; isinstance(vids, Playlist) --> True;
# super useful way to sanitize inputs to alphanumeric inputs
# re.sub("[^0-9a-zA-Z]+", "-", to_sanitize)

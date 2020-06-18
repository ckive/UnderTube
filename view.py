import model

# init_search: None --> None
# displays initial search options
def init_search():
    #search (filter) video
    print("What would you like to search for?")
    print("1: Videos     2: Playlists     3: Channels     or enter 'Q' to quit")

# search: string --> None
# controller passes option, show corresponding search text
def search(option):
    print("Please enter your " + option + " search: ")

# show_search: OrC:(listof Videos, listof Playlists) --> None
# prints out index and title of Video or Playlist.
def show_search(to_show):
    for i in range(len(to_show)):
        print('{:10}'.format(i) + to_show[i].title.select('.yt-uix-tile-link')[0].text)


def invalid():
    print("Invalid selection, please try again")

def bye():
    print("Thanks for using UnderTube")


def show_actions():
    print("To download an element, enter 'D'")
    print("To use buffer functionality, enter 'B'")
    print("To exit, enter 'Q'")
    print("To perform a new search, enter 'N'")
    print("For more information, enter 'I'")

def select():
    print("Select index of element")

def info():
    print("GO suck one")

def buffer_choices():

    print("Show contents of buffer with 'S'")
    print("Add to buffer with 'A'")
    print("Remove from buffer with 'R'")
    print("Finish buffer manipulation with 'F'")

def buffer_contents(buffer):
    for element in buffer.show_contents():
        print('{:10}'.format(i) + element.title)
    for i in range(len(buffer.show_contents())):
        print('{:10}'.format(i) + buffer.show_contents()[i].title)

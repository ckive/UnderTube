import model
import view

def start():
    while True:
        try:
            view.init_search()
            search_choice = str(input()).upper() #1, 2, 3, 9
            if search_choice == '1' or '2' or '3' or 'Q':
                if search_choice == 'Q':
                    quit()
                search(search_choice)
        except Exception as e:
            view.invalid()


def search(option):
    buf = model.Buffer()
    view.search(operation[option][0])           #print
    term = str(input())                         #get query
    results = operation[option][1](term)        #return list of vids
    view.show_search(results)                   #show results
    execute_actions(results, buf)               #move to actions


def execute_actions(payload, buffer):           #payload is a list!
    view.show_actions()                         #show actions
    action = str(input()).upper()               #get action D,B,N,I,Q
    if action == 'D':                           #download payload
        operation[action](payload)
    elif action == 'B':
        operation[action](payload, buffer)      #use buffer
    else:
        operation[action]()

def use_buffer(results, buffer):
    view.show_search(results)
    while True:
        try:
            view.buffer_choices()
            buf_choice = str(input()).upper()
            if buf_choice == 'S':                   #show contents
                view.buffer_contents(buffer)

            elif buf_choice == 'A':                 #add to buffer
                view.select()
                ind = str(input())
                buffer.add_to_buffer(results[ind])

            elif buf_choice == 'R':                 #remove from buffer
                view.buffer_contents(buffer)
                view.select()
                ind = str(input())
                buffer.remove_from_buffer(buffer.show_contents()[ind])

            elif buf_choice == 'F':                 #finished with buffer
                buffer_seq(buffer)

            view.invalid()
        except Exception as e:
            print(e)       #


def single_download_seq(payload):               #either 1 vid or 1 playlist
    view.select()
    selection = int(input())
    download(payload[selection])                #download the selection
    #exit()

def buffer_seq(buffer):
    for elements in buffer:
        model.download(elements)
    #DOWNLOAD ALL IN BUFFER



def quit():
    view.bye()
    exit()

operation = {'1': ('video', model.query_videos),'2': ('playlist', model.query_playlists),'3': ('channel', model.query_channels),'Q': quit,'D': single_download_seq,'B': use_buffer,'N': start,'I': 'lol'}


if __name__ == "__main__":
    start()

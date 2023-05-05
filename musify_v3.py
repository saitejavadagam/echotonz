import threading
import time
from tkinter import *
from pygame import mixer
from customtkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from mutagen.mp3 import MP3
from threading import Thread
import speech_recognition as sr

mixer.init()

songlist = []
songnames = []
background = "#333333"  # light black


# function to add songs path to the songlist
def add_song():
    song = filedialog.askopenfilenames(initialdir='songslib/', filetypes=(("mp3 files", "*.mp3"),))
    for i in song:
        if i not in songlist:
            songlist.append(i)
    addtobox()


# function to print songs name in the terminal
def printsong():
    for x in songlist:
        x = x.replace('.mp3', '')
        print(x)
    print(len(songlist))


# some global variables
count = 0
j = 0
step = 0

exit_event = threading.Event()


# function to play the song which is currently selected by cursor or in play sequence
def play_song():

    if len(songlist) != 0:

        mixer.music.load(str(songlist[count]))
        displaybox.activate(count)
        mixer.music.play(loops=0,start=0)
        name = "Playing:-\t" + songnames[count] + " " * 200
        Label(root, text=name, bg=background, fg='white', font=("Arial", 16)).place(x=300, y=475)

        if not startprogress.is_alive():
            startprogress.__init__(target=progresscheck)
            startprogress.start()
    else:
        print("Songs List is empty!!...")


# function to stop the current playing song
def togglemusic():
    global song_bar, songlist, count, j
    i = displaybox.curselection()
    if i != j:
        if len(i) != 0:
            count = i[0]
            song_bar.set(0)
            play_song()
    elif mixer.music.get_busy():
        mixer.music.pause()
        play_btn.configure(image=play_img)
    else:
        mixer.music.unpause()
        play_btn.configure(image=stop_img)
    j = i



# function to play the next song in the sequence
def next_song():
    mixer.music.stop()
    exit_event.set()
    song_bar.set(0)
    time.sleep(0.5)
    global count
    global songlist
    if count < len(songlist) - 1:
        count += 1
    else:
        count = 0
    play_song()


# function to play the previous song in the sequence
def prev_song():
    mixer.music.stop()
    exit_event.set()
    song_bar.set(0)
    time.sleep(0.5)
    global count
    if count >= 0:
        count -= 1
    else:
        count = len(songlist) - 1
    play_song()


# function to get the song duration in seconds
def songlength():
    global songlist
    song = MP3(songlist[count])
    return int(song.info.length)


# creating the GUI window for the music player
root = Tk()
root.title('Musify')
root.iconbitmap('icons/biticon.ico')
root.geometry('1280x800')
root.resizable(False, True)
root.configure(bg=background)

wf = root.winfo_width() / 600
hf = root.winfo_height() / 300


# creating a listbox for displaying songs list in the GUI window
def displaylistbox():
    list_box = Listbox(root, bg='black', fg='#00ff00', font=("Arial", 16), selectbackground='grey',
                       activestyle='underline',
                       selectforeground='white', width=300, height=15)
    return list_box


# function to add songs in songslist to the listbox
def addtobox():
    for i in songlist:
        i = i.replace('.mp3', '')
        i = i[i.rfind('/') + 1:]
        if i not in displaybox.get(0, END):
            displaybox.insert(END, i)
            songnames.append(str(i))

# def speechRecognition():
#
#     r = sr.Recognizer()
#
#     with sr.Microphone as source:
#         audio = r.listen(source)
#
#         try:
#             text = r.recognize_google(audio)
#             print('you said {}' .format(text))
#             return text[0]
#         except:
#             print('sorry your voice not recognized')


def progresscheck():
    global song_bar, exit_event
    song_bar.set(0)
    x = 0
    factor = 0.1
    exit_event.clear()
    length = songlength()
    slen = ((1 + 0.042 / factor) / length ) * factor

    p,c=0,0

    while not x >= 1 and not exit_event.is_set():
        if x >= 1:break
        if not mixer.music.get_busy():
            time.sleep(factor)
        else:
            p = song_bar.get()
            x += slen
            song_bar.set(x)
            time.sleep(factor)
            c = song_bar.get()
            if p+slen != c:
                x = c
                mixer.music.set_pos(song_bar.get()*length)
    mixer.music.stop()



            # print(song_bar.get())


startprogress = Thread(target=progresscheck)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
print_menu = Menu(my_menu)
toggle_display = Menu(my_menu)
info_menu = Menu(my_menu)

my_menu.add_cascade(label='File', menu=add_song_menu)
my_menu.add_cascade(label='Print', menu=print_menu)
my_menu.add_cascade(label='Info', menu=info_menu)
add_song_menu.add_cascade(label='Add songs', command=add_song)
print_menu.add_cascade(label='Click to print song names', command=printsong)
print_menu.add_cascade(label='Display', command=displaylistbox)
info_menu.add_cascade(label='About')

# images

prev_img = CTkImage(Image.open('icons/back.png').resize((20, 20)))
play_img = CTkImage(Image.open('icons/play.png').resize((20, 20)))
next_img = CTkImage(Image.open('icons/next.png').resize((20, 20)))
stop_img = CTkImage(Image.open('icons/pause.png').resize((20, 20)))
left_img = ImageTk.PhotoImage(Image.open('icons/disc.png').resize((150, 150)))
right_img = ImageTk.PhotoImage(Image.open('icons/sound.png').resize((150, 150)))

# buttons
prev_btn = CTkButton(root, text='', image=prev_img, command=prev_song, fg_color='green', hover_color='#00ff00')

prev_btn.place(x=400, y=600)

play_btn = CTkButton(root, text='', image=play_img, command=togglemusic, fg_color='green', hover_color='#00ff00')

play_btn.place(x=550, y=600)

# playpause = CTkButton(root, text='', image=stop_img, command=speechRecognition, fg_color='green', hover_color='#00ff00')
# playpause.place(x=550, y=640)

CTkButton(root, text='', image=next_img, command=next_song, fg_color='green', hover_color='#00ff00').place(x=700, y=600)

# image Labels

Label(root, image=left_img, bg=background).place(x=100, y=550)
Label(root, image=right_img, bg=background).place(x=1025, y=550)
Label(root, text="Musify - MP3 Player", fg='white', bg=background, font=("Muroslant", 19)).pack(padx=1)

displaybox = displaylistbox()

displaybox.pack(padx=20, pady=3)

song_bar = CTkSlider(master=root, width=600, hover=True, progress_color="cyan", button_hover_color='red')
song_bar.place(x=320, y=555)
song_bar.set(0)

root.mainloop()

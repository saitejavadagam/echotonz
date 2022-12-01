from tkinter import *
from tkinter import filedialog
from pygame import mixer

mixer.init()

songlist = []


def add_song():
    song = filedialog.askopenfilenames(initialdir='songslib/', filetypes=(("mp3 files", "*.mp3"),))
    for i in song:
        songlist.append(str(i).replace("C:/Users/saite/PycharmProjects/musify/", ""))


def printsong():
    for x in songlist:
        x = x.replace('songslib/','')
        x = x.replace('.mp3','')
        print(x)
    print(len(songlist))


count = 0


def play_song():
    global songlist
    mixer.music.load(str(songlist[count]))
    mixer.music.play(loops=0)


def stop_song():
    mixer.music.stop()


def next_song():
    global count
    global songlist
    if count < len(songlist) - 1:
        count += 1
    else:
        count = 0
    play_song()


def prev_song():
    global count
    if count >= 0:
        count -= 1
    else:
        count = len(songlist) - 1
    play_song()


root = Tk()
root.title("♫ Player")
root.geometry('600x300')
root.configure(bg='grey')
# creating a menu bar


def displaylistbox():
    list_box = Listbox(root, bg='black', fg='green', selectbackground='grey', selectforeground='black', width=70)
    return list_box


def addtobox():
    for i in songlist:
        i = i.replace('songslib/', '')
        i = i.replace('.mp3', '')
        displaybox.insert(END, i)


def selectplay():
    global count
    i = displaybox.curselection()
    count = i[0]
    play_song()

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
print_menu = Menu(my_menu)
toggle_display = Menu(my_menu)

my_menu.add_cascade(label='File', menu=add_song_menu)
my_menu.add_cascade(label='Print',menu=print_menu)
add_song_menu.add_cascade(label='select one song', command=add_song)
print_menu.add_cascade(label='Click to print song names', command=printsong)
print_menu.add_cascade(label='Display', command=displaylistbox)

# print_btn = Button(root, text='print', command=printsong).place(x=260, y=150)

Button(root, text='prev', command=prev_song).place(x=220, y=220)

Button(root, text='play', command=play_song).place(x=260, y=220)

Button(root, text='stop', command=stop_song).place(x=300, y=220)

Button(root, text='next', command=next_song).place(x=340, y=220)

Button(root, text='Play Selected',command=selectplay).place(x=257, y=180)
displaybox = displaylistbox()

displaybox.pack()

Button(root, text='Reload Songs', command=addtobox).place(x=515,y=20)

root.mainloop()

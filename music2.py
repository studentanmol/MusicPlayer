from lyricsgenius import Genius
import api_key
import tkinter as tk
from tkinter import *
from tkinter.ttk import * 
from tkinter import filedialog
import pygame
import gc
import requests
import requests
import shutil
import os
from PIL import ImageTk, Image


genius = Genius(api_key.token)

# Initialise the Node
class Node:
    def __init__(self, data):
        self.item = data
        self.next = None
        self.prev = None

# Class for doubly Linked List
class doublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    # Insert element at the end
    def insert(self, data):

        # Check if the list is empty
        if self.head is None:
            new_node = Node(data)
            self.head = new_node
            self.tail = self.head
            self.tail.next = self.head
            self.head.prev = self.tail
            return
        
        new_node = Node(data)
        self.tail.next = new_node
        new_node.prev = self.tail
        new_node.next = self.head
        self.head.prev = new_node
        self.tail = self.tail.next
    
    # Delete the element
    def delete(self,data):
        # Check if the List is empty
        if self.head is None:
            print("The playlist is empty, no song to delete")
            return 
        n = self.head

        # For first node
        if(n.item == data):
            if self.head.next is self.head:
                self.head = None
                self.tail = None
                return
            self.head = self.head.next
            self.head.prev = self.tail
            self.tail.next = self.head
            gc.collect()
            return
        
        # For middle nodes
        while n.next is not self.head:
            if(n.item == data):
                n.prev.next = n.next
                n.next.prev = n.prev
                gc.collect()
                return
            n = n.next
        
        # For last node
        if(n.item == data):
            self.tail = self.tail.prev
            self.tail.next = self.head
            self.head.prev = self.tail
            gc.collect()
            return

        print("Song not Found")
    
    # Traversing and Displaying each element of the list
    def display(self):
        count = 1
        if self.head is None:
            print("Your Playlist is Empty")
            return

        else:
            print("\nYour Playlist:")
            n = self.head
            while n.next is not self.head:
                print(f"{count}) {n.item}")
                count=count+1
                n = n.next
            print(f"{count}) {n.item}")




# Start Main program 
# Create a new Doubly Linked List using object
DLL = doublyLinkedList()

#Initialzing pygame mixer
pygame.init() 

root = tk.Tk()

DLL.insert("Easy On Me.mp3")


class player:

    # Start at head of list
    global var
    var = DLL.head

    global MUSIC_END
    MUSIC_END = pygame.USEREVENT+1
    pygame.mixer.music.set_endevent(MUSIC_END)
    
    def get_info(self,sname):
        #sname = song_name.get(first=END)
        sname = sname.replace(" ",'_')
        sname = sname.replace(".mp3",'')
        print(sname)
        song=genius.search_song(sname)
        artist_name.delete(0,END)
        artist_name.insert(END,song.artist)
        r = requests.get(song.header_image_thumbnail_url, stream=True)
        if r.status_code == 200:
            with open(f"song_image\{sname}.gif", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        img = ImageTk.PhotoImage(Image.open(f"song_image\{sname}.gif"))
        img_button=tk.Button(root, image = img,compound = LEFT)
        img_button.image = img
        img_button.place(relx=0.9,rely=0.1)
        print(song.header_image_thumbnail_url)

    
    def add_song(self):
        songs = filedialog.askopenfilenames(initialdir='C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project\\songs',title='Add Music To Playlist',filetypes=(('mp3 Files' , '*.mp3'),))
        for song in songs:
            songs = song.replace('C:/Users/Anmol/Desktop/Data Structures/mini_project/songs/','')
            song_playlist.insert(END,songs)
            DLL.insert(songs)
            DLL.display()

    def play_song(self):
        song = song_playlist.curselection()
        global MUSIC_END
        if song:
            song = f'C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project\\songs\\{song_playlist.get(song)}'
            s = song
            print(f'songis{song}')
        else:
            song = f'C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project\\songs\\{var.item}'
            s = var.item
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        song_name.delete(0,END)
        song_name.insert(END,var.item)
        self.get_info(s)
    
    def check_event(self):
        global var
        global MUSIC_END
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                var=var.next
                print("Music ended")
                self.play_song()
        root.after(100, self.check_event)

    def stop_song(self):
        pygame.mixer.music.stop()
        song_playlist.selection_clear(ACTIVE)

    global paused
    paused=False
    def pause_song(self):
        global paused
        if paused:
            pygame.mixer.music.unpause()
            paused = False
        else:
            pygame.mixer.music.pause()
            paused = True


    def play_next_song(self):
        global var
        var = var.next
        """song = f'C:/Users/Anmol/Desktop/Data Structures/mini_project/songs/{var.item}'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        song_playlist.selection_clear(0,END)"""
        self.play_song()
        song_name.delete(0,END)
        song_name.insert(END,var.item)
        self.get_info(var.item)

    def play_previous_song(self):
        global var
        var = var.prev
        """song = f'C:/Users/Anmol/Desktop/Data Structures/mini_project/songs/{var.item}'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        song_playlist.selection_clear(0,END)"""
        self.play_song()
        song_name.delete(0,END)
        song_name.insert(END,var.item)
        self.get_info(var.item)

    def set_volume(self):
        pygame.mixer.music.set_volume(float(v1.get()/100))
    
    def on_closing(self):
        l = os.listdir('C:/Users/Anmol/Desktop/Data Structures/mini_project/song_image/')
        for name in l:
            os.remove(f'C:/Users/Anmol/Desktop/Data Structures/mini_project/song_image/{name}')
        root.destroy()
    
    def delete(self):
        global var
        song = song_playlist.curselection()
        if song:
            song = song_playlist.get(song)
        else:
            song = var.item
        idx = song_playlist.get(0,END).index(song)
        song_playlist.delete(idx)
        DLL.delete(song)
        var = var.next
        self.play_song()
    
Music = player()


root.title('Music Player')
root.geometry('600x600')
root.config(bg='gray')
song_list = tk.Label(root,width=50,height=10,bg='blue',fg='white',highlightcolor='grey')
song_list.pack(pady=20)

song_playlist = tk.Listbox(root,width=40,height=14,bg='red',fg='yellow',highlightcolor='grey')
song_playlist.pack(pady=20)
song_playlist.insert(END,DLL.head.item)

song_name = tk.Listbox(root,width=15,height=8,bg='red',fg='white',highlightcolor='grey')
artist_name = tk.Listbox(root,width=15,height=8,bg='orange',fg='black',highlightcolor='grey')

frame = tk.Frame(root,bg='blue')
frame.pack()

photoimage6 = PhotoImage(file = "C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project/prev.gif").subsample(13, 13)
previous_button=tk.Button(root, image = photoimage6,compound = LEFT, command=lambda: Music.play_previous_song())

photoimage5 = PhotoImage(file = "C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project/next.gif").subsample(13, 13)
next_button=tk.Button(root, image = photoimage5, command=lambda: Music.play_next_song(),compound = LEFT)

photoimage2 = PhotoImage(file = "C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project/play.gif").subsample(5, 5)
play_button=tk.Button(root, image = photoimage2, command=lambda: Music.play_song(),compound = LEFT)

photoimage3 = PhotoImage(file = "C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project/pause.gif").subsample(6, 6)
pause_button=tk.Button(root, image = photoimage3, command=lambda: Music.pause_song(),compound = LEFT)

photoimage4 = PhotoImage(file = "C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project/stop.gif").subsample(6, 6)
stop_button=tk.Button(root, image = photoimage4, command=lambda: Music.stop_song(),compound = LEFT)

photoimage1 = PhotoImage(file = "C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project/add.gif").subsample(5, 5)
add_song_btn=tk.Button(root, image = photoimage1,command=lambda: Music.add_song(),compound = LEFT)

photoimage7 = PhotoImage(file = "C:\\Users\\Anmol\\Desktop\\Data Structures\\mini_project/del.gif").subsample(5, 5)
del_song_btn=tk.Button(root, image = photoimage7,command=lambda: Music.delete(),compound = LEFT)


#volume button
v1 = DoubleVar()
scale=tk.Scale(root,bg='#A1A1A1',bd=1, from_=0, to=100,command='HORIZONTAL',troughcolor='green',label='Volume',variable=v1)
b1 = Button(root, text ="Set Volume", command =lambda:  Music.set_volume())

add_song_btn.place(relx=0.36,rely=0.5)
previous_button.place(relx=0.18,rely=0.4)
pause_button.place(relx=0.3,rely=0.4)
play_button.place(relx=0.418,rely=0.4)
stop_button.place(relx=0.560,rely=0.4)
next_button.place(relx=0.680,rely=0.4)
del_song_btn.place(relx=0.5,rely=0.5)
scale.place(relx=0.8,rely=0.37)
b1.place(relx=0.8,rely=0.3)
song_playlist.place(relx=0.08,rely=0.6)
song_name.place(relx=0.1,rely=0.1)
artist_name.place(relx=0.25,rely=0.1)

root.protocol("WM_DELETE_WINDOW", lambda: Music.on_closing())
Music.check_event()
root.mainloop()
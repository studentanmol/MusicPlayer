# MusicPlayer
HyperSonic Music Player using Pyton tkinter and DLL Data Structure

### Doubly Linked List
A class is created for DLL where each node stores some data, a next and an previous pointer. The DLL is used to store the songs in the playlist. The class of doublylinkedlist contains the following functions:
* insert() which inserts a new node in the DLL.
* delete() which deletes a node from the DLL.
* display() which prints the nodes of the DLL.

### pygame module
The pygame module is used to play the songs from the users device.

### tkinter module
This module is used to create an interactive GUI for the user to view and use to play songs.

### genius API
A genius API is used to get infor for each song using only song name. The artist name,thumbnail photo for the song and other information is used from this API. It downloads the thumbnail in the users file, but after the GUI is closed the photos are automatically deleted.

### player class
The player class will store the functionality available for each song in the playlist. A global variable is used to store the header of the Doubly linked list. The functions in this class are:
* get_info() function is used to get the artists name and thumbnail photo for the song being played using genius API. The info is placed in the tkinter GUI for the user to view.
* add_song() function adds a new song from the users file to the current playlist. User cna select one or more songs to add at a time.
* play_song() function plays either the selected song or the next song in the playlist using pygame module.
* check_event() function checks if the song being played has ended and if that is the case it plays the next song in the playlist.
* stop_song() function stops the current song being played.
* pause_song() function pauses and unpauses the song being played.
* play_next_song() function plays the next song in the playlist. If the last song is being played then it circles back to the first song.
* play_previous_song() function plays the previous song in the playlist. If the first song is being played, it plays the last song.
* set_volume() function allows the user to set the volume of the song using a horizontal scale in GUI.
* on_closing() function deletes the thumbnail photos downloaded in the users file by genius , when the application is closed.
* delete() function deletes the selected song or the currently playing song from the playlist.

##### The rest of the code consists of how the GUI would look and where each of the buttons would be placed and what their function would be.

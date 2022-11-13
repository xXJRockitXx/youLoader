#!/usr/bin/python3
from __future__ import unicode_literals
import os
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter.filedialog import askdirectory
from threading import *

def app_config(app, width, height):
    app.geometry("%dx%d" % (width, height))
    app.configure(background="#404258")
    tk.Wm.wm_title(app, "YouLoader")

""" Creating the app and configs """
app = tk.Tk()
width= app.winfo_screenwidth()
height= app.winfo_screenheight()
app_config(app, width, height)

link = tk.StringVar()
stop_event = Event()
songCounter = 0
lblPath = tk.Label()

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def restart():
    """ Kills the whole application and starts a fresh one """
    global app
    app.destroy()
    app = tk.Tk()
    app_config(app, width, height)
    app.mainloop()


def my_hook(d):
    """ In this label we're show a counter with the downloaded songs """
    global songCounter
    
    if d['status'] == 'finished':
        songCounter += 1
        lblCounter = create_label(app, "Downloads Completed: " + str(songCounter) + 
                              "\nPlease wait Please wait until \"Done!\"", "Arial 18", "#404258", "white", "flat", "left")
        lblCounter.place(x=20, y=width * 0.18)


def download_directory():
    """ We're gonna "Open" dialog box and return the 
    path to the selected file """
    global lblPath
    lblPath.destroy()
    filename = askdirectory()
    global path
    path = filename
    
    lblPath = create_label(app, "Your song will be here: \n" + filename, "Arial 15", "#404258", "white", "flat", "left")
    lblPath.place(x=20, y=width * 0.11)
    
    """ Once we have the directory we can start the download """
    btnDownload.place(x=20, y=width * 0.15)
    
    
def download():
    """ Reset the counter """
    global lblComplete
    global songCounter
    songCounter = 0
    btnRestart.place_forget()
    lblComplete.destroy()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'writethumbnail': True,
        'outtmpl': path + '/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
        'addmetadata':True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'EmbedThumbnail',
        }, {
            'key': 'FFmpegMetadata',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
           
    lblCounter = create_label(app, "Downloads Completed: " + str(songCounter) + 
                              "\nPlease wait Please wait until \"Done!\"", "Arial 18", "#404258", "white", "flat", "left")
    lblCounter.place(x=20, y=width * 0.18)
        
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([link.get()])
                    
    lblComplete = create_label(app, "Done!", "Arial 18", "#404258", "white", "flat", "left")
    lblComplete.place(x=20, y=width * 0.23)


def task():
    """ This thread for the downloads, so the GUI doesn't freeze """
    downloadThread = Thread(target=download, name="Download")
    downloadThread.start()


def create_label(app, textValue, fontValue, background, foreground, rel, align):
    """ Creates a new Label """
    lbl = tk.Label(app,
                    text=textValue,
                    textvariable=textValue,
                    fg=foreground,
                    relief=rel,
                    font=(fontValue),
                    justify=align,
                    bg=background)
    
    return lbl


def create_entry(app, background, foreground, rel, variable, wth):
    """ Creates a new Entry """
    ent = tk.Entry(app, 
                    bg=background,
                    fg=foreground,
                    relief=rel,
                    textvariable=variable,
                    width= wth)
    
    return ent

def create_button(app, textValue, fontValue, background, foreground, comm, rel):
    """ Creates a new Button """
    button = tk.Button(app, 
                        text=textValue, 
                        font=(fontValue), 
                        bg=background,
                        fg=foreground,
                        command= comm,
                        relief=rel)
    
    return button


""" In this label we're gonna show the instructions """
lblInstructions = create_label(app, "Insert the link of a song or playlist:", "Arial 18", "#404258", "white", "flat", "left")
lblInstructions.place(x=20, y=5)

""" With this label, we will notify the download complete """
lblComplete = create_label(app, "Done!", "Arial 18", "#404258", "white", "flat", "left")

""" This entry for the link of the song or playlist """
entLink = create_entry(app, "#6B728E", "white", "flat", link, 100)
entLink.place(height=30,x=20, y=width * 0.03)

""" This button for choosing the download directory """
btnDirectory = create_button(app, "Choose\nDirectory", "Courier 14", "#50577A", "white", download_directory, "flat")
btnDirectory.place(x=20, y=width * 0.06)

""" This button for start the download """
btnDownload = create_button(app, "Download", "Courier 14", "#50577A", "white", task, "flat")

""" This button for restart the app """
btnRestart = create_button(app, "New\nDownload", "Courier 14", "#50577A", "white", restart, "flat")

app.mainloop()
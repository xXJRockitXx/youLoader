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

""" We init the app and configure """
app = tk.Tk()
width= app.winfo_screenwidth()
height= app.winfo_screenheight()
app_config(app, width, height)

link = tk.StringVar()
stop_event = Event()
songCounter = 0

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
    
    lblCounter = tk.Label(app,
                            text="Downloads Completed: "+ str(songCounter + 1),
                            textvariable="Downloads Completed: " + str(songCounter + 1),
                            fg="white",
                            relief="flat",
                            font=('Arial 18'),
                            bg="#404258")
    
    if d['status'] == 'finished':
        songCounter += 1
        print('Download complete, converting ...' + str(songCounter)) 
        lblCounter.place(x=20, y=width * 0.18)


def download_directory():
    """ We're gonna "Open" dialog box and return the 
    path to the selected file """
    filename = askdirectory()
    global path
    path = filename
    
    lblPath = tk.Label(app,
                    text="Your song will be here: \n" + filename,
                    textvariable="Your song will be here: \n" + filename,
                    fg="white",
                    relief="flat",
                    justify="left",
                    font=('Arial 15'),
                    bg="#404258")
    
    lblPath.place(x=20, y=width * 0.11)
    """ Once we have the directory we can start the download """
    btnDownload.place(x=20, y=width * 0.15)
    
    
def download(event):
    """ Reset the counter """
    global songCounter
    songCounter = 0
    
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
    
    """ Starts downloading """
    while not event.is_set():    
        lblCounter.place(x=20, y=width * 0.18)
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link.get()])
            
        stop_event.set()
        
    btnRestart.place(x=20, y=width * 0.21)


def task():
    global downloadThread
    downloadThread = Thread(target=download, args=(stop_event,), daemon=True, name="Download")
    downloadThread.start()
    
""" In this label we're gonna show the instructions """
lblInstructions = tk.Label(app,
                            text="Insert the link of a song or playlist:",
                            fg="white",
                            relief="flat",
                            font=('Arial 18'),
                            bg="#404258")

lblInstructions.place(x=20, y=5)


lblCounter = tk.Label(app,
                        text="Downloads Completed: "+ str(songCounter),
                        textvariable="Downloads Completed: " + str(songCounter),
                        fg="white",
                        relief="flat",
                        font=('Arial 18'),
                        bg="#404258")


""" This entry for the link of the song or playlist """
entLink = tk.Entry(app, 
                    bg="#6B728E",
                    fg="white",
                    relief="flat",
                    textvariable=link,
                    width= 100)

entLink.place(height=30,x=20, y=width * 0.03)


""" This button for choosing the download directory """
btnDirectory = tk.Button(app, 
          text="Choose\nDirectory", 
          font=("Courier", 14), 
          bg="#50577A",
          fg="white",
          command= download_directory,
          relief="flat")
btnDirectory.place(x=20, y=width * 0.06)


""" This button for start the download """
btnDownload = tk.Button(app, 
          text="Download", 
          font=("Courier", 14), 
          bg="#50577A",
          fg="white",
          command= task,
          relief="flat")

""" This button for restart the app """
btnRestart = tk.Button(app, 
          text="New\nDownload", 
          font=("Courier", 14), 
          bg="#50577A",
          fg="white",
          command= restart,
          relief="flat")

app.mainloop()
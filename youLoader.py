#!/usr/bin/python3
from __future__ import unicode_literals
import os
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter.filedialog import askdirectory

class MyLogger(object):

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Descarga completa, convirtiendo ...') 


ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
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

app = tk.Tk()
link = tk.StringVar()
filename = ""

width= app.winfo_screenwidth()
height= app.winfo_screenheight()
app.geometry("%dx%d" % (width, height))
app.configure(background="#404258")
tk.Wm.wm_title(app, "YouLoader")

def download_directory():
    """ We're gonna "Open" dialog box and return the 
    path to the selected file """
    filename = askdirectory()
    
    lblPath = tk.Label(app,
                    text="Your song will be here: \n" + filename,
                    textvariable="Your song will be here: \n" + filename,
                    fg="white",
                    relief="flat",
                    justify="left",
                    font=('Arial 15'),
                    bg="#404258")
    
    lblPath.place(x=20, y=200)
    
    
""" In this label we're gonna show the instructions """
lblInstructions = tk.Label(app,
                            text="Insert the link of a song or playlist:",
                            fg="white",
                            relief="flat",
                            font=('Arial 18'),
                            bg="#404258")

lblInstructions.place(x=20, y=5)

""" This entry for the link of the song or playlist """
lblLink = tk.Entry(app, 
                    bg="#6B728E",
                    fg="white",
                    relief="flat",
                    width= 100)

lblLink.place(height=30,x=20, y=width * 0.03)

""" This button for choosing the download directory """
btnDirectory = tk.Button(app, 
          text="Choose\nDirectory", 
          font=("Courier", 14), 
          bg="#50577A",
          fg="white",
          command= download_directory,
          relief="flat")
btnDirectory.place(x=20, y=width * 0.06)


app.mainloop()
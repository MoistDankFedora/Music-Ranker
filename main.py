from tkinter import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkcap
import os
import time
import sys
a=0
x=0
trackslabel = None

trackslabel_list = []
def save():
    global albumname
    current_directory = os.getcwd()
    print(current_directory)
    if 'Songs Ranked Folder' in os.listdir(current_directory):
        
        cap = tkcap.CAP(root)
        cap.capture(f'{current_directory}\\Songs Ranked Folder\\{albumname} UNFINISHED.png')
    else:
        print('not here')
        os.mkdir(f'{current_directory}\\Songs Ranked Folder')
        cap = tkcap.CAP(root)
        cap.capture(f'{current_directory}\\Songs Ranked Folder\\{albumname} UNFINISHED.png')
def checksize():
    global trackslabel
    if int(root.winfo_width()) <= 500:
        for label in trackslabel_list:
            label.configure(font=('Arial',8,'bold'))
        entry.configure(width=12,font=('Arial',10,'bold'))
        save.grid(column=4,row=3)
    if int(root.winfo_width()) <= 300:
        for label in trackslabel_list:
            label.configure(font=('Arial',6,'bold'))
    
    root.after(1000,checksize)


def next(*event):
    global artistname
    global albumname
    global a
    global x
    score = entry.get()
    entry.delete(0,END)
    label.config(text=f'{a+1}')
    if a < 1:
        score = ''
    

    scorelabel = Label(root,text=f'{score}/100   .({a})',
                       font=('Arial',12,'bold'),
                       bg='#121212',
                       fg='white')
    scorelabel.grid(column=1,row=a+3)

    if a<1:
        score = -1
    if score == -1:
        pass
    elif int(score)>=70:
        scorelabel.config(bg='green',fg='white')
    elif int(score)<70:
        scorelabel.config(bg='red',fg='white')
    
        
    print(score)
    a+=1
    print(f'x:{x} a:{a-1} ')

    

    if a-1 == x:
        print('finish')
        finish = Label(root,
                       text='Done!',
                       font=('Arial',24,'bold'),
                       bg='#121212')
        finish.grid(column=2,row=4)
        current_directory = os.getcwd()
        print(current_directory)
        if 'Songs Ranked Folder' in os.listdir(current_directory):
        
            cap = tkcap.CAP(root)
            cap.capture(f'{current_directory}\\Songs Ranked Folder\\{albumname}.png')
        else:
            print('not here')
            os.mkdir(f'{current_directory}\\Songs Ranked Folder')
            cap = tkcap.CAP(root)
            cap.capture(f'{current_directory}\\Songs Ranked Folder\\{albumname}.png')
        time.sleep(5)
        sys.exit()
    print(a)
def spotifygettracklist(artistname,albumname):
    global trackslabel
    global x
    
    client_id = "818f61a36702452ba9581054ab55780b"
    client_secret = "ceb73b20093c412a85abe955444c0827"
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    
    artist_name = artistname
    album_name = albumname

    
    results = sp.search(q=artist_name, type="artist")
    artist_id = results["artists"]["items"][0]["id"]

  
    results = sp.search(q=album_name, type="album")
    album_id = results["albums"]["items"][0]["id"]

    
    results = sp.album_tracks(album_id)
    tracks = results["items"]
   
    
    print(f"Tracklist of {album_name} by {artist_name}:")
    for i, track in enumerate(tracks):
        
        print(f"{i+1}. {(track['name'].split('feat.'))[0]}")
        trackslabel=Label(root,text=f'{i+1}. {(track["name"].split("feat."))[0]}',
                          font=('Arial',10,'bold'),
                          bg='#121212',
                          fg='white',
                          anchor='w')
        trackslabel.grid(column=0,row=i+4)
        trackslabel_list.append(trackslabel)
    x = i+1   
    root.geometry(f'750x{(len(trackslabel_list)*28+30)}')
    submit.config(command=next)
    root.bind('<Return>',next)
    next()
def submit1(*event):
    global artistname
    global albumname
    names = entry.get()
    splitnames = names.split(sep=':')
    artistnamelabel = Label(root,text=f'{splitnames[1].capitalize()}',
                            font=('Arial',12,'bold')
                            ,bg='#121212',
                            fg='dark gray')
    artistnamelabel.grid(column=2,row=2)
    albumnamelabel = Label(root,text=f'{splitnames[0].capitalize()}',
                           font=('Arial',
                                 16,
                                 'bold')
                                 ,bg='#121212',
                                 fg='dark gray')
    albumnamelabel.grid(column=0,row=2)
    artistname=splitnames[1]
    albumname=splitnames[0]
    spotifygettracklist(artistname,albumname)
    print(albumname,artistname)
root = Tk()
root.config(bg='#121212')
root.title('Music Ranker')
try:
    root.iconbitmap('musicicon.ico')
except Exception:
    pass
root.geometry('700x200')

root.after(1000,checksize)
Label(root,text='',bg='#121212').grid(row=0,column=0)
label = Label(root,
              font=('Gotham'
                    ,12),
                    text='Album Name\n And \nArtist (seperated by :  )',
                    bg='#202020',
                    relief='groove',
                    fg='white')
label.grid(column=0,row=1)
entry = Entry(root,
              font=('Arial'
                    ,24,
                    'bold'),
                    width=20)
entry.grid(column=2,row=1)
Label(root,text='       ',bg='#121212').grid(column=1,row=1)
Label(root,text='  ',bg='#121212').grid(column=3,row=1)
submit = Button(root,
                text='Submit',
                command=submit1)
submit.grid(column=4,row=1)
Label(root,text='    ',bg='#121212').grid(column=5,row=1)
save = Button(root,
                text='Save',
                command=save)
save.grid(column=6,row=1)

root.bind('<Return>',submit1)
root.mainloop()

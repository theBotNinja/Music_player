import pygame,os
from PIL import ImageTk, Image
from ttkthemes import themed_tk as th
import tkinter as tk
from tkinter import simpledialog
from random import choice
from threading import Thread
from tinytag import TinyTag
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from time import sleep

pygame.init()

#constant
color=["red","green","blue","pink","yellow","lime","light blue","gold","orange"]
Thread_stoper=False
playlist_index=0
length=0
playlist=[]
music_lis=[]
lis_box=[]
paused=False
index=0
mid_frame_bg="black"
cwdir=""
app_path=os.getcwd()
os.chdir(app_path)



with open("playlists.txt","r") as f:
    text=f.readlines()
    for i in text:
        playlist.append(i.strip("\n"))


#function


def remove_TO():
    i=playlist[playlist_index]
    playlist.remove(i)
    lisx.delete(playlist_index)
    with open("playlists.txt","w") as f:
        for i in playlist:
            print(i,file=f)



def add_TO():
    if lis_box[index] not in playlist:
        playlist.append(lis_box[index])
        with open("playlists.txt","a") as f:
            print(cwdir+"\\"+lis_box[index],file=f)
        lisx.insert("end",lis_box[index])
    

def player(song):
    global Thread_stoper
    load_song(song)
    Thread_stoper=True
    sleep(1)
    Thread_stoper=False
    t1=Thread(target=current_time)
    t1.start()
    pos["value"]=0
    pygame.mixer_music.play()
    
def load_song(music):
    try:
        pygame.mixer_music.load(music)
        show_song_detail(music)
    except:
        print(Exception)
        messagebox.showinfo("""Error""","could not load song ...")

def show_song_detail(filename):
    global length
    detail=(TinyTag.get(filename))
    length=detail.duration
    mint=int(length//60)
    sec=int(length%60)
    totaltime='{:02d}:{:02d}'.format(mint,sec)
    m["text"]=detail.title
    time["text"]="Song Durtion :"+str(totaltime)
    alb["text"]="Album : "+str(detail.album)
    art["text"]="Artist : "+str(detail.artist)
    bit["text"]="Bit Rate : "+str(detail.bitrate)
    colour_changer()


def select_song(event):
    global index,music_lis
    if len(listbox.curselection()) != 0 :
        index=listbox.curselection()[0]
        player(lis_box[index])
        music_lis=lis_box


def select_playlist_song(event):
    global playlist_index,music_lis
    if len(lisx.curselection())!=0:
        playlist_index=lisx.curselection()[0]
        player(playlist[playlist_index])
        music_lis=playlist
    

def search_file():
    global file_path,cwdir,music_lis,lis_box
    music_lis=[]
    cwdir=file_path.get()
    got_file=False
    if file_path!="":
        try:
            os.chdir(file_path.get())
            got_file=True
        except:
            messagebox.showerror("Error message","could not load file")
            print(Exception)
    if got_file:
        for i in os.listdir():
            if i.find(".mp")!=-1:
                music_lis.append(i)
        for i in music_lis:
            if i not in lis_box:
                lis_box.append(i)
                listbox.insert("end",i)
        music_lis=[]
        

def pause_play():
    global paused
    if paused:
        pp_button["image"]=pause_img
        pygame.mixer_music.unpause()
        paused=False
    else:
        pp_button["image"]=play_img
        pygame.mixer_music.pause()
        paused=True

def forward():
    global index
    index+=1
    player(music_lis[index])

def backward():
    global index
    index-=1
    player(music_lis[index])

def search_folder():
    global file_path
    file=filedialog.askdirectory()
    file_path.set(file)
    search_file()

def set_volume(val):
    val=float(val)//1
    volume=int(val)/100
    pygame.mixer_music.set_volume(volume)

def set_position1():
    val=pygame.mixer_music.get_pos()
    pygame.mixer_music.play(0,(val/1000)-10.0)


def set_position2():
    val=pygame.mixer_music.get_pos()
    pygame.mixer_music.pause()
    pygame.mixer_music.set_pos((val/1000)+10.0)
    pygame.mixer_music.unpause()

def current_time():
    mint=0
    sec=0
    pos["maximum"]=length
    while not Thread_stoper:
        if not paused:
            l=pygame.mixer_music.get_pos()//1000
            mint=int(l//60)
            sec=int(l%60)
            totaltime='{:02d}:{:02d}'.format(mint,sec)
            pos.step()
            Ctime["text"]="Current time :" + totaltime
            sleep(1)
        if length//1==mint*60+sec:
            sleep(2)
            forward()
            break
            

def colour_changer():
    fg=choice(color)
    m["fg"]=fg
    fg=choice(color)
    time["fg"]=fg
    alb["fg"]=fg
    art["fg"]=fg
    bit["fg"]=fg

def stop():
    pygame.mixer_music.stop()
    m["text"]=""
    time["text"]=""
    alb["text"]=""
    art["text"]=""
    bit["text"]=""

def close():
    global Thread_stoper
    Thread_stoper=True
    pygame.mixer_music.stop()
    root.destroy()
    exit()

###font end
root=th.ThemedTk()
root.title("MUSIC")
root.set_theme("arc")
# images
play_img = ImageTk.PhotoImage(Image.open("play.png"))
pause_img = ImageTk.PhotoImage(Image.open("pause.png"))
forward_img = ImageTk.PhotoImage(Image.open("f.png"))
backward_img = ImageTk.PhotoImage(Image.open("b.png"))
secf_img = ImageTk.PhotoImage(Image.open("ff.png"))
secb_img = ImageTk.PhotoImage(Image.open("bb.png"))

#left part
panedwin=ttk.PanedWindow(root,orient=tk.HORIZONTAL)
panedwin.pack(fill=tk.BOTH,expand=True)
frame1=tk.Frame(panedwin,height=900,width=1000)
file_frame=tk.Frame(frame1,borderwidth=10,relief="ridge",bg="white")  #flat, groove, raised, ridge, solid, or sunken

ttk.Label(file_frame,text="Enter the file path to see the music list :").pack(fill="x")
file_path=tk.StringVar()

file_path.set("""D:\\music""")

file_entry=tk.Entry(file_frame,width=75,font="Rockwell",textvariable=file_path)
file_entry.pack(fill=tk.X)
file_entry.update()
ttk.Button(file_frame,text="Search in above given file",command=search_file).pack(fill=tk.X,side=tk.LEFT,expand=True)
ttk.Button(file_frame,text="Browse ...",command=search_folder).pack(fill="x",side=tk.RIGHT)
file_frame.pack(fill=tk.BOTH,side=tk.TOP)

mid_frame=tk.Frame(frame1,width=680,height=600,bg="white")
tk.Label(mid_frame,font="Rockwell",bg="white").pack()
m=tk.Label(mid_frame,text="",font="Rockwell 22",fg="white",bg="white")
m.pack()
tk.Label(mid_frame,font="Rockwell",bg="white").pack()
time=tk.Label(mid_frame,text= "",font="Rockwell 18",fg="black",bg="white")
time.pack()
alb=tk.Label(mid_frame,text= "",font="Rockwell 18",fg="black",bg="white")
alb.pack()
art=tk.Label(mid_frame,text= "",font="Rockwell 18",fg="black",bg="white")
art.pack()
bit=tk.Label(mid_frame,text= "",font="Rockwell 18",fg="black",bg="white")
bit.pack()
tk.Label(mid_frame,font="Rockwell",bg="white").pack()
ttk.Button(mid_frame,text="STOP Playing",command=stop).pack(fill=tk.X,expand=True)
playlist_f=ttk.LabelFrame(mid_frame,text="PLAYLIST")
scroll=ttk.Scrollbar(playlist_f)
scroll.pack(side=tk.RIGHT,fill="y")
lisx=tk.Listbox(playlist_f,yscrollcommand=scroll.set,width=100,bg="white")
lisx.pack(side="top",fill=tk.BOTH,expand=True)
scroll.config(command=lisx.yview)
lisx.bind("<Button-1>",select_playlist_song)
ttk.Button(playlist_f,text="add this song to playlist",command=add_TO).pack(side="left",fill="x",expand=True)
ttk.Button(playlist_f,text="remove song to playlist",command=remove_TO).pack(side="left",fill="x",expand=True)
playlist_f.pack(expand=True,fill=tk.BOTH)
for i in playlist:
    i=i[::-1]
    a=i.find("\\")
    i=i[:a]
    i=i[::-1]
    lisx.insert("end",i)
mid_frame.pack(fill=tk.BOTH,expand=True)

m_frame=tk.Frame(root,bg=mid_frame_bg)
Ctime=tk.LabelFrame(m_frame,text= "",bg=mid_frame_bg,fg="lime",font="fgsd 15")
pos=ttk.Progressbar(Ctime,orient=tk.HORIZONTAL)
pos.pack(fill=tk.X)
Ctime.pack(fill=tk.X)
ttk.Button(m_frame,image=backward_img,command=backward).pack(expand=True,side="left",fill=tk.BOTH)
ttk.Button(m_frame,image=secb_img,command=set_position1).pack(side="left",fill=tk.BOTH)
pp_button=ttk.Button(m_frame,image=pause_img,command=pause_play)
pp_button.pack(expand=True,side="left",fill=tk.BOTH)
ttk.Button(m_frame,image=secf_img,command=set_position2).pack(side="left",fill=tk.BOTH)
ttk.Button(m_frame,image=forward_img,command=forward).pack(expand=True,side="left",fill=tk.BOTH)
ttk.Button(m_frame,text="Colour Changer",command=colour_changer).pack(expand=True,side="left",fill=tk.BOTH)
ttk.Button(m_frame,text="Change Theme",command=lambda : messagebox.showerror("ERROR","This version of app do not have theme changer \n but your can still download dark or light theme \n please contact the devloper")).pack(expand=True,side=tk.LEFT,fill=tk.BOTH)
ttk.Button(m_frame,text="EXIT",command=close).pack(expand=True,side="left",fill=tk.BOTH)
vol_frame = ttk.LabelFrame(m_frame,text="Volume")
vol=ttk.Scale(vol_frame,from_=0,to=100,orient=tk.HORIZONTAL,length=150,command=set_volume)
vol.set(100)
vol.pack(fill=tk.BOTH)
vol_frame.pack(side=tk.RIGHT,fill=tk.Y)
m_frame.pack(fill=tk.BOTH,side=tk.BOTTOM)
frame1.pack(side="left",fill=tk.BOTH,expand=True)

#right part
frame2=tk.Frame(panedwin)
scrollbar=ttk.Scrollbar(frame2)
scrollbar.pack(side=tk.RIGHT,fill="y")
listbox=tk.Listbox(frame2,yscrollcommand=scrollbar.set,width=100,bg="white")
listbox.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
scrollbar.config(command=listbox.yview)
#binding
listbox.bind("<Button-1>",select_song)
frame2.pack(fill=tk.BOTH,expand=True)
panedwin.add(frame1)
panedwin.add(frame2)
root.mainloop()

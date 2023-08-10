import tkinter as tk
import pygame
from tkinter import messagebox
from os import listdir
from PIL import Image,ImageTk
from tkinter import ttk
import ttkthemes as th
from tkinter import filedialog
from tinytag import TinyTag

class Main_app:
    def __init__(self,root):
        pygame.init()
        self.root = root
        self.pauseChecker=True
        self.currentMusicList=[]

    def setupGUI(self):
        

        self.midFrame=tk.Frame(self.root,bg="black")
        self.canvas=tk.Label(self.midFrame,bg="black")
        self.canvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.titleL=tk.Label(self.midFrame,text="title",font="dj 30",fg="white",bg="black")
        self.titleL.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.albL=tk.Label(self.midFrame,text="album",font="dj 20",fg="white",bg="black")
        self.albL.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.artL=tk.Label(self.midFrame,text="art",font="dj 20",fg="white",bg="black")
        self.artL.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.midFrame.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.lowerFrame=tk.Frame(self.root,bg="black")
        self.play_img = ImageTk.PhotoImage(Image.open("play.png"))
        self.pause_img = ImageTk.PhotoImage(Image.open("pause.png"))
        self.forward_img = ImageTk.PhotoImage(Image.open("f.png"))
        self.backward_img = ImageTk.PhotoImage(Image.open("b.png"))
        self.secf_img = ImageTk.PhotoImage(Image.open("ff.png"))
        self.secb_img = ImageTk.PhotoImage(Image.open("bb.png"))

        self.musicListBox = ttk.Combobox(self.lowerFrame)
        self.musicListBox.pack(side=tk.TOP,fill=tk.X)
        self.musicListBox.bind("<<ComboboxSelected>>",self.select_song) 
        
        self.Ctime=tk.LabelFrame(self.lowerFrame,text= "",fg="lime",font="fgsd 15",height=150)
        self.pos=ttk.Progressbar(self.Ctime,orient=tk.HORIZONTAL)
        self.pos.pack(fill=tk.X)
        self.Ctime.pack(fill=tk.X)
        ttk.Button(self.lowerFrame,image=self.backward_img).pack(expand=True,side="left",fill=tk.BOTH)
        ttk.Button(self.lowerFrame,image=self.secb_img).pack(side="left",fill=tk.BOTH)
        self.pp_button=ttk.Button(self.lowerFrame,image=self.pause_img,command=self.pause_play)
        self.pp_button.pack(expand=True,side="left",fill=tk.BOTH)
        ttk.Button(self.lowerFrame,image=self.secf_img).pack(side="left",fill=tk.BOTH)
        ttk.Button(self.lowerFrame,image=self.forward_img).pack(expand=True,side="left",fill=tk.BOTH)
        ttk.Button(self.lowerFrame,text="Colour Changer").pack(side="left",fill=tk.BOTH)
        ttk.Button(self.lowerFrame,text="EXIT").pack(expand=True,side="left",fill=tk.BOTH)
        self.vol_frame = ttk.LabelFrame(self.lowerFrame,text="Volume")
        self.vol=ttk.Scale(self.vol_frame,from_=0,to=100,orient=tk.HORIZONTAL,length=150)
        self.vol.set(100)
        self.vol.pack(fill=tk.BOTH)
        self.vol_frame.pack(side=tk.RIGHT,fill=tk.Y)
        self.lowerFrame.pack(side=tk.BOTTOM,fill=tk.X)


        self.menu = tk.Menu(self.root,bg="black")
        self.menu1= tk.Menu(self.menu,tearoff=0)
        self.menu1.add_command(label="Give File",command=self.openFile)
        self.menu1.add_command(label="Give Music File")
        self.menu.add_cascade(label="File",menu=self.menu1)
        self.menu.add_command(label="Exit",command=lambda : self.root.destroy())
        self.root.config(menu=self.menu)

        self.root.bind("<Any-KeyPress>",self.themechanger)

    def themechanger(self,event):
        if event.keycode==68:
            self.canvas["bg"]="black"
            self.albL["fg"]="white"
            self.artL["fg"]="white"
            self.titleL["fg"]="white"
            self.albL["bg"]="black"
            self.artL["bg"]="black"
            self.titleL["bg"]="black"
            self.root.set_theme("black")
        elif event.keycode==76:
            self.albL["fg"]="black"
            self.artL["fg"]="black"
            self.titleL["fg"]="black"
            self.canvas["bg"]="white"
            self.albL["bg"]="white"
            self.artL["bg"]="white"
            self.titleL["bg"]="white"
            self.root.set_theme("arc")

    def pause_play(self):
        if not self.pauseChecker:
            self.pp_button["image"]=self.play_img
            pygame.mixer_music.pause()
            self.pauseChecker=not self.pauseChecker
        else:
            self.pp_button["image"]=self.pause_img
            pygame.mixer_music.unpause()
            self.pauseChecker=not self.pauseChecker
        

    def openFile(self):
        self.path=filedialog.askdirectory()
        path=self.path
        if path != (None or "") :
            self.currentMusicList.clear()
            for i in listdir(path):
                if i.find(".mp") != -1:
                    self.currentMusicList.append(i)
            self.musicListBox["values"]=self.currentMusicList

    def select_song(self,event):
        self.musicplayer(self.path+"/"+self.musicListBox.get())

    def musicplayer(self,song):
        self.load_song(song)
        Thread_stoper=True
        # sleep(1)
        Thread_stoper=False
        # t1=Thread(target=current_time)
        # t1.start()
        # pos["value"]=0
        pygame.mixer_music.play()

    def load_song(self,music):
        try:
            pygame.mixer_music.load(music)
        except:
            print(Exception)
            messagebox.showinfo("""Error""","could not load song ...")
        self.show_song_detail(music)

    def show_song_detail(self,filename):
        self.detail=(TinyTag.get(filename,image=True))
        print(self.detail)
        try:
            if self.detail.get_image() != None:
                with open("D:\\img.jpeg","wb") as f:
                    f.write(self.detail.get_image())
                self.cover = ImageTk.PhotoImage(Image.open(".\\cover\\img.jpeg"))
                self.canvas["image"]=self.cover
        except :
            self.cover = ImageTk.PhotoImage(Image.open("bitmap.png"))
            self.canvas["image"]=self.cover
        print(self.detail.duration)
        
        # mint=int(length//60)
        # sec=int(length%60)
        # totaltime='{:02d}:{:02d}'.format(mint,sec)
        self.titleL["text"]=self.detail.title
        self.albL["text"]="Album : "+str(self.detail.album)
        self.artL["text"]="Artist : "+str(self.detail.artist)

        

if __name__ == "__main__":
    root=th.ThemedTk()
    root.set_theme("equilux")
    root.maxsize(800,600)
    root.geometry("800x600")
    abc = Main_app(root)
    abc.setupGUI()
    root.mainloop()

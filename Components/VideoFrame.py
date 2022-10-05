from ctypes import alignment
from tkinter import *
from tkinter import ttk



class VideoFrame:
    def __init__(self,parent):
        self.__parent = ttk.Frame(parent)
        self.__header = ttk.Label(self.__parent)

        self.__data_frame = ttk.Frame(self.__parent)
        self.__video_title = ttk.Label(self.__data_frame)
        self.__video_channel_url = ttk.Label(self.__data_frame)
        self.__video_length = ttk.Label(self.__data_frame)
        self.__video_author = ttk.Label(self.__data_frame)

        self.__setWidgets()


    def __setWidgets(self):
        
        label_style = ttk.Style()
        label_style.configure("Video.TLabel",font='Ubuntu 12') 

        self.__parent.columnconfigure(0,weight=1)
        self.__parent.configure(borderwidth=2,relief="groove")
        self.__header.configure(font="Ubuntu 16",text="Current Video")



        self.__data_frame.configure(padding=8)



        self.__video_title.configure(style="Video.TLabel",text="Title")
        self.__video_channel_url.configure(style='Video.TLabel',text="Channel URL")
        self.__video_length.configure(style='Video.TLabel',text="Duration")
        self.__video_author.configure(style='Video.TLabel',text="Author")

    def placeWidgets(self):
        self.__parent.grid(row=0,column=0,sticky=(N,E,W),columnspan=2)

        self.__header.grid(row=0,column=0,padx=5,pady=5)

        self.__data_frame.grid(row=1,column=0,sticky=(W,E))
        self.__video_title.grid(row=0,column=0,sticky=W)
        self.__video_channel_url.grid(row=1,column=0,sticky=W)
        self.__video_length.grid(row=2,column=0,sticky=W)
        self.__video_author.grid(row=3,column=0,sticky=W)


    @property
    def Title(self):
        return self.__video_title

    @property 
    def ChannelUrl(self):
        return self.__video_channel_url
    @property 
    def  Length(self):
        return self.__video_length
    @property
    def Autor(self):
        return self.__video_author

    @property
    def Parent(self):
        return self.__parent
from tkinter import * 

from tkinter import ttk 


class StreamFrame:
    def __init__(self,parent):
        self.__parent = ttk.Frame(parent)

        self.__stream_format = ttk.Label(self.__parent)
        self.__stream_size = ttk.Label(self.__parent)
        self.__stream_quality = ttk.Label(self.__parent)

        self.__download_button = ttk.Button(self.__parent)


        self.__stream_progress_bar_frame = ttk.Frame(self.__parent)

        self.__stream_progress = ttk.Label(self.__stream_progress_bar_frame)

        self.__stream_progress_bar = ttk.Progressbar(self.__stream_progress_bar_frame)
        self.__setStreamFrame()
        



    def __setStreamFrame(self):
        self.__parent.rowconfigure(0,weight=1)
        self.__parent.columnconfigure(0,weight=1)
        self.__parent.configure(padding=8)

        self.__stream_format.configure(font='Ubuntu 11',text="Hola")
        self.__stream_size.configure(font='Ubuntu 11',text="Hola")
        self.__stream_quality.configure(font="Ubuntu 11",text="Hola")

        self.__download_button.configure(text="Download")


        self.__stream_progress_bar_frame.columnconfigure(0,weight=1)
        self.__stream_progress_bar_frame.rowconfigure(0,weight=1)
        self.__stream_progress_bar.configure(maximum=101,length=100,mode="determinate",orient=HORIZONTAL)


    def placeStream(self,row,column):

        self.__parent.grid(row=row,column=column,padx=10,pady=10,sticky=(E,W))

        self.__stream_format.grid(row=0,column=0,sticky=W)
        self.__stream_size.grid(row=1,column=0,sticky=W)
        self.__stream_quality.grid(row=2,column=0,sticky=W)

        self.__download_button.grid(row=3,column=0,sticky=(W,E),pady=8)

        self.__stream_progress_bar_frame.grid(row=4,column=0,padx=10,pady=0,sticky=(E,W))
        self.__stream_progress.grid(row=0,column=0,sticky=(E,W))
        self.__stream_progress_bar.grid(row=1,column=0,sticky=(E,W))


    @property
    def Format(self):
        return self.__stream_format
    @property
    def Size(self):
        return self.__stream_size

    @property 
    def Quality(self):
        return self.__stream_quality

    @property
    def DownloadButton(self):
        return self.__download_button
    @property 
    def ProgressBar(self):
        return self.__stream_progress_bar
    @property
    def ProgressBarLabel(self):
        return self.__stream_progress   

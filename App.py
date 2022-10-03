from threading import Thread
from tkinter import *
from tkinter import ttk
from xmlrpc.client import Boolean

from pytube import YouTube

from utils import convertToMb

from functools import partial




#dark color : #161925


#todo: Add scrollbar to canvas frame, add checkboxes to filter data. (audio,video,audio/video)

URL = "https://www.youtube.com/watch?v=d6WoNmDzNCM&list=RD_PEe6TP1kCc&index=2"
class App:

    __dark_color = "#161925"

    __mainWindow = Tk()



    __youtube_icon = None


    #Top container and it's widgets
    __search_url_var = StringVar()
    __search_video_filter = StringVar()


    __search_url_frame = ttk.Frame(__mainWindow)

    __search_url_widgets_frame = ttk.Frame(__search_url_frame)
    __search_url_label = ttk.Label(__search_url_widgets_frame)
    __search_url_entry = ttk.Entry(__search_url_widgets_frame,textvariable=__search_url_var)
    __search_url_button = ttk.Button(__search_url_widgets_frame)

    __search_radio_button_frame = ttk.Frame(__search_url_frame)
    __search_video_only_filter_radio_button = ttk.Radiobutton(__search_radio_button_frame,text="Video Only",variable=__search_video_filter,value="Video")
    __search_audio_only_filter_radio_button = ttk.Radiobutton(__search_radio_button_frame,text="Audio Only",variable=__search_video_filter,value="Audio")
    __search__progressive_filter_radio_button = ttk.Radiobutton(__search_radio_button_frame,text="Video/Audio",variable=__search_video_filter,value="Progressive")
    

    __search_response_label = ttk.Label(__search_url_widgets_frame)


    #Bottom container and it's widgets

    __bottom_frame = ttk.Frame(__mainWindow)

    __information_frame = ttk.Frame(__bottom_frame)
    __information_frame_label = ttk.Label(__information_frame)

    __video_data_frame = ttk.Frame(__information_frame,borderwidth=4,relief='groove')
    __default_icon_label = ttk.Label(__video_data_frame)
    __video_title_label = ttk.Label(__video_data_frame)
    __video_channel_url_label = ttk.Label(__video_data_frame)
    __video_length_label = ttk.Label(__video_data_frame)
    __video_author_label = ttk.Label(__video_data_frame)


    #Canva frame for showing download options streams

    __canva_frame = Canvas(__bottom_frame)

    #application status

    __searching_status = False

    #dict to manage the streams
    __current_streams = {}

    #status
    __activeDownloads = False

    def __init__(self):
        self.__setMainWindow()
        self.__setSearchUrlFrame()
        self.__setBottomFrame()


        


    def __setMainWindow(self):
        self.__mainWindow.title("Youtube Downloader")
        self.__mainWindow.geometry("1024x768")

        self.__mainWindow.configure(background=self.__dark_color)
        #self.__mainWindow.resizable(0,0)

        self.__mainWindow.columnconfigure(0,weight=1)
        self.__mainWindow.rowconfigure(1,weight=1)





    def __setSearchUrlFrame(self):

        #setting the frame itself
        self.__search_url_frame.configure(padding=20)
        self.__search_url_frame.columnconfigure(0,weight=1)
        self.__search_url_frame.rowconfigure(0,weight=1)

        self.__search_url_frame.grid(row=0,column=0,sticky=(W,E))


        #setting the widgets associate to that frame
        self.__search_url_widgets_frame.grid(row=0,column=0)
        

        self.__search_url_label.configure(text="Insert URL",font="Ubuntu")
        self.__search_url_label.grid(row=0,column=0,sticky=(W))


        self.__search_url_entry.configure(width=50)
        self.__search_url_entry.grid(row=1,column=0)
        
        
        self.__search_url_button.configure(width=30,padding=6,command=self.__searchButtonCallBack,text="Search")
        self.__search_url_button.grid(row=2,column=0,padx=8,pady=8)


        self.__search_radio_button_frame.grid(row=3,column=0,pady=(10,0),padx=5)

        self.__search_audio_only_filter_radio_button.grid(row=0,column=0,padx=10)
        self.__search_video_only_filter_radio_button.grid(row=0,column=1,padx=10)
        self.__search__progressive_filter_radio_button.grid(row=0,column=2,padx=10)

    def __searchButtonCallBack(self):
        

        
        #status of the search.
        if self.__search_url_var.get() !=  "":
            if self.__search_video_filter.get() != "":
                if not self.__searching_status:
                    
                    self.__searching_status = True
                    Thread(target=self.__ProcessURL).start()
                else:
                    self.__search_response_label.configure(text="Wait a moment...")
            else:
                self.__search_response_label.configure(text="Select One of the options...")
               
        else:
            self.__search_response_label.configure(text="Invalid Url...")

        self.__search_response_label.grid(row=4,column=0)

    def __ProcessURL(self):
        
        self.__search_response_label.configure(text="Searching...")
        try:
            yt = YouTube(self.__search_url_var.get(),on_progress_callback=self.__onProgressCallBack,on_complete_callback=self.__OnCompleteCallBack)
            self.__search_response_label.configure(text="Loading video data...")
            self.__setCurrentVideoFrame(yt)
            self.__search_response_label.configure(text="Loading streams...") 

            if(self.__search_video_filter.get() == "Audio"):
                streams = yt.streams.filter(only_audio=True)
            elif(self.__search_video_filter.get() == "Video"):
                streams = yt.streams.filter(only_video=True)
            elif(self.__search_video_filter.get() == "Progressive"):
                streams = yt.streams.filter(progressive=True)
            self.__setStreamFrames(streams)
            
        except Exception as e:
            print(e)
            self.__search_response_label.configure(text="Sorry couldn't find any data, try again.")
        else:
            self.__search_response_label.grid_remove()

        self.__searching_status = False

    

    def __setCurrentVideoFrame(self,data):
        

        #Frame to show the actual video in the bottom-top frame
        self.__information_frame_label.configure(text="Current Video",font="Ubuntu 16")
        

        self.__video_data_frame.configure(padding=8)
        self.__video_data_frame.grid(row=1,column=0,sticky=(W,E))

        label_style = ttk.Style()
        label_style.configure("Video.TLabel",font='Ubuntu 12')       

        self.__video_title_label.configure(text=f"Video title: {data.title}",style='Video.TLabel')
        

        self.__video_channel_url_label.configure(text=f"Channel URL: {data.channel_url}",style='Video.TLabel')
       

        self.__video_length_label.configure(text=f'Duration: {data.length} seg',style='Video.TLabel')
        

        self.__video_author_label.configure(text=f"Author: {data.author}",style='Video.TLabel')
        


        self.__information_frame_label.grid(row=0,column=0,padx=5,pady=5)
        self.__video_title_label.grid(row=0,column=0,sticky=W)
        self.__video_channel_url_label.grid(row=1,column=0,sticky=W)
        self.__video_length_label.grid(row=2,column=0,sticky=W)
        self.__video_author_label.grid(row=3,column=0,sticky=W)

    def __setStreamFrames(self,streams):
        self.__current_streams = {}
        current_row = 0
        current_column = 0
        for stream in streams:
            if current_column == 3:
                current_row+=1
                current_column = 0
            stream_frame = ttk.Frame(self.__canva_frame,padding=8)
            stream_frame.rowconfigure(0,weight=1)
            stream_frame.columnconfigure(0,weight=1)


            if stream.is_progressive:
                stream_format_label = ttk.Label(stream_frame,text="Format: Video/Audio",font="Ubuntu 12")
                stream_quality_label = ttk.Label(stream_frame,text=f"Resolution: {stream.resolution}",font='Ubuntu 12')
            elif stream.includes_audio_track:
                stream_format_label = ttk.Label(stream_frame,text="Format: Audio Only ",font="Ubuntu 12")
                stream_quality_label = ttk.Label(stream_frame,text=f"Abr: {stream.abr}",font='Ubuntu 12')
            elif stream.includes_video_track:
                stream_format_label = ttk.Label(stream_frame,text="Format: Video Only ",font="Ubuntu 12")
                stream_quality_label = ttk.Label(stream_frame,text=f"Resolution: {stream.resolution}",font='Ubuntu 12')

            stream_size_label = ttk.Label(stream_frame,text=f"Size: {convertToMb(stream.filesize)} mb ",font='Ubuntu 12')
            stream_download_button = ttk.Button(stream_frame,text="Download",width=30,command=partial(self.__DownloadButtonCallBack,stream.itag))

           

            
            stream_progress_bar_frame = ttk.Frame(stream_frame)
            stream_progress_bar_frame.columnconfigure(0,weight=1)

            stream_progress_bar_label = ttk.Label(stream_progress_bar_frame,text="Download...")
            stream_progress_bar = ttk.Progressbar(stream_progress_bar_frame,orient=HORIZONTAL,length=200,mode='determinate')

            


            stream_frame.grid(row=current_row,column=current_column,padx=10,pady=10,sticky=(N,E,W))
            stream_format_label.grid(row=0,column=0,sticky=W)
            stream_size_label.grid(row=1,column=0,sticky=W)
            stream_quality_label.grid(row=2,column=0,sticky=W)
            stream_download_button.grid(row=3,column=0,sticky=(N,W,E))
            stream_progress_bar_frame.grid(row=4,column=0,padx=10,pady=(15,0),sticky=(N,W,E))
            stream_progress_bar_label.grid(row=0,column=0,sticky=(N,W,E))
            stream_progress_bar.grid(row=1,column=0,sticky=(N,W,E))
            
            current_column+=1

            self.__current_streams[stream.itag] = {
                "stream":stream,
                "frame":stream_frame,
                "stream_size_label":stream_size_label,
                "stream_format_label":stream_format_label,
                "stream_download_button":stream_download_button,
                "stream_progress_bar_frame":stream_progress_bar_frame,
                "stream_progress_bar_label":stream_progress_bar_label,
                "stream_progress_bar":stream_progress_bar,
                "previous_progress":0,
                "onDownload":False
            }


    def __setBottomFrame(self):




        bottom_frame_style = ttk.Style()
        bottom_frame_style.configure('Bottom.TFrame',background=self.__dark_color)

        self.__bottom_frame.configure(padding=2,style='Bottom.TFrame')
        self.__bottom_frame.grid(row=1,column=0,sticky=(E,W,S,N))
        self.__bottom_frame.columnconfigure(0,weight=1)
        self.__bottom_frame.rowconfigure(1,weight=1)


        #bottom frame widgets

        """  Information frame  """
        self.__information_frame.columnconfigure(0,weight=1)
        self.__information_frame.grid(row=0,column=0,sticky=(N,E,W))

        

        """ Option canvas container  """

        self.__canva_frame.configure(bg=self.__dark_color)
        self.__canva_frame.columnconfigure(0,weight=1)
        self.__canva_frame.columnconfigure(1,weight=1)
        self.__canva_frame.columnconfigure(2,weight=1)
        self.__canva_frame.grid(row=1,column=0,sticky=(W,E,S,N),padx=1,pady=0)

    

    def __onProgressCallBack(self,stream,data_chunk,bytes_remaining):

        filesize = convertToMb(stream.filesize)
        bm = convertToMb(bytes_remaining)

        downloaded = round(filesize - bm,2)
        percentage = round((100*downloaded)/filesize,2)
        


        previous_progress = self.__current_streams[stream.itag]['previous_progress']
        self.__current_streams[stream.itag]['previous_progress'] = percentage

        step = round(percentage - previous_progress,2)

        self.__current_streams[stream.itag]['stream_progress_bar_label'].configure(text=f"Downloading... {percentage} %")
        self.__current_streams[stream.itag]['stream_progress_bar'].step(step)



    def __OnCompleteCallBack(self,stream,file_path):
        self.__current_streams[stream.itag]['stream_progress_bar_label'].configure(text=f"Download complete...!")
        self.__current_streams[stream.itag]['onDownload'] = False


    def __DownloadButtonCallBack(self,itag):

        if  not self.__current_streams[itag]['onDownload']:
            current_stream = self.__current_streams[itag]['stream']
            self.__current_streams[itag]['stream_progress_bar'].configure(maximum=101)
            self.__current_streams[itag]['stream_progress_bar_label'].configure(text="Downloading... 0.00 %")
            self.__current_streams[itag]['onDownload'] = True
            Thread(target=partial(self.__startDownload,current_stream)).start()

    def __startDownload(self,stream):

        output_filename = str(stream.itag)+"_"+stream.title+"."+stream.mime_type.split("/")[1]
        stream.download(filename=output_filename)    

    
    def run(self):
        self.__mainWindow.mainloop()





app = App()
app.run()
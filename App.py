from threading import Thread
from tkinter import *
from tkinter import ttk
from xmlrpc.client import Boolean

from pytube import YouTube

from utils import convertToMb,dark_color

from functools import partial


from Components.SearchFrame import SearchFrame
from Components.BottomFrame  import BottomFrame
from Components.StreamFrame import StreamFrame

#dark color : #161925


#todo: Add scrollbar to canvas frame, add checkboxes to filter data. (audio,video,audio/video)

#add the option to not search new videos while downloads are still pending,...

URL = "https://www.youtube.com/watch?v=d6WoNmDzNCM&list=RD_PEe6TP1kCc&index=2"
class App:

    
    

    __mainWindow = Tk()

    __search_frame = SearchFrame(__mainWindow)

    
    __bottom = BottomFrame(__mainWindow)





    __searching_status = False

    #dict to manage the streams
    __current_streams = {}

    #status

   

    def __init__(self):
        self.__setMainWindow()
        self.__setSearchFrame()
        self.__setBottom()


        self.__current_streams = {}

        


    def __setMainWindow(self):
        self.__mainWindow.title("Youtube Downloader")
        self.__mainWindow.geometry("1024x768")

        self.__mainWindow.configure(background=dark_color)
        #self.__mainWindow.resizable(0,0)

        self.__mainWindow.columnconfigure(0,weight=1)
        self.__mainWindow.rowconfigure(1,weight=1)

        


    
    def __setSearchFrame(self):


        self.__search_frame.SearchButton.configure(command=self.__searchButtonCallBack)
        self.__search_frame.placeWidgets()

    def __setBottom(self):
        self.__bottom.placeParent()
        

    def __searchButtonCallBack(self):
        
        #status of the search.
        if self.__search_frame.EntryValue !=  "":
            if self.__search_frame.FilterValue != "":
                if not self.__searching_status:
                    self.__searching_status = True
                    Thread(target=self.__ProcessURL).start()
                else:
                    self.__search_frame.setResponse("Wait a moment...")
            else:
                self.__search_frame.setResponse("Select one of the options...")
               
        else:
            self.__search_frame.setResponse("Invalid url...")



    def __ProcessURL(self):
        
        self.__search_frame.setResponse("Searching...")
        try:
            yt = YouTube(
            self.__search_frame.EntryValue,
            on_progress_callback=self.__OnProgress,
            on_complete_callback=self.__OnComplete
            )

            self.__bottom.VideoFrame.Parent.grid_remove()
            self.__bottom.CanvasFrame.Canvas.grid_remove()

            self.__search_frame.setResponse("Loading video data...")


            #self.__setCurrentVideoFrame(yt)
            
            self.__ShowVideoData(yt)
            self.__search_frame.setResponse("Loading streams...")
            

            if(self.__search_frame.FilterValue == "Audio"):
                streams = yt.streams.filter(only_audio=True)
            elif(self.__search_frame.FilterValue == "Video"):
                streams = yt.streams.filter(only_video=True)
            elif(self.__search_frame.FilterValue == "Progressive"):
                streams = yt.streams.filter(progressive=True)

            self.__ListStreams(streams)
            
        except Exception as e:
            print(e)
            self.__search_frame.setResponse("Sorry there has been an error, try again")
        else:
            self.__search_frame.removeResponse()

        self.__searching_status = False
    

    def __ShowVideoData(self,video):
        self.__bottom.VideoFrame.Title.configure(text=f"Title: {video.title}")
        self.__bottom.VideoFrame.ChannelUrl.configure(text=f"Channel URL: {video.channel_url}")
        self.__bottom.VideoFrame.Length.configure(text=f"Duration: {video.length} seg")
        self.__bottom.VideoFrame.Autor.configure(text=f"Author: {video.author}")
        
        self.__bottom.VideoFrame.placeWidgets()
    
    def __ListStreams(self,streams):
        column=0
        row=0
        self.__current_streams = {}
        for stream in streams:
            if column == 3:
                column = 0
                row+=1
            stream_frame = StreamFrame(self.__bottom.CanvasFrame.Canvas)
            if stream.is_progressive:
                stream_frame.Format.configure(text="Format: Video/Audio")
                stream_frame.Quality.configure(text=f"Resolution: {stream.resolution}")
            elif stream.includes_audio_track:
                stream_frame.Format.configure(text="Format: Audio Only")
                stream_frame.Quality.configure(text=f"Abr: {stream.abr}")
            elif stream.includes_video_track:
                stream_frame.Format.configure(text=f"Video Only")
                stream_frame.Quality.configure(text=f"Resolution: {stream.resolution}")

            stream_frame.Size.configure(text=f"Size: {convertToMb(stream.filesize)}mb")
            
            stream_frame.DownloadButton.configure(command=partial(self.__ButtonCallBack,stream))

            stream_frame.placeStream(row,column)
            self.__current_streams[stream.itag] = {"stream":stream,"stream_frame":stream_frame,'previous_progress':0,"OnDownload":False}
            column+=1
        self.__bottom.CanvasFrame.placeCanvas()

    
    
    def __ButtonCallBack(self,stream):
        self.__current_streams[stream.itag]['stream_frame'].ProgressBarLabel.configure(text="Downloading... 0.00%")
        Thread(
            target=partial(
                self.__DownloadFile,
                self.__current_streams[stream.itag]['stream']
            )
        ).start()
        
    def __DownloadFile(self,stream):
        if not self.__current_streams[stream.itag]['OnDownload']:
            try:
                print("Starting download...")
                self.__current_streams[stream.itag]['OnDownload'] = True
                output_filename = str(stream.itag)+"_"+stream.title+"."+stream.mime_type.split("/")[1]
                stream.download(filename=output_filename)
            except Exception as e:
                print(e)
                print('...')
                self.__current_streams[stream.itag]['OnDownload'] = False
            else:
                self.__current_streams[stream.itag]['OnDownload'] = False

    def __OnProgress(self,stream,data_chunk,byte_remaining):
        filesize = convertToMb(stream.filesize)
        bm = convertToMb(byte_remaining)

        downloaded = round(filesize - bm,2)
        percentage = round((100*downloaded)/filesize,2)

        previous_progress = self.__current_streams[stream.itag]['previous_progress']
        self.__current_streams[stream.itag]['previous_progress'] = percentage

        step = round(percentage - previous_progress,2)

        self.__current_streams[stream.itag]['stream_frame'].ProgressBarLabel.configure(text=f"Downloading... {percentage}")
        self.__current_streams[stream.itag]['stream_frame'].ProgressBar.step(step)

    def __OnComplete(self,stream,file_path):
        self.__current_streams[stream.itag]['stream_frame'].ProgressBarLabel.configure(text="Download completed...")
        self.__current_streams[stream.itag]['OnDownload'] = False
        self.__current_streams[stream.itag]['previous_progress'] = 0

 

    
    def run(self):
        self.__mainWindow.mainloop()





app = App()
app.run()
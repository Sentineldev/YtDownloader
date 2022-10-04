from tkinter import * 
from tkinter import ttk



class SearchFrame:
    
    
    
    #__search_filter_variable = StringVar()
    def __init__(self,parentElement):
        self.__search_entry_variable = StringVar()
        self.__search_filter_variable = StringVar()


        self.__search_frame = ttk.Frame(parentElement)


        self.__search_widgets_frame = ttk.Frame(self.__search_frame)

        self.__search_frame_label = ttk.Label(self.__search_widgets_frame)
        self.__search_frame_entry = ttk.Entry(self.__search_widgets_frame)
        self.__search_frame_button = ttk.Button(self.__search_widgets_frame)

        
        self.__search_radio_button_frame = ttk.Frame(self.__search_frame)

        self.__search_audio_only_filter = ttk.Radiobutton(self.__search_radio_button_frame)
        self.__search_video_only_filter = ttk.Radiobutton(self.__search_radio_button_frame)
        self.__search_progressive_filter = ttk.Radiobutton(self.__search_radio_button_frame)


        self.__search_frame_response_label = ttk.Label(self.__search_frame)
        

        self.__setWidgets()



    def __setWidgets(self):


        self.__search_frame.configure(padding=20)
        self.__search_frame.columnconfigure(0,weight=1)


        self.__search_widgets_frame.columnconfigure(0,weight=1)

        self.__search_frame_label.configure(text="Insert URL",font='Ubuntu')
        
        self.__search_frame_entry.configure(width=50,textvariable=self.__search_entry_variable)

        self.__search_frame_button.configure(width=30,padding=6,text="Search")

        self.__search_radio_button_frame.columnconfigure(0,weight=1)

        
        self.__search_audio_only_filter.configure(text="Audio Only",variable=self.__search_filter_variable,value="Audio")
        self.__search_video_only_filter.configure(text="Video Only",variable=self.__search_filter_variable,value="Video")
        self.__search_progressive_filter.configure(text="Audio/Video",variable=self.__search_filter_variable,value="Progressive")


    def placeWidgets(self):

        self.__search_frame.grid(row=0,column=0,sticky=(W,E))

        self.__search_widgets_frame.grid(row=0,column=0)

        self.__search_frame_label.grid(row=0,column=0,sticky=W)

        self.__search_frame_entry.grid(row=1,column=0)

        self.__search_frame_button.grid(row=2,column=0,padx=8,pady=(10,8))

        self.__search_radio_button_frame.grid(row=4,column=0,pady=(10,0),padx=5)

        self.__search_audio_only_filter.grid(row=0,column=0,padx=(0,10))
        self.__search_video_only_filter.grid(row=0,column=1,padx=(0,10))
        self.__search_progressive_filter.grid(row=0,column=2,padx=(0,10))


    def setResponse(self,response:str):
        self.__search_frame_response_label.configure(text=response)
        self.__search_frame_response_label.grid(row=3,column=0)



    def removeResponse(self):
        self.__search_frame_response_label.grid_remove()

    @property
    def SearchButton(self):
        return self.__search_frame_button
    
    @property
    def FilterValue(self):
        return self.__search_filter_variable.get()

    @property
    def EntryValue(self):
        return self.__search_entry_variable.get()


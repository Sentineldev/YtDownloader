from tkinter import *
from tkinter import ttk
from utils import dark_color

from Components.StreamFrame import StreamFrame


class CanvasFrame:
    def __init__(self,parent):
        self.__parent = Canvas(parent)
        self.__scrollBar = ttk.Scrollbar(parent)        

        self.__WidgetFrame = ttk.Frame(self.__parent)

        self.__setCanvas()

        


    def __setCanvas(self):

        frame_style = ttk.Style()

        frame_style.configure("WidgetFrame.TFrame",background=dark_color)


        #setting the canvas config
        self.__parent.configure(
            background=dark_color,
            yscrollcommand=self.__scrollBar.set
        )

        self.__parent.bind("<Configure>",self.__CanvaBind)


        self.__parent.create_window(
            (8,0),
            window=self.__WidgetFrame,
        )

        self.__parent.columnconfigure(0,weight=1)


        #setting the scrollbar config

        self.__scrollBar.configure(orient=VERTICAL,command=self.__parent.yview)


        #setting the widget frame

        self.__WidgetFrame.configure(style="WidgetFrame.TFrame")
        self.__WidgetFrame.columnconfigure(0,weight=1)
        self.__WidgetFrame.columnconfigure(1,weight=1)
        self.__WidgetFrame.columnconfigure(2,weight=1)
      

    def __CanvaBind(self,e):
        self.__WidgetFrame.configure(
            width=self.__parent.winfo_width()-6,
            height=self.__WidgetFrame.winfo_height()
        )
        self.__WidgetFrame.grid_propagate(0)
        self.__parent.configure(scrollregion=self.__parent.bbox('all'))
        

    def placeCanvas(self):
        self.__parent.grid(row=1,column=0,sticky=(N,E,W,S))
        self.__scrollBar.grid(row=1,column=1,sticky=(N,S))



    @property 
    def Canvas(self):
        return self.__parent

    @property
    def WidgetFrame(self):
        return self.__WidgetFrame

        
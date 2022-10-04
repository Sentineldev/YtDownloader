from tkinter import *
from tkinter import ttk
from utils import dark_color

from Components.VideoFrame import VideoFrame
from Components.CanvaFrame import CanvasFrame


class BottomFrame:
    def __init__(self,parent):
        self.__parent = ttk.Frame(parent)
        self.__setParent()
        self.__videoFrame = VideoFrame(self.__parent)
        self.__canvasFrame = CanvasFrame(self.__parent)

    def __setParent(self):

        parent_style = ttk.Style()
        parent_style.configure("Bottom.TFrame",background=dark_color)
        self.__parent.configure(padding=0,style='Bottom.TFrame')

        self.__parent.columnconfigure(0,weight=1)
        self.__parent.rowconfigure(1,weight=1)


    def placeParent(self):
        self.__parent.grid(row=1,column=0,sticky=(N,E,W,S))


    def removeChildsFrames(self):
        self.__videoFrame.Parent.grid_remove()
        self.__canvasFrame.Canvas.grid_remove()


   


    @property
    def CanvasFrame(self):
        return self.__canvasFrame

    @property
    def VideoFrame(self):
        return self.__videoFrame
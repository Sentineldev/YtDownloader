from tkinter import *
from tkinter import ttk
from utils import dark_color

from Components.StreamFrame import StreamFrame


class CanvasFrame:
    def __init__(self,parent):
        self.__parent = Canvas(parent)

        self.__setCanvas()

        


    def __setCanvas(self):
        self.__parent.configure(background=dark_color)
        self.__parent.columnconfigure(0,weight=1)
        self.__parent.columnconfigure(1,weight=1)
        self.__parent.columnconfigure(2,weight=1)


    def placeCanvas(self):
        self.__parent.grid(row=1,column=0,sticky=(N,E,W,S))

    def placeStream(self,row,column):
        pass

    @property 
    def Canvas(self):
        return self.__parent

        
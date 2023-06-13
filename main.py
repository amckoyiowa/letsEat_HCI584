#Beginning imports, may change later
from tkinter import *
import tkinter.filedialog 
import tkinter.messagebox
import feedparser
import glob
import os
import urllib.parse # for making a safe URL
import requests 
import random
import string
from pprint import pprint

class App(Frame):
    def __init__(self, master):     
        self.master = master # store link to master window, use as frame to put all other widgets into
        # make a label
        self.label = Label(self.master, text="Search a protein you're in the mood for", 
                           justify=LEFT, 
                           font= ("Helvetica","16", "bold"))        
        self.label.grid(row=0, column=0, sticky="e")

        # make a entry field for the search to save the text into on quit 
        self.entry_text_variable = StringVar()
        self.entry = Entry(self.master, width=30, 
                           textvariable=self.entry_text_variable) # textvariable arg needs to be a special TKinter variable!

        # quit button
        self.button2 = Button(self.master, text="Quit", command=self.quit)
        self.button2.grid(row=0, column=2, sticky="we") # sticky="we" make stick to west and east => stretch 
        
        # use the grid geometry manager to put them into your first row
        # re-use the code for creating a Frame with the Text widget and the y scrollbar inside
        # you will use insert() in your processing method later to display the results
        # define new frame and put text area and scroll bar in it
        self.textframe=Frame(self.master)

        # put text frame in 2.row but merge the all columns of row 1 together
        self.textframe.grid(row=1, column=0, columnspan=3, sticky=(N, S, E, W)) 

        # create and pack the text area
        self.text=Text(self.textframe, height=30, width=100,wrap=WORD)
        self.text.pack(side=LEFT, fill=BOTH)
    
        # yview callback gets called when the scroll bar or its arrows are moved
        self.text_scroll=Scrollbar(self.textframe, command=self.text.yview)
        self.text_scroll.pack(side=RIGHT,fill=Y)
    
        # this connects changes in the scroll bar to changing the text area
        # i.e. the text area will show a smaller window into the full text
        self.text.configure(yscrollcommand=self.text_scroll.set)

# This cell is running the app
master = Tk()  # create a Tk window called master
master.title("A simple TkInter text editor")
myapp = App(master) # create App object within master (Tk) windowmaster.mainloop() # draw master window, react to events only
master.mainloop() # draw master window, react to events 
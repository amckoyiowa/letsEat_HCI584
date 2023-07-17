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
from os import sep, getcwd, walk, listdir, chdir
from os.path import exists, isdir, isfile, getsize, basename, join, split
from pprint import pprint

class App(Frame):
    def __init__(self, master):     
        self.master = master # store link to master window, use as frame to put all other widgets into
        # make a label
        self.label = Label(self.master, text="What would you like to eat?", 
                           justify=LEFT, 
                           font= ("Helvetica","16", "bold"))        
        self.label.grid(row=0, column=0, sticky="e")

        # make a entry field for the search to save the text into on quit 
        self.entry_text_variable = StringVar()
        self.entry = Entry(self.master, width=30, 
                           textvariable=self.entry_text_variable) # textvariable arg needs to be a special TKinter variable!

        # add a Run search button that will run your processing method
        # and/or bind() the Return key into the Entry widget to run your processing method 
        self.entry.bind("<Return>", self.process_entry) 
        self.entry.grid(row=0, column=1, sticky="w") # sticky="w" make stick to west

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

    def process_entry(self, event=None):
        search_term = self.entry_text_variable.get() # get content of text entry field
        if self.check_folder("Data"):
            # get files in folder1 in list1
            with open("Data/RAW_recipes.csv", 'r') as file:
                contents = file.read()
                print(contents[0])
        print(search_term)

    def check_folder(self, folder):
        '''Will check if the folder (string) exists and also is not a file and also in not empty.
        Returns True if ALL three conditions are fulfilled, otherwise returns False
        '''

        # 1) check that the folder actually exists  (potential user typo?)
        if not exists(folder):
            # on error, return an informative error message (a single string!)
            return "\nError: The folder name you provided does not exists. Please check your input for typos."
        
        
        # 2) check that folder is actually a folder, not just a weirdly named file 
        if not isdir(folder):
            # on error, return an informative error message (a single string!)
            return "\nError: The name you provided is not a folder. Please try again."


        # 3) check that folder actally contains any files or folders (i.e. is NOT empty) 
        if len(listdir(folder)) == 0:
            # on error, return an informative error message (a single string!)
            return "\nError: The folder name you provided is empty."
        
        
        # 4) if no errors occured, return True
        return True
# This cell is running the app
master = Tk()  # create a Tk window called master
master.title("A simple TkInter text editor")
myapp = App(master) # create App object within master (Tk) windowmaster.mainloop() # draw master window, react to events only
master.mainloop() # draw master window, react to events 
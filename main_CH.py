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

import pandas as pd # please use pandas instead of csv!
import sys

# CH set data location as constants
DATA_FOLDER = "Data"
DATA_FILE = "RAW_recipes.csv"

class App(Frame):
    def __init__(self, master):     
        self.master = master # store link to master window, use as frame to put all other widgets into
    

        # CH set up a set of multiple "conditions" to be used for filtering

        # 1) search for words in 
        self.label1 = Label(self.master, text="What would you like to eat?", justify=LEFT)        
        self.label1.grid(row=0, column=0, sticky="e")        
        self.title_search_value = StringVar()
        self.title_search = Entry(self.master, width=20, textvariable=self.title_search_value) 
        self.title_search.bind("<Return>", self.process_entry) 
        self.title_search.grid(row=0, column=1, sticky="w")  

        # 2) not more than n steps
        self.label2 = Label(self.master, text="Maximum steps:", justify=LEFT)        
        self.label2.grid(row=0, column=2, sticky="e")        
        self.max_steps_value = StringVar()
        self.max_steps = Entry(self.master, width=2, textvariable=self.max_steps_value)
        self.max_steps.insert(0, "5")  # Default value
        self.max_steps.bind("<Return>", self.process_entry) 
        self.max_steps.grid(row=0, column=3, sticky="w") 

        # quit button 
        # CH put back later ...
        #self.button2 = Button(self.master, text="Quit", command=self.quit)
        #self.button2.grid(row=0, column=2, sticky="we") # sticky="we" make stick to west and east => stretch 
        
        # use the grid geometry manager to put them into your first row
        # re-use the code for creating a Frame with the Text widget and the y scrollbar inside
        # you will use insert() in your processing method later to display the results
        # define new frame and put text area and scroll bar in it
        self.textframe=Frame(self.master)

        # put text frame in 2.row but merge the all columns of row 1 together
        # CH adjust columnspan so it covers ALL you columns
        self.textframe.grid(row=1, column=0, columnspan=4, sticky=(N, S, E, W)) 

        # create and pack the text area
        self.text=Text(self.textframe, height=30, width=100,wrap=WORD)
        self.text.pack(side=LEFT, fill=BOTH)
    
        # yview callback gets called when the scroll bar or its arrows are moved
        self.text_scroll=Scrollbar(self.textframe, command=self.text.yview)
        self.text_scroll.pack(side=RIGHT,fill=Y)
    
        # this connects changes in the scroll bar to changing the text area
        # i.e. the text area will show a smaller window into the full text
        self.text.configure(yscrollcommand=self.text_scroll.set)

        # CH read csv into a dataframe here, so we can search/filter in it based on user input later
        r = self.check_folder(DATA_FOLDER)
        if r == True:
            path = DATA_FOLDER + "/" + DATA_FILE
            data = pd.read_csv(path)
            self.data = data.drop(data[data["minutes"] < 0.1].index) # remove 0 minute rows
        else:
            sys.exit(f"{r}\ncsv must be in folder {DATA_FOLDER} and be called {DATA_FILE}!\nAborting ....")

    def process_entry(self, event=None):
        
        search_term = self.title_search_value.get() # get content of text entry field

        # df with exact matches (not case sensitive)
        mask1 = self.data["name"].str.contains(search_term, case=False, regex=False, na=False)
        df1 = self.data[mask1]
        print(len(df1), "matches")

        # grabe 3 random rows
        NUMRECS = 3
        rando_recs = df1.sample(n=NUMRECS) 

        # TODO: Need to check that we have at least 3 results!

        # print out results
        for i in range(len(rando_recs)):
            ser = rando_recs.iloc[i] # get row (actually a Series)
            name = ser["name"]
            minutes = ser["minutes"]
            ingr = ser["ingredients"]
            ingr = ingr.replace("[", "").replace("]", "").replace("'", "")
            steps = ser["steps"]
            steps = steps.replace("[", "").replace("]", "").replace("'", "")
            print(name, minutes)
            print(ingr)
            print(steps)

            self.text.insert(INSERT, f"{name} ({minutes} minutes)\n")
            self.text.insert(INSERT, f"{ingr}\n")
            self.text.insert(INSERT, f"{steps}\n\n")

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
master.title("Let's Eat!")
myapp = App(master) # create App object within master (Tk)  
master.mainloop() # draw master window, react to events 
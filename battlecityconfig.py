## Project: BattleCity
## Module: BattleCity Config
## Author: Salwan

import pygame
from Tkinter import *
from pyenkido.preferences import *

__author__="Salwan"
__date__ ="$Sep 24, 2010 3:10:50 PM$"



class MyApp:
    def __init__(self, parent):
        self.gamePrefs = GamePreferences()
        self.gamePrefs.load("game.cfg")

        self.mainFrame = parent
        self.mainFrame.configure(padx=5, pady=5)
        self.mainFrame.columnconfigure(0, minsize=100)
        self.mainFrame.columnconfigure(1, minsize=100)
        self.mainFrame.columnconfigure(2, minsize=100)

        px = 10
        py = 10

        self.label1 = Label(self.mainFrame, text="Display mode: ")
        self.label1.grid(row=0, column=0,sticky=W+N)

        self.label2 = Label(self.mainFrame, text="Display resolution: ")
        self.label2.grid(row=1, column=0, sticky=W+N)

        self.label3 = Label(self.mainFrame, text="Scale filter: ")
        self.label3.grid(row=2, column=0, sticky=W+N)

        

        self.supRes = {
            0:("800x600 - Default", (800, 600)),
            1:("768x720 - Best view", (768, 720)),
            2:("640x480", (640, 480)),
            3:("1024x768", (1024, 768))
            }
        self.invRes = {
            (800, 600):0,
            (768, 720):1,
            (640, 480):2,
            (1024, 768):3,
            }

        self.supScale = {
            0:"No scale filter - Default",
            1:"Smooth scale filter",
            }

        self.supMode = {
            0:"No - Default",
            1:"Yes"
            }

        self.resList = Listbox(self.mainFrame, selectmode=SINGLE, height=4, exportselection=0)
        self.resList.grid(row=1, column=1, columnspan=2, sticky=W+E)
        for i in self.supRes.itervalues():
            self.resList.insert(END, i[0])
        self.resList.select_set(self.invRes[self.gamePrefs.displayResolution])

        self.scaleList = Listbox(self.mainFrame, selectmode=SINGLE, height=2, exportselection=0)
        self.scaleList.grid(row=2, column=1, columnspan=2, sticky=W+E)
        for i in self.supScale.itervalues():
            self.scaleList.insert(END, i)
        self.scaleList.select_set(self.gamePrefs.scaleFilter)

        self.modeList = Listbox(self.mainFrame, selectmode=SINGLE, height=2, exportselection=0)
        self.modeList.grid(row=0, column=1, columnspan=2, sticky=W+E)
        for i in self.supMode.itervalues():
            self.modeList.insert(END, i)
        self.modeList.select_set(self.gamePrefs.fullscreen)

        self.OKButton = Button(self.mainFrame, command=self.buttonClick_OK, text="OK", width=10)
        self.OKButton.grid(row=3, column=0, sticky=W,padx=px,pady=py)

        self.DefaultButton = Button(self.mainFrame, command=self.buttonClick_Default, text="Default", width=10)
        self.DefaultButton.grid(row=3, column=1, sticky=S,padx=px,pady=py)

        self.CancelButton = Button(self.mainFrame, command=self.buttonClick_Cancel, text="Cancel",width=10)
        self.CancelButton.grid(row=3, column=2, sticky=E,padx=px,pady=py)

    def buttonClick_OK(self):
        print "<OK Clicked> - Saving game preferences"
        resi = int(self.resList.curselection()[0])
        scai = int(self.scaleList.curselection()[0])
        modi = int(self.modeList.curselection()[0])
        self.gamePrefs.displayResolution = self.supRes[resi][1]
        self.gamePrefs.scaleFilter = scai
        self.gamePrefs.fullscreen = modi
        self.gamePrefs.save("game.cfg")
        self.mainFrame.destroy()

    def buttonClick_Cancel(self):
        print "<Cancel Clicked>"
        self.mainFrame.destroy()

    def buttonClick_Default(self):
        print "<Default Clicked>"
        self.gamePrefs = GamePreferences()
        self.resList.select_clear(int(self.resList.curselection()[0]))
        self.scaleList.select_clear(int(self.scaleList.curselection()[0]))
        self.modeList.select_clear(int(self.modeList.curselection()[0]))
        self.resList.select_set(self.invRes[self.gamePrefs.displayResolution])
        self.scaleList.select_set(self.gamePrefs.scaleFilter)
        self.modeList.select_set(self.gamePrefs.fullscreen)

root = Tk()
root.title("BattleCity Remake - Config")
myapp = MyApp(root)
root.mainloop()





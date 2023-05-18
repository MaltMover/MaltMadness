import tkinter
from tkinter import *


class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("MaltMadness")
        self.geometry("960x540")

        self.configure(
            bg="#000000"
        )
        self.mainloop()

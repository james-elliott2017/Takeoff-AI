#James Elliott
#Main GUI Code for Autocount software

import tkinter as tk
from tkinter import filedialog
from main import *


def browsefunc():
    filename = filedialog.askdirectory()
    ent1.insert(tk.END, filename)  # add this

def say_hi():
    print("hi there, everyone!")
"""
class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.go = tk.Button(self)
        self.go["text"] = "Hello World\n(click me)"
        self.go["command"] = self.say_hi
        self.go.pack(side="top")

        self.ent1 = tk.Entry(root, font=40)
        self.ent1.pack(side="top")
        self.projectDir = tk.Button(root, text="DEM", font=40, command=browsefunc)
        self.projectDir.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
"""
root = tk.Tk()
root.geometry("1000x500")

base_columnspan = 100


go = tk.Button(root,text = "Hello World\n(click me)", font = 40, command=say_hi)
#go.pack()
go.grid(row=3,column=3)

ent1 = tk.Entry(root, font=40)
#ent1.pack()
ent1.grid(row = 1, columnspan = 1)

projectDir = tk.Button(root, text="Find Folder", font=40, command=browsefunc)
#projectDir.pack()
projectDir.grid(row = 1, column = base_columnspan + 1)

quit = tk.Button(root, text="QUIT", fg="red",command=root.destroy)
#quit.pack()
quit.grid(row = 5, column = 5)


#start GUI#
#app = Application(master=root)
root.mainloop()
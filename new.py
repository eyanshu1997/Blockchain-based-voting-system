import Tkinter as tk
from Tkinter import *

class Application(Frame):
    def __init__(self, master):
		super(Application, self).__init__(master)
		self.grid()
		self.widgets()

    def widgets(self):
        self.entryBox = Entry(self).grid()
        Button(self, text="Submit", command=self.search()).grid()

    def search(self):
        if len(self.entryBox.get()) == 0:
			tkinter.messagebox.showinfo("Warning!", "Box is empty! Write something")
        else:
            do_something()

    # main
root = Tk()
root.title("Title")
app = Application(root)
root.mainloop()
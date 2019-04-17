import Tkinter as tk
from Tkinter import *
et=0
xt=0
def focus1(event): 
    course_field.focus_set() 
  
  


	
def calc():
	print et
	print xt
def avoter():
	root = Tk()
	root.configure(background='light green')
	root.title("registration form")
	root.geometry("500x300")
	
	heading = Label(root, text="Form", bg="light green")
	name = Label(root, text="Name", bg="light green")
	pas = Label(root, text="Course", bg="light green")
	
	heading.grid(row=0, column=1)
	name.grid(row=1, column=0)
	pas.grid(row=2, column=0)
	
	name_field = Entry(root)
	pass_field = Entry(root)
	
	name_field.bind("<Return>", focus1)
	pass_field.bind()
	
	name_field.grid(row=1, column=1, ipadx="100")
	pass_field.grid(row=2, column=1, ipadx="100") 
 
	et=name_field.get()
	xt=pass_field.get()
	submit = Button(root, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=8, column=1)
	root.mainloop()  
re = tk.Tk() 
re.title('voting system') 
button = tk.Button(re, text=' add a voter', width=25, command=avoter)
button.pack()
button = tk.Button(re,text='add a vote' , width=25,command=avoter)
button.pack() 
re.mainloop() 
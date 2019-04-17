import Tkinter as tk
from Tkinter import *
et=0
xt=0
def focus1(event): 
    course_field.focus_set() 
  
  
  
re = tk.Tk() 
re.title('voting system')
re.configure(background='light green')
re.geometry("500x300")
def avoter():
	heading = Label(re, text="Form", bg="light green")
	name = Label(re, text="Name", bg="light green")
	pas = Label(re, text="voter pass", bg="light green")
	
	heading.grid(row=1, column=1)
	name.grid(row=2, column=0)
	pas.grid(row=3, column=0)
	
	name_field = Entry(re)
	pass_field = Entry(re)
	
	name_field.bind("<Return>", focus1)
	pass_field.bind()
	
	name_field.grid(row=2, column=1, ipadx="50")
	pass_field.grid(row=3, column=1, ipadx="50") 

	def calc():
		et=name_field.get()
		xt=pass_field.get()
		print et
		print xt
		
	submit = Button(re, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=9, column=1)
button = tk.Button(re, text=' add a voter', width=25, command=avoter)
button.grid(row=0,column=0)
butt = tk.Button(re,text='add a vote' , width=25,command=avoter)
butt.grid(row=0,column=1)
re.mainloop() 
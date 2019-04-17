import Tkinter as tk
from Tkinter import *

  
re = tk.Tk() 
re.title('voting system')
re.configure(background='light green')
re.geometry("700x400")
def avoter():
	heading = Label(re, text="ADD A VOTER", bg="light green")
	name = Label(re, text="Name", bg="light green")
	pas = Label(re, text="voter pass", bg="light green")
	
	heading.grid(row=1, column=1)
	name.grid(row=2, column=0)
	pas.grid(row=3, column=0)
	
	name_field = Entry(re)
	pass_field = Entry(re)
	
	name_field.grid(row=2, column=1, ipadx="50")
	pass_field.grid(row=3, column=1, ipadx="50") 

	def calc():
		et=name_field.get()
		xt=pass_field.get()
		print et
		print xt
		
	submit = Button(re, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=9, column=1)
def avote():
	heading = Label(re, text="ADD A VOTE", bg="light green")
	name = Label(re, text="Voter Hash", bg="light green")
	pas = Label(re, text="voter pass", bg="light green")
	vote = Label(re, text="candidate id bwteen (0/1)", bg="light green")
	heading.grid(row=1, column=1)
	name.grid(row=2, column=0)
	pas.grid(row=3, column=0)
	vote.grid(row=4,column=0)
	
	name_field = Entry(re)
	pass_field = Entry(re)
	vote_field = Entry(re)
	
	name_field.grid(row=2, column=1, ipadx="50")
	pass_field.grid(row=3, column=1, ipadx="50") 
	vote_field.grid(row=4, column=1, ipadx="50") 
	def calc():
		et=name_field.get()
		xt=pass_field.get()
		vt=vote_field.get()
		print et
		print xt
		print vt
		
	submit = Button(re, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=9, column=1)
def countvote():
	heading = Label(re, text="COUNT VOTE", bg="light green")
	name = Label(re, text="Candidate id", bg="light green")
	heading.grid(row=1, column=1)
	name.grid(row=2, column=0)

	name_field = Entry(re)
	
	name_field.grid(row=2, column=1, ipadx="50")
 
	def calc():
		et=name_field.get()

		print et
		
	submit = Button(re, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=9, column=1)
def icheck():
	heading = Label(re, text="INTEGRITY CHECK", bg="light green")
	heading.grid(row=1, column=1)
	print " intergrity check"
button = tk.Button(re, text=' add a voter', width=25, command=avoter)
button.grid(row=0,column=0)
butt = tk.Button(re,text='add a vote' , width=25,command=avote)
butt.grid(row=0,column=1)
but = tk.Button(re,text='count vote of candidate' , width=25,command=countvote)
but.grid(row=0,column=2)
butt1 = tk.Button(re,text='integrity check' , width=25,command=icheck)
butt1.grid(row=0,column=3)
re.mainloop() 
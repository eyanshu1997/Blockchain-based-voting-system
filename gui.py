import Tkinter as tk
from Tkinter import *
import tkMessageBox
import socket			
import datetime 
import hashlib
import os
voteblocks=[]
blocks=[] 

file= ""
vfile=""
no=0
port = 12348
ip='127.0.0.1'
def compare(x,block):
	y=0
	for  y in range(len(block)):
		if x[y]!=block[y]:
			return 1
	return 0
	
	
def check(block):
	for x in blocks:
		if x[0]==block[0]:
			if compare(x,block)==1:
				print "error in data tampered", x ,block
				print " eroor: ",x[0],block[0]
				return 2
			return 1
	return 0
	
	
def vcheck(block):
	for x in voteblocks:
		if x[0]==block[0]:
			if compare(x,block)==1:
				print "error in data tampered"
				print " eroor: ",x[0],block[0]
				return 2
			return 1
	return 0
	
def sync():
	choice='4'
	global no
	global file
	global vfile
	print "sync started"
	f = open(file)
	lines = f.readlines()
	for x in lines:
		block =[]
		for y in x.strip("\n").split(","):
			block.append(y)
		z=check(block)
		if z==0:
			blocks.append(block)
		else:
			if z==2:
				return 1
	f=open(vfile)
	lines=f.readlines()
	for x in lines:
		block =[]
		for y in x.strip("\n").split(","):
			block.append(y)
		o=vcheck(block)
		if o==0:
			voteblocks.append(block)
		else:
			if o==2:
				return 1
	s = socket.socket()
	s.connect((ip, port))
	s.send(no)
	x=s.recv(1024)
	print "from server: ",x
	s.send(choice)
	l=str(len(blocks))
	x= s.recv(1024)
	if len(blocks)==0:
		s.send(str(len(blocks)))
		x=s.recv(1024)
		print x
	else:
		s.send(str(len(blocks)))
		s.recv(1024)
		s.send(str(len(blocks[0])))
		s.recv(1024)
		for b in blocks:
			for dig in b:
				s.send(dig)
				s.recv(1024)
	if len(voteblocks)==0:
		s.send(str(len(voteblocks)))
		x=s.recv(1024)
		print x
	else:
		s.send(str(len(voteblocks)))
		s.recv(1024)
		s.send(str(len(voteblocks[0])))
		s.recv(1024)
		for b in voteblocks:
			for dig in b:
				s.send(dig)
				s.recv(1024)
	s.close()
	return 0
	
	
class quitButton(Button):
    def __init__(self, parent):
        Button.__init__(self, parent)
        self['text'] = 'OK'
        self['command'] = parent.destroy
        self.pack(side=BOTTOM)
def msg(ms,w=200,h=100):
	sync()
	main = Tk() 
	def cl(event):
		main.destroy()
	main.lift()
	main.attributes("-topmost", True)
	main.bind('<Return>',cl)
	ws = main.winfo_screenwidth() 
	hs = main.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	main.geometry('%dx%d+%d+%d' % (w, h, x, y))
	def close_window (): 
		root.destroy()
	ourMessage =ms
	frame = Frame(main,height=h,width=w)
	frame.pack()
	messageVar = Message(frame, text = ourMessage,width=w) 
	messageVar.config(bg='light blue') 
	messageVar.pack( ) 
	quitButton(main)
	main.mainloop( ) 
def err(ms,w=80,h=120):
	main = Tk() 
	def cl(event):
		main.destroy()
	main.lift()
	main.attributes("-topmost", True)
	main.bind('<Return>',cl)
	ws = main.winfo_screenwidth() 
	hs = main.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	main.geometry('%dx%d+%d+%d' % (w, h, x, y))
	def close_window (): 
		root.destroy()
	ourMessage =ms
	frame = Frame(main,height=h,width=w)
	frame.pack()
	messageVar = Message(frame, text = ourMessage,width=w) 
	messageVar.config(bg='light blue') 
	messageVar.pack( ) 
	quitButton(main)
	main.mainloop( ) 
	
def amsg(ms,has,w=80,h=120):
	def close_window (): 
		main.destroy()
	def paste():
		text=has
		command = 'echo ' + text.strip()+ '| clip'
		os.system(command)
		close_window()
	sync()
	main = Tk() 
	def cl(event):
		main.destroy()
	main.lift()
	main.attributes("-topmost", True)
	main.bind('<Return>',cl)
	ws = main.winfo_screenwidth() 
	hs = main.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)

	
	main.geometry('%dx%d+%d+%d' % (w, h, x, y))
	ourMessage =ms
	frame = Frame(main,height=h,width=w)
	frame.pack()
	messageVar = Message(frame, text = ourMessage,width=w) 
	messageVar.config(bg='lightblue') 
	messageVar.pack( ) 
	submit = Button(main, text="Copy Hash", padx=10, pady=10, command=paste)
	submit.pack()
	quitButton(main)
	main.mainloop( ) 

	
def sconvert(s): 
    new = "" 
    for x in s: 
		if x!=s[-1]:
			new += (str(x)+ ", ")   
		else:
			new+=(str(x))
    return new 
	
def convert(s): 
    new = "" 
    for x in s: 
        new += (str(x)+ " ")   
    return new 
	

	
def sendvote(voterhash,voterpass,vote):
	choice='5'
	global no
	global file
	global vfile
	print "send vote started"
	ti=str(datetime.datetime.now())
	s = socket.socket()
	s.connect((ip, port))
	s.send(no)
	x=s.recv(1024)
	print "from server: ",x		
	s.send(choice)
	print("waiting for prehash")
	prehash=s.recv(1024)
	s.send("recieved")
	count=s.recv(1024)
	s.send(voterhash)
	print "sent votrehash"
	x=s.recv(1024)
	if x=='false' or x=='falsevote':
		if x=='false':
			print "false voterhash"
			msg("false voterhash")
		if x=='falsevote':
			print "vote for this hash already exists"
			msg("vote already exits")
	else:
		s.send(voterpass)
		print "sent voterpass"
		x=s.recv(1024)
		if x=='false':
			print "invlid details"
			msg("invalid details")
		else:
			print "previous hash",prehash
			print "count " , count
			block=[count,voterhash,voterpass,vote,prehash,ti]
			has= hashlib.sha224(convert(block)).hexdigest()
			block.append(has)
			voteblocks.append(block)
			f = open(vfile, "a")	
			for li in block:
				if li==block[-1]:
					f.write(li)
				else:
					f.write(li+",")
			f.write("\n")
			f.close()
			s.send(has)
			print "vote block added"
			msg("vote block added\n"+sconvert(block),400,100)
			print block
			print "vote block list"
			print voteblocks
	s.close()
	
	
def sendv(votername,voterpass,dob):
	choice='2'
	global no
	global file
	global vfile
	print "sendv started"
	ti=str(datetime.datetime.now())
	s = socket.socket()
	s.connect((ip, port)) 	
	s.send(no)
	x=s.recv(1024)
	print "from server: ",x
	s.send(choice)
	print("waiting for prehash")
	prehash=s.recv(1024)
	s.send("recieved")
	count=s.recv(1024)
	print "previous hash",prehash
	print "count " , count

	s.send(votername)
	s.recv(1024)
	s.send(dob)
	x=s.recv(1024)
	if x=='false' :
		print "voter exists"
		msg("voter exists")
	else:
		block=[count,votername,voterpass,prehash,ti,dob]
		has= hashlib.sha224(convert(block)).hexdigest()
		block.append(has)
		blocks.append(block)
		s.send(has)
		f = open(file, "a")	
		for li in block:
			if li==block[-1]:
				f.write(li)
			else:
				f.write(li+",")
		f.write("\n")
		f.close()
		print "block added"
		print block
		amsg("block added: \n"+sconvert(block),has,400,100)
		print "block list"
		print blocks
	s.close()
	
def cvote(candidate):
	choice='6'
	global no
	global file
	global vfile
	print "countvote started"
	s = socket.socket()
	s.connect((ip, port))
	s.send(no)
	x=s.recv(1024)
	print "from server: ",x		
	s.send(choice)
	s.recv(1024)
	s.send(candidate)
	co=s.recv(1024)
	print "Number of votes for that candidate: ",co
	ms="Number of votes for this candidate: "+co
	heading = Label(re, text=ms, bg="light blue", font=('TIMES NEW ROMAN',15))
	heading.grid(row=8, column=1)
	msg(ms)
	s.close()
	
def intcheck():
	if sync()==1:
		return "data tampered"
	choice='7'
	global no
	global file
	global vfile
	print "integrity check started"
	s = socket.socket()
	s.connect((ip, port))
	s.send(no)
	x=s.recv(1024)
	print "from server: ",x		
	s.send(choice)
	x=s.recv(1024)
	print x
	s.send("recieved")
	count=s.recv(1024)
	s.send("recived")
	vcount=s.recv(1024)
	ms="Voter chain no. of lists: "+count
	head=Label(re,text=ms, bg="light green")
	head.grid(row=5,column=1)
	ms="Vote chain no. of lists: "+vcount
	head=Label(re,text=ms, bg="light green")
	head.grid(row=6,column=1)
	ms="No. of Voters in this client: "+str(len(blocks))
	head=Label(re,text=ms, bg="light green")
	head.grid(row=7,column=1)
	ms="No. of Votes in this client: "+str(len(voteblocks))
	head=Label(re,text=ms, bg="light green")
	head.grid(row=8,column=1)
	s.close()
	return x
  
re = tk.Tk() 
re.title('Voting system')
re.configure(background='light blue')
re.geometry("700x600")
def dialog():
	w=200
	h=100
	check=0
	main = Tk() 
	main.lift()
	main.attributes("-topmost", True)
	ws = main.winfo_screenwidth() 
	hs = main.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	main.geometry('%dx%d+%d+%d' % (w, h, x, y))
	def close_window (): 
		root.destroy()
	ourMessage ="are yu sure you want to exit?"
	frame = Frame(main,height=h,width=w)
	frame.pack()
	messageVar = Message(frame, text = ourMessage,width=w) 
	messageVar.config(bg='light blue') 
	messageVar.pack( )
	def yes():
		main.destroy()
		re.destroy()
	def no():
		main.destroy()
	ye=Button(main,text="yes",command=yes)
	ye.pack()
	noo=Button(main,text="no",command=no)
	noo.pack()
	main.mainloop( ) 
def start():
	heading = Label(re, text="ENTER CLIENT DETAILS", bg="light blue", pady="10", font = ('TIMES NEW ROMAN',30))
	name = Label(re, text="Client Number",bg= 'light blue',font = ('TIMES NEW ROMAN',15))
	i = Label(re, text="IP OF SERVER",bg= 'light blue', font = ('TIMES NEW ROMAN',15))
	heading.grid(row=1, column=2)
	name.grid(row=2, column=0)
	i.grid(row=3, column=0)
	name_field = Entry(re)
	i_field=Entry(re)
	name_field.grid(row=2, column=2, ipadx="60")
	i_field.grid(row=3,column=2,ipadx="60")
	def calc():
		global no
		global file
		global vfile
		global ip
		no=name_field.get()
		ip=str(i_field.get())
		if len(no)==0 and len(ip)==0:
			err("enter all fields")
		else:
			print "ip is",ip
			file= no+".txt"
			vfile=no+"vote.txt"
			home()
	submit = Button(re, text="Submit", font=(10), command=calc)
	q= tk.Button(re,text="Quit", padx=8, font=(10), command= dialog)
	submit.grid(row=9, column=2,pady=10)
	q.grid(row=10,column=2)

def clear():
    list = re.grid_slaves()
    for l in list:
        l.destroy()
def top():
	heading = Label(re, text="VOTER ACTIONS", bg="light blue", pady="10", font = ('TIMES NEW ROMAN',30))
	heading.grid(row=0, column=1)
	button = tk.Button(re, text='Add a voter', width=30, padx=10,pady=10, command=avoter)
	button.grid(row=1,column=0,padx=10,pady=10)
	butt = tk.Button(re,text='Add a vote' , width=30, padx=10,pady=10, command=avote)
	butt.grid(row=1,column=1,padx=10,pady=10)
	but = tk.Button(re,text='count vote of candidate' , width=30, padx=10,pady=10, command=countvote)
	but.grid(row=2,column=0,padx=10,pady=10)
	butt1 = tk.Button(re,text='integrity check' , width=30, padx=10,pady=10, command=icheck)
	butt1.grid(row=2,column=1,padx=10,pady=10)
	butt1 = tk.Button(re,text='Quit' , width=10, padx=10,pady=10, command=dialog)
	butt1.grid(row=3,column=0,padx=10,pady=10)
	
    
def home():
	global file
	global vfile
	sync()
	print no
	print str(file)
	print str(vfile)
	clear()
	top()
	ms="Number of Voters in this Client: "+str(len(blocks))
	head=Label(re,text=ms, bg="light blue", font =('TIMES NEW ROMAN',15))
	head.grid(row=5,column=1)
	ms="Number of Votes in this Client: "+str(len(voteblocks))
	head=Label(re,text=ms, bg="light blue", font =('TIMES NEW ROMAN',15))
	head.grid(row=6,column=1)

	
def avoter():
	clear()
	top()
	heading = Label(re, text="ADD A VOTER", bg="light blue", pady="10", font = ('TIMES NEW ROMAN',30))
	name = Label(re, text="Voter Name", bg="light blue")
	pas = Label(re, text="Voter Password", bg="light blue")
	dob=Label(re,text="dob",bg="light blue")
	heading.grid(row=5, column=1)
	name.grid(row=6, column=0)
	pas.grid(row=8, column=0)
	dob.grid(row=7,column=0)
	
	name_field = Entry(re)
	dob_field=Entry(re)
	pass_field = Entry(re)
	name_field.grid(row=6, column=1, ipadx="50")
	pass_field.grid(row=8, column=1, ipadx="50") 
	dob_field.grid(row=7,column=1,ipadx="50")
	def calc():
		et=name_field.get()
		xt=pass_field.get()
		yt=dob_field.get()
		if len(et) ==0 and len(xt)==0 and len(yt)==0:
			msg("enter all input")
		else:
			print et
			print xt
			sendv(et,xt,yt)
			avoter()
			home()
	submit = Button(re, text="Submit", padx=10, pady=10,command=calc)
	submit.grid(row=9, column=1)
	button = tk.Button(re, text='home', width=25, padx=10, pady=10, command=home)
	button.grid(row=3,column=1, pady=10, padx=10)
	
def avote():
	clear()
	top()

	heading = Label(re, text="ADD A VOTE", bg="light blue", pady="10", font = ('TIMES NEW ROMAN',30))
	name = Label(re, text="Voter Hash", bg="light blue")
	pas = Label(re, text="Voter password", bg="light blue")
	vote = Label(re, text="Candidate id Between (1/10)", bg="light blue")
	heading.grid(row=5, column=1)
	name.grid(row=6, column=0)
	pas.grid(row=7, column=0)
	vote.grid(row=8,column=0)
	
	name_field = Entry(re)
	pass_field = Entry(re)
	vote_field = Entry(re)
	
	name_field.grid(row=6, column=1, ipadx="50")
	pass_field.grid(row=7, column=1, ipadx="50") 
	vote_field.grid(row=8, column=1, ipadx="50") 
	def calc():
		et=name_field.get()
		xt=pass_field.get()
		vt=vote_field.get()
		if len(et) ==0 and len(xt)==0 and len(vt)==0:
			msg("enter all input")
		else:
			print et
			print xt
			print vt
			sendvote(et,xt,vt)
			home()
	submit = Button(re, text="Submit", padx=10, pady=10,command=calc)
	submit.grid(row=9, column=1)
	button = tk.Button(re, text='Home',padx=10, pady=10, width=25, command=home)
	button.grid(row=3,column=1,padx=10,pady=10)
	
def countvote():
	clear()
	top()
	heading = Label(re, text="COUNT VOTE",  bg="light blue", pady="10", font = ('TIMES NEW ROMAN',30))
	name = Label(re, text="Candidate id", bg="light blue")
	heading.grid(row=5, column=1)
	name.grid(row=6, column=0)

	name_field = Entry(re)
	
	name_field.grid(row=6, column=1, ipadx="50")
 
	def calc():
		et=name_field.get()
		print et
		if len(et)==0:
			msg("Enter input")
		else:
			cvote(et)
			home()
	submit = Button(re, text="Submit",padx=10, pady=10, command=calc)
	submit.grid(row=7, column=1)
	button = tk.Button(re, text='home', width=25, command=home)
	button.grid(row=3,column=1)
def icheck():
	clear()
	top()
	message = intcheck()
	heading = Label(re, text="INTEGRITY CHECK", bg="light green")
	heading.grid(row=5, column=1)
	head=Label(re,text=message, bg="light Blue", font=('TIMES NEW ROMAN', 15))
	head.grid(row=5,column=1)
	print "Intergrity check"
	button = tk.Button(re, text='home', padx=10, pady=10, width=25, command=home)
	button.grid(row=3,column=1)
start()
re.mainloop() 
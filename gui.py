import Tkinter as tk
from Tkinter import *
import socket			
import datetime 
import hashlib

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
        # Command to close the window (the destory method)
        self['command'] = parent.destroy
        self.pack(side=BOTTOM)
def msg(ms,w=80,h=65):
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
	messageVar.config(bg='lightgreen') 
	messageVar.pack( ) 
	quitButton(main)
	main.mainloop( ) 

def sconvert(s): 
  
    # initialization of string to "" 
    new = "" 
  
    # traverse in the string  
    for x in s: 
		if x!=s[-1]:
			new += (str(x)+ ", ")   
		else:
			new+=(str(x))
    # return string  
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
	
	
def sendv(votername,voterpass):
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
	block=[count,votername,voterpass,prehash,ti]
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
	msg("block added: \n"+sconvert(block),400,100)
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
	print "no of votes for that candidate",co
	ms="no of votes for this candidate: "+co
	heading = Label(re, text=ms, bg="light green")
	heading.grid(row=3, column=1)
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
	ms="voter chain no of lists"+count
	head=Label(re,text=ms, bg="light green")
	head.grid(row=3,column=1)
	ms="vote chain no of lists"+vcount
	head=Label(re,text=ms, bg="light green")
	head.grid(row=4,column=1)
	ms="no of voters in this client"+str(len(blocks))
	head=Label(re,text=ms, bg="light green")
	head.grid(row=5,column=1)
	ms="no of votes in this client"+str(len(voteblocks))
	head=Label(re,text=ms, bg="light green")
	head.grid(row=6,column=1)
	s.close()
	return x

	

  
re = tk.Tk() 
re.title('voting system')
re.configure(background='light green')
re.geometry("700x400")

def start():
	heading = Label(re, text="ENTER CLIENT NO", bg="light green")
	name = Label(re, text="Client no", bg="light green")
	i = Label(re, text="IP OF SERVER", bg="light green")
	heading.grid(row=1, column=1)
	name.grid(row=2, column=0)
	i.grid(row=3, column=0)
	name_field = Entry(re)
	i_field=Entry(re)
	name_field.grid(row=2, column=1, ipadx="50")
	i_field.grid(row=3,column=1,ipadx="50")
	def calc():
		global no
		global file
		global vfile
		global ip
		no=name_field.get()
		ip=str(i_field.get())
		print "ip is",ip
		file= no+".txt"
		vfile=no+"vote.txt"
		home()
	submit = Button(re, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=9, column=1)
def clear():
    list = re.grid_slaves()
    for l in list:
        l.destroy()
def top():
	button = tk.Button(re, text=' add a voter', width=25, command=avoter)
	button.grid(row=0,column=0)
	butt = tk.Button(re,text='add a vote' , width=25,command=avote)
	butt.grid(row=0,column=1)
	but = tk.Button(re,text='count vote of candidate' , width=25,command=countvote)
	but.grid(row=0,column=2)
	butt1 = tk.Button(re,text='integrity check' , width=25,command=icheck)
	butt1.grid(row=0,column=3)
def home():
	global file
	global vfile
	sync()
	print no
	print str(file)
	print str(vfile)
	clear()
	top()
	ms="no of voters in this client"+str(len(blocks))
	head=Label(re,text=ms, bg="light green")
	head.grid(row=5,column=1)
	ms="no of votes in this client"+str(len(voteblocks))
	head=Label(re,text=ms, bg="light green")
	head.grid(row=6,column=1)
	
def avoter():
	clear()
	top()
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
		sendv(et,xt)
		avoter()
		home()
	submit = Button(re, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=9, column=1)
	button = tk.Button(re, text='home', width=25, command=home)
	button.grid(row=10,column=1)
def avote():
	clear()
	top()

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
		sendvote(et,xt,vt)
		home()
	submit = Button(re, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=9, column=1)
	button = tk.Button(re, text='home', width=25, command=home)
	button.grid(row=10,column=1)
def countvote():
	clear()
	top()
	heading = Label(re, text="COUNT VOTE", bg="light green")
	name = Label(re, text="Candidate id", bg="light green")
	heading.grid(row=1, column=1)
	name.grid(row=2, column=0)

	name_field = Entry(re)
	
	name_field.grid(row=2, column=1, ipadx="50")
 
	def calc():
		et=name_field.get()
		print et
		cvote(et)
		home()
	submit = Button(re, text="Submit", fg="Black", bg="Red", command=calc)
	submit.grid(row=9, column=1)
	button = tk.Button(re, text='home', width=25, command=home)
	button.grid(row=10,column=1)
def icheck():
	clear()
	top()
	message = intcheck()
	heading = Label(re, text="INTEGRITY CHECK", bg="light green")
	heading.grid(row=1, column=1)
	head=Label(re,text=message, bg="light green")
	head.grid(row=2,column=1)
	print " intergrity check"
	button = tk.Button(re, text='home', width=25, command=home)
	button.grid(row=10,column=1)
start()
re.mainloop() 
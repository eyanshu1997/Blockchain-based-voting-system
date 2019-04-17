import socket			
import datetime 
import hashlib

voteblocks=[]
blocks=[] 

no=raw_input("enter your client no")
file= no+".txt"
vfile=no+"vote.txt"


	
def convert(s): 
    new = "" 
    for x in s: 
        new += (str(x)+ " ")   
    return new 
	
port = 12348
print("enter what you want to do\n 1:get list of all node\n 2: add a voter \n3:exit\n 4: synchronize blocks\n 5: add a vote \n 6: count of vote of candidate\n 7: integrety check of chain\n")
choice=str(raw_input(""))
while True:
	if choice=='1':
		s = socket.socket()
		s.connect(('127.0.0.1', port))
		s.send(no)
		x=s.recv(1024)
		print "from server: ",x		
		s.send(choice)
		x= str(s.recv(1024)) 
		print x
		s.close()
		choice='4'
	if choice=='2':
		votername=raw_input("enter the voter name\n")
		voterpass=raw_input("enter the voter pass\n")
		ti=str(datetime.datetime.now())
		s = socket.socket()
		s.connect(('127.0.0.1', port)) 	
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
		print "block list"
		print blocks
		s.close()
		choice='4'
	if choice=='3':
		break
	if choice=='4':
		voteblocks=[]
		blocks=[] 
		f = open(file)
		lines = f.readlines()
		for x in lines:
			block =[]
			for y in x.strip("\n").split(","):
				block.append(y)
			blocks.append(block)
	
		f=open(vfile)
		lines=f.readlines()
		for x in lines:
			block =[]
			for y in x.strip("\n").split(","):
				block.append(y)
			voteblocks.append(block)
		s = socket.socket()
		s.connect(('127.0.0.1', port))
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
		print("enter what you want to do\n 1:get list of all node\n 2: add a voter \n3:exit\n 4: synchronize blocks\n 5: add a vote\n 6: count of vote of candidate\n 7: integrety check of chain\n")
		choice=str(raw_input(""))
	if choice=='5':
		voterhash=raw_input("enter the voter hash\n")
		voterpass=raw_input("enter the voter pass\n")
		vote=raw_input("enter the id of cadidate you want to vote (1-9)") 
		while vote!='1' and vote!='2' and vote!='3' and vote!='4' and vote!='5' and vote!='6' and vote!='7' and vote!='8' and vote!='9' :
			vote=raw_input("invalid vote please use between 1-9")
		ti=str(datetime.datetime.now())
		s = socket.socket()
		s.connect(('127.0.0.1', port))
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
				print "false voterhas"
			if x=='falsevote':
				print "vote for this hash already exists"
			continue
		else:
			s.send(voterpass)
			print "sent voterpass"
			x=s.recv(1024)
			if x=='false':
				print "invlid details"
				continue
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
				print block
				print "vote block list"
				print voteblocks
		s.close()
		choice='4'
	if choice=='6':
		candidate=raw_input("enter the candidate\n")
		s = socket.socket()
		s.connect(('127.0.0.1', port))
		s.send(no)
		x=s.recv(1024)
		print "from server: ",x		
		s.send(choice)
		s.recv(1024)
		s.send(candidate)
		co=s.recv(1024)
		print "no of votes for that candidate",co
		s.close()
		choice='4'
	if choice=='7':
		s = socket.socket()
		s.connect(('127.0.0.1', port))
		s.send(no)
		x=s.recv(1024)
		print "from server: ",x		
		s.send(choice)
		x=s.recv(1024)
		print x
		s.close()
		choice='4'
	if choice!='1' or choice!='2' or choice!='3' or choice !='4' or choice !='5' or choice !='6' or choice !='7':
		print "no choice"

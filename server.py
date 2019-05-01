import socket			 
import datetime
import hashlib

hashes=[]
blocks=[]
votehashes=[]
voteblocks=[]
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = ' '.join(socket.gethostbyname_ex(socket.gethostname())[2])
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
    except: 
        print("Unable to get Hostname and IP") 
  
def sear(hash):
	for x in hashes:
		if x[1]==hash:
			return 1
	return 0
def searv(hash):
	for x in votehashes:
		if x[1]==hash:
			return 1
	return 0
def integretycheck():
	i=1
	for i in range(len(voteblocks)):
		if searv(voteblocks[i][-1])!=1:
			return 1
	i=1
	for i in range(len(blocks)):
		if sear(blocks[i][-1])!=1:
			return 1
	i=1
	for i in range(len(voteblocks)):
		if voteblocks[i][4]!=voteblocks[i-1][-1]:
			return 1
	i=1
	for i in range(len(blocks)):
		if blocks[i][2]!=blocks[i-1][-1]:
			return 1
	return 0
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
			return 1
	return 0
	
	
def vcheck(block):
	for x in voteblocks:
		if x[0]==block[0]:
			if compare(x,block)==1:
				print "error in data tampered"
			return 1
	return 0
		
def convert(s): 
    new = "" 
    for x in s: 
        new += (str(x)+ " ")   
    return new 
def checkvote(voterhash):
	for x in voteblocks:
		print "comapre x and voterhash",x[1],voterhash
		if x[1]==voterhash:
			return 1
	return 0
def dobmatch(votername,dob):
	for x in blocks:
		if x[1]==votername and x[-2]==dob:
			return 1
	return 0
def fi(voterhash):
	i=0
	found=-1
	for i in range(len(blocks)):
		if blocks[i][-1]==voterhash:
			if checkvote(voterhash)==1:
				print "votealready cast"
				found=-2
				return found
			found=i
			break
	return found

	
t=str(datetime.datetime.now())
voteblock=['0','vote hash',"votepass",'0','ex45pre34hash',t]
vhas= hashlib.sha224(convert(voteblock)).hexdigest()
voteblock.append(vhas)
block=['0','votername','voterpasss','ex45pre34hash','dob',t]
has= hashlib.sha224(convert(block)).hexdigest()
block.append(has)
blocks.append(block)
voteblocks.append(voteblock)

print "Server created\n"
s = socket.socket()		 
port = 12348	
s.bind(('', port))		 
s.listen(5)

get_Host_name_IP()
prehash=has
voteprehash=vhas
while True: 
	print "socket is listening"	
	c,addr = s.accept()	 
	clientno=c.recv(1024)
	c.send("hello  client  "+clientno)
	print 'Got connection from', addr 
	f = open("demofile2.txt", "a")
	f.write(convert(addr)+"\n")
	f.close()
	choice=c.recv(1024)
	if choice=='2':
		c.send(prehash)
		c.recv(1024)
		count=len(blocks)+1
		c.send(str(count))
		print "sent prehash and count"
		votername=c.recv(1024)
		c.send("recieved")
		dob=c.recv(1024)
		res=dobmatch(votername,dob)
		if res==1:
			c.send("false")
		else:
			c.send("true")
			data=c.recv(1024)
			print "voter data added hash is",data,"by addres",addr
			prehash=data
			arr=[count,data,addr,clientno]
			hashes.append(arr)
			print "hash list",hashes
	if choice=='4':
		c.send("choice recieved")
		n=c.recv(1024)
		if int(n)==0:
			c.send("not added")
		else:
			print "n is:  ",n,"\n"
			c.send("recieved")
			m=c.recv(1024)
			print "m is : " ,m,"\n"
			c.send("recieved")
			i=0
			j=0
			for i in range(int(n)):
				block=[]
				for j in range(int(m)):
					hi=c.recv(1024)
					block.append(hi)
					c.send("recieved")
				if check(block)==0:
					blocks.append(block)
			print "blocks",blocks
		n=c.recv(1024)
		if int(n)==0:
			c.send("not added vote")
		else:
			print "n is:  ",n,"\n"
			c.send("recieved")
			m=c.recv(1024)
			print "m is : " ,m,"\n"
			c.send("recieved")
			i=0
			j=0
			for i in range(int(n)):
				voteblock=[]
				for j in range(int(m)):
					hi=c.recv(1024)
					voteblock.append(hi)
					c.send("recieved")
				if vcheck(voteblock)==0:
					voteblocks.append(voteblock)
			print "voteblocks",voteblocks
	if choice=='5':
		c.send(voteprehash)
		print "sent voterprehash"
		c.recv(1024)
		print "recieved"
		vcount=len(voteblocks)+1
		c.send(str(vcount))
		print "sent votercount"
		print "sent prehash and count"
		voterhash=c.recv(1024)
		print "recieved new voterhash"
		found=fi(voterhash)
		if found==-1 or found==-2:
			if found==-1:
				c.send("false")
			if found==-2:
				print "vote alreday casted"
				c.send("falsevote")
		else:
			c.send("true")
			voterkey=c.recv(1024)
			print "recieved voterkey"
			if blocks[found][2]!=voterkey:
				print "not found pass match: ",blocks[found][2]
				c.send("false")
			else:
				c.send("true")
				data=c.recv(1024)
				print "vote data added hash is",data,"by addres",addr
				voteprehash=data
				arr=[vcount,data,addr,clientno]
				votehashes.append(arr)
				print "vote hash list",votehashes
	
	if choice=='6':
		co=0
		c.send("choice recieved")
		candidate=c.recv(1024)
		for x in voteblocks:
			if x[3]==candidate:
				co=co+1
		c.send(str(co))
	if choice=='7':
		if integretycheck()=='1':
			c.send("chain tampered")
		else:
			c.send("chain true")
			c.recv(1024)
			c.send(str(len(blocks)))
			c.recv(1024)
			c.send(str(len(voteblocks)))
	c.close()
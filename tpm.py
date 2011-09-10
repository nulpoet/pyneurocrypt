# Server program
import random
from socket import *
import threading
import sys

class TreeParityMachine ():
	""" ... """
	
	START_SYNC = 0
	SHARE_INPUT = 1
	SHARE_OUTPUT = 2
	DONE_SYNC = 3

	SYNC_COUNT_LIMIT = 100


	def __init__(self, K, L, N, myaddr, partner_addr_list, IS_MASTER):
		
		self.GOT_INPUT = False		
		self.iterations = 0		
		self.IS_MASTER = IS_MASTER
		self.sync_count = 0
		
		self.K = K
		self.L = L
		self.N = N

		self.w = []
		self.partner_addr_list = partner_addr_list
		
		self.other_outputs ={}		
		self.x = None
		
		for i in range(self.K) :
			l = []
			for j in range(self.N) :
				r = random.randint(-self.L, self.L)
				random.seed(r)
				l.append ( r )
#				l.append(1)
			self.w.append (l)


		# Set the socket parameters		
		self.buf = 10 + 2 * self.N * self.K
		self.myaddr = myaddr
		
		# Create socket and bind to address
		self.UDPSock = socket(AF_INET,SOCK_DGRAM)
		self.UDPSock.bind(self.myaddr)
		
#		self.sender_UDPSock = socket(AF_INET,SOCK_DGRAM)

		self.logfilename = "log_" + str( self.myaddr[1] ) 
		f = open (self.logfilename, 'w')
		f.close ()
		

		receiver_thread = threading.Thread(target=self.reciever, args=() ) 
		receiver_thread.start()

		
	def log(self, a):
		f = open (self.logfilename, 'a')
		f.write (str(self.myaddr) +" :: "+ str(a) + "\n")
		f.close()


	def generate_x (self):
		x = []
		for i in range(self.K) :
			l = []
			for j in range(self.N) :
				l.append ( random.randint(-self.L, self.L) )				
			x.append (l)
		
#		random.seed(x)
		
		self.x = x
#		self.log (str(self.myaddr) + " generated : " + str(self.x))
		
		self.compute()
		self.GOT_INPUT = True
		
		data_input = str(self.SHARE_INPUT) + " "
		for i in range(self.K) :
			for j in range(self.N) :
				data_input += str(self.x[i][j]) + ':'
				
		data_output = " ".join( [str(self.SHARE_OUTPUT), str(self.output)] )
		
		for addr in self.partner_addr_list :
			self.UDPSock.sendto(data_input, addr)			
		for addr in self.partner_addr_list :
			self.UDPSock.sendto(data_output, addr)

	def compute(self):
		
		self.iterations += 1
		
		self.output = 1
		self.sigmas = []
		
		for i in range(self.K) :
			locf = 0
			for j in range(self.N) :
				locf +=  self.w[i][j] * self.x[i][j]
			
			if locf > 0 :
				self.sigmas.append(1)
				self.output *= 1
			else :
				self.sigmas.append(-1)
				self.output *= -1
		
#		self.log( str((self.myaddr, self.x, self.w, self.sigmas)) )

	def theta(self, x, y):
		if x == y :
			return 1
		else :
			return 0
	
	
	def learn(self):
		""" ... """
		
		self.log ("\nHere\n")
		
		is_equal = 1
		for v in self.other_outputs.values() :
			if v != self.output :
				is_equal = 0
		
		if is_equal == 0 :
			self.log("  sync break at" + str(self.sync_count) + "\n'''''''''''''''''" )
			self.sync_count = 0
#			self.log( "-----------" + str(self.other_outputs) + " " + str(self.output) )
			return
		else :
			self.sync_count += 1
#			self.log( "-----------" + "is_equal 1")
			
			
			for i in range(self.K) :			
				for j in range(self.N) :
					delta_w = self.x[i][j] * self.theta(self.sigmas[i], self.output) * is_equal
					self.w[i][j] += delta_w
					
					if self.w[i][j] > self.L :
						self.w[i][j] =  self.L
					elif self.w[i][j] < -self.L :
						self.w[i][j] =  -self.L
			
#			self.log( str(self.myaddr) + " after leanring " + str(self.w) )
			
	
	def reciever(self):
		
		if self.IS_MASTER :
			self.generate_x()
			
		
		# Receive messages
		while 1:
			data,addr = self.UDPSock.recvfrom(self.buf)
			
			if not data:
				print "Client has exited!"
				break
			else:
				self.log(" received '" + str(data) + "' from " + str(addr) )				
				s = str(data)								
				if int(s[0]) == self.START_SYNC :
					self.master_addr = addr
					print "sync started"
				elif int(s[0]) == self.DONE_SYNC :
					print "sync done with key : " + str(self.w)
				elif int(s[0]) == self.SHARE_INPUT :
					s_list = s.split(' ')
					x_list = s_list[1].split(':')
					x = []
					cnt = 0
					#self.log(x_list)
					for i in range(self.K) :
						l = []
						for j in range(self.N) :							
							l.append ( int(x_list[cnt]) )							
							cnt+=1
						x.append(l)					
					self.x = x
					self.compute()					
					self.GOT_INPUT = True					
					data = " ".join( [str(self.SHARE_OUTPUT), str(self.output)] )					
					for addr in self.partner_addr_list :
#						self.sender_UDPSock.sendto(data, addr)
						self.UDPSock.sendto(data, addr)
				elif int(s[0]) == self.SHARE_OUTPUT :
					s_list = s.split(' ')
					self.other_outputs[ addr ] = int(s_list[1])
				else : 
					print "Invalid received message '", data,"'"
				
#				if self.IS_MASTER:
#					print self.other_outputs.keys(), self.partner_addr_list
				
				if is_unordered_equal(self.other_outputs.keys(), self.partner_addr_list):
					if self.GOT_INPUT == True:
						self.learn()
#					self.log( str(self.myaddr) + " after learning " + str(self.w) )						
						self.other_outputs = {}
						self.GOT_INPUT = False
						
						if self.sync_count == self.SYNC_COUNT_LIMIT:
							print "\n\n" + str(self.myaddr) + "\nSYNCED in "+str(self.iterations)+" iterations with key : \n**************\n" + str(self.w) + "\n**************\n"													
							sys.exit()
						elif self.IS_MASTER == True :
							self.generate_x()
					else:
						print self.myaddr, " SHARE_OUTPUTs recvd too early."
		
		
		# Close socket
		self.UDPSock.close()

def is_unordered_equal (l1, l2):	
	for x in l1:
		if not(x in l2):
			return False
	for x in l2:
		if not(x in l1):
			return False
	return True	
		
		
if __name__ == "__main__" :

#	addr_list = []
#	
#	addr_list.append(("127.0.0.1", 11111))
#	addr_list.append(("127.0.0.1", 22222))
#	addr_list.append(("127.0.0.1", 33333))
	
	
#	b = TreeParityMachine (
#						K=3, L=4, N=3,
#						myaddr = ("127.0.0.1", 22222),
#						partner_addr_list = [("127.0.0.1", 11111)], 
#						IS_MASTER = False
#					)
#
#	a = TreeParityMachine (
#						K=3, L=4, N=3,
#						myaddr = ("127.0.0.1", 11111),
#						partner_addr_list = [("127.0.0.1", 22222)], 
#						IS_MASTER = True
#					)
	
	
	b = TreeParityMachine (
						K=3, L=1, N=2,
						myaddr = ("127.0.0.1", 22222),
						partner_addr_list = [("127.0.0.1", 11111), ("127.0.0.1", 33333)], 
						IS_MASTER = False
					)
	c = TreeParityMachine (
						K=3, L=1, N=2,
						myaddr = ("127.0.0.1", 33333),
						partner_addr_list = [("127.0.0.1", 11111), ("127.0.0.1", 22222)], 
						IS_MASTER = False
					)

	a = TreeParityMachine (
						K=3, L=1, N=2,
						myaddr = ("127.0.0.1", 11111),
						partner_addr_list = [("127.0.0.1", 22222), ("127.0.0.1", 33333)], 
						IS_MASTER = True
					)


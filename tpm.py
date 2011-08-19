# Server program
import random
from socket import *
import threading

def log(a):
	print "[log] " + str(a)

class TreeParityMachine ():
	""" ... """
	
	START_SYNC = 0
	SHARE_INPUT = 1
	SHARE_OUTPUT = 2
	DONE_SYNC = 3

	SYNC_COUNT_LIMIT = 100

	def __init__(self, K, L, N, myaddr, partner_addr_list, IS_MASTER):
		
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

		receiver_thread = threading.Thread(target=self.reciever, args=() ) 
		receiver_thread.start()

		if self.IS_MASTER :
			self.generate_x()

	def generate_x (self):
		x = []		
		for i in range(self.K) :
			l = []
			for j in range(self.N) :
				l.append ( random.randint(-self.L, self.L) )				
			x.append (l)
		
#		random.seed(x)
		
		self.x = x
#		log (str(self.myaddr) + " generated : " + str(self.x))
		
		self.compute()
		
		data_input = str(self.SHARE_INPUT) + " "
		for i in range(self.K) :
			for j in range(self.N) :
				data_input += str(self.x[i][j]) + ':'
				
		data_output = " ".join( [str(self.SHARE_OUTPUT), str(self.output)] )
		
		for addr in self.partner_addr_list :
#			self.sender_UDPSock.sendto(data_input, addr)
#			self.sender_UDPSock.sendto(data_output, addr)
			self.UDPSock.sendto(data_input, addr)
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
		
#		log( str((self.myaddr, self.x, self.w, self.sigmas)) )

	def theta(self, x, y):
		if x == y :
			return 1
		else :
			return 0
	
	
	def learn(self):
		""" ... """
		
#		log ("\n----------- Here -----------\n")
		
		is_equal = 1
		for v in self.other_outputs.values() :
			if v != self.output :
				is_equal = 0
		
		if is_equal == 0 :
			log("'''''''''''''''\nsync break at \n'''''''''''''''''" + str(self.sync_count))
			self.sync_count = 0
#			log( "-----------" + str(self.other_outputs) + " " + str(self.output) )
			return
		else :
			self.sync_count += 1
#			log( "-----------" + "is_equal 1")
			
			
			for i in range(self.K) :			
				for j in range(self.N) :
					delta_w = self.x[i][j] * self.theta(self.sigmas[i], self.output) * is_equal
					self.w[i][j] += delta_w
					
					if self.w[i][j] > self.L :
						self.w[i][j] =  self.L
					elif self.w[i][j] < -self.L :
						self.w[i][j] =  -self.L
			
#			log( str(self.myaddr) + " after leanring " + str(self.w) )
			
	
	def reciever(self):
		
		
		# Receive messages
		while 1:
			data,addr = self.UDPSock.recvfrom(self.buf)
			
			if not data:
				print "Client has exited!"
				break
			else:		
				
#				log( str(self.myaddr) + " received '" + str(data) + "' from " + str(addr) )
				
				s = str(data)
				
				if int(s[0]) == self.START_SYNC :
					self.master_addr = addr
					print "sync started"
					continue
					
				elif int(s[0]) == self.DONE_SYNC :
					print "sync done with key : " + str(self.w)
					continue
					
				elif int(s[0]) == self.SHARE_INPUT :
					s_list = s.split(' ')
					x_list = s_list[1].split(':')
					x = []
					cnt = 0
					#log(x_list)
					for i in range(self.K) :
						l = []
						for j in range(self.N) :
							l.append ( int(x_list[cnt]) )							
							cnt+=1
						x.append(l)
					
					self.x = x
					self.compute()
					
					data = " ".join( [str(self.SHARE_OUTPUT), str(self.output)] )
					
					for addr in self.partner_addr_list :
#						self.sender_UDPSock.sendto(data, addr)
						self.UDPSock.sendto(data, addr)
						
					continue
						
				elif int(s[0]) == self.SHARE_OUTPUT :
					s_list = s.split(' ')
					self.other_outputs[ addr ] = int(s_list[1])
					
					
#					log( "self.other_outputs.keys() :: " + str(type(self.other_outputs.keys())) + str(self.other_outputs.keys()) )
#					log( "self.partner_addr_list :: " + str(type(self.partner_addr_list)) + str(self.partner_addr_list) )
					
					if self.other_outputs.keys() == self.partner_addr_list :
						self.learn()
#					log( str(self.myaddr) + " after learning " + str(self.w) )
					self.x = None
					self.other_outputs = {}
					
					if self.sync_count == self.SYNC_COUNT_LIMIT :		
						print "\n\n" + str(self.myaddr) + "\nSYNCED in "+str(self.iterations)+" iterations with key : \n**************\n" + str(self.w) + "\n**************\n"
						data = str(self.DONE_SYNC)
						for addr in self.partner_addr_list :
#							self.sender_UDPSock.sendto( data, addr)						
							self.UDPSock.sendto( data, addr)
							
						break
					elif self.IS_MASTER == True :
						self.generate_x()
					
					continue
				else : 
					print "Invalid received message '", data,"'"
		
		
		# Close socket
		self.UDPSock.close()
		
		
		
if __name__ == "__main__" :

	addr_list = []
	
	addr_list.append(("127.0.0.1", 11111))
	addr_list.append(("127.0.0.1", 22222))
	addr_list.append(("127.0.0.1", 33333))

#	a = TreeParityMachine (3,4,3, 
#						("127.0.0.1", 11111), 
#						[("127.0.0.1", 22222)], 
#						IS_MASTER=False
#					)
#	b = TreeParityMachine (3,4,3, 
#						("127.0.0.1", 22222),
#						[("127.0.0.1", 11111)], 
#						IS_MASTER=True
#					)

	
	a = TreeParityMachine (1,1,3, 
						("127.0.0.1", 11111), 
						[("127.0.0.1", 22222), ("127.0.0.1", 33333)], 
						IS_MASTER=False
					)
	b = TreeParityMachine (1,1,3, 
						("127.0.0.1", 22222), 
						[("127.0.0.1", 11111), ("127.0.0.1", 33333)], 
						IS_MASTER=False
					)
	c = TreeParityMachine (1,1,3, 
						("127.0.0.1", 33333), 
						[("127.0.0.1", 11111), ("127.0.0.1", 22222)], 
						IS_MASTER=True
					)
	

	"""	
	x = a.generate_x()
	print a.w
	print x
	a.learn(x, 1)
	print "----"
	print a.w
	"""

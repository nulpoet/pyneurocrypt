# Server program
import random
from socket import *
import threading

class TreeParityMachine() :
	""" ... """
	
	START_SYNC = 0
	SHARE_INPUT = 1
	SHARE_OUTPUT = 2
	DONE_SYNC = 3

	SYNC_COUNT_LIMIT = 100

	def __init__(self, K, L, N, myaddr, partner_addr_list, IS_MASTER):
		
		self.IS_MASTER = IS_MASTER
		self.sync_count = 0
		
		self.K = K
		self.L = L
		self.N = N

		self.w = []
		self.partner_addr_list = partner_addr_list
		
		self.other_outputs ={}		
		self.x = None
		
		for x in range(self.N) :
			l = []
			for y in range(self.K) :
				l.append ( random.randint(-self.L, self.L) )
			self.w.append (l)


		# Set the socket parameters		
		self.buf = 10 + 2 * self.N * self.K
		self.myaddr = myaddr
		
		# Create socket and bind to address
		self.UDPSock = socket(AF_INET,SOCK_DGRAM)
		self.UDPSock.bind(self.myaddr)
		
		self.sender_UDPSock = socket(AF_INET,SOCK_DGRAM)

		receiver_thread = threading.Thread(target=self.reciever, args=() ) 
		receiver_thread.start()

	def generate_x (self):
		x = []		
		for i in range(self.N) :
			l = []
			for j in range(self.K) :
				l.append ( random.randint(-self.L, self.L) )
			x.append (l)
		
		self.x = x
		self.compute(x)
		
		data_input = ""
		for i in range (self.N) :
			for j in range(self.K) :
				data_input += ':'+ str(self.w[i][j])
				
		data_output = " ".join( str(self.SHARE_OUTPUT), str(self.output))
		
		for addr in self.partner_addr_list :
			self.sender_UDPSock.sendto(data_input, addr)
			self.sender_UDPSock.sendto(data_output, addr)


	def compute(self):
		
		self.output = 1
		self.sigmas = []
		
		for i in range(self.N) :
			locf = 0
			for j in range(self.K) :
				locf +=  self.w[i][j] * self.x[i][j]
			
			if locf > 0 :
				self.sigmas.append(1)
				self.output *= 1
			else :
				self.sigmas.append(-1)
				self.output *= -1
		

	def theta(self, x, y):
		if x == y :
			return 1
		else :
			return 0
	
	
	def learn(self):
		""" ... """
		
		is_equal = 1
		for v in self.other_outputs.values() :
			 if v != self.output :
			 	is_equal = 0
		
		if is_equal == 0 :
			self.sync_count = 0
		else :
			self.sync_count += 1
		
		for i in range(self.N) :			
			for j in range(self.K) :
				delta_w = self.x[i][j] * self.theta(self.sigmas[i], self.output) * is_equal
				self.w[i][j] += delta_w
				
				if self.w[i][j] > self.L :
					self.w[i][j] =  self.L
				elif self.w[i][j] < -self.L :
					self.w[i][j] =  -self.L
	
	
	def reciever(self):
		
		
		# Receive messages
		while 1:
			data,addr = self.UDPSock.recvfrom(self.buf)
			
			if not data:
				print "Client has exited!"
				break
			else:		
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
					for i in range(self.N) :
						l = []
						for j in range(self.K) :
							l.append ( int(x_list[cnt]) )							
							cnt+=1
						x.append(l)
					
					self.x = x
					self.compute(x)
					
					data = " ".join( str(self.SHARE_OUTPUT), str(self.output))
					
					for addr in self.partner_addr_list :
						self.sender_UDPSock.sendto(data, addr)
						
				elif int(s[0]) == self.SHARE_OUTPUT :
					s_list = s.split(' ')
					self.other_outputs[ addr ] = int(s_list[1])
					
					if self.other_outputs.keys() == self.partner_addr_list :
						self.learn()
					
					self.x = None
					self.other_outputs = {}
					
					if self.sync_count == self.SYNC_COUNT_LIMIT :		
						print str(self.myaddr) + " SYNCED with key : " + str(self.w)
						data = str(self.DONE_SYNC)
						for addr in self.partner_addr_list :
							self.sender_UDPSock.sendto( data, addr)						
					elif self.IS_MASTER == True :
						self.generate_x()
						
				else : 
					print "Invalid received message '", data,"'"
		
		
		# Close socket
		self.UDPSock.close()
		
		
		
if __name__ == "__main__" :

	addr_list = []
	
	addr_list.append(("localhost", 11111))
	addr_list.append(("localhost", 22222))
	addr_list.append(("localhost", 33333))
	
	a = TreeParityMachine (3,5,2, addr_list[0], addr_list.remove(addr_list[0]), IS_MASTER=True)
	b = TreeParityMachine (3,5,2, addr_list[0], addr_list.remove(addr_list[0]), IS_MASTER=False)
	c = TreeParityMachine (3,5,2, addr_list[0], addr_list.remove(addr_list[0]), IS_MASTER=False)

	"""	
	x = a.generate_x()
	print a.w
	print x
	a.learn(x, 1)
	print "----"
	print a.w
	"""

# Server program
import random
from socket import *


class TreeParityMachine() :
	""" ... """

	def __init__(self, K, L, N):
		self.K = K
		self.L = L
		self.N = N

		self.w = []
		
		for x in range(self.N) :
			l = []
			for y in range(self.K) :
				l.append ( random.randint(-self.L, self.L) )
			self.w.append (l)


	def generate_x (self):
		x = []		
		for i in range(self.N) :
			l = []
			for j in range(self.K) :
				l.append ( random.randint(-self.L, self.L) )
			x.append (l)
		
		return x


	def compute(self, x):
		
		output = 1
		sigmas = []
		
		for i in range(self.N) :
			locf = 0
			for j in range(self.K) :
				locf +=  self.w[i][j] * x[i][j]
			
			if locf > 0 :
				sigmas.append(1)
				output *= 1
			else :
				sigmas.append(-1)
				output *= -1
		
		return output, sigmas


	def theta(self, x, y):
		if x == y :
			return 1
		else :
			return 0
	
	
	def learn(self, x, other_output):
		""" ... """
		
		output, sigmas = self.compute(x)		
		#print output, sigmas

		for i in range(self.N) :			
			for j in range(self.K) :
				delta_w = x[i][j] * self.theta(sigmas[i], output) * self.theta(output, other_output)
				self.w[i][j] += delta_w
				
				if self.w[i][j] > self.L :
					self.w[i][j] =  self.L
				elif self.w[i][j] < -self.L :
					self.w[i][j] =  -self.L

		
if __name__ == "__main__" :
	
	a = TreeParityMachine(3,5,2)
	x = a.generate_x()
	print a.w
	print x
	a.learn(x, 1)
	print "----"
	print a.w
	
"""
# Set the socket parameters
host = "localhost"
port = 21567
buf = 1024
addr = (host,port)

# Create socket and bind to address
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)

# Receive messages
while 1:
	data,addr = UDPSock.recvfrom(buf)
	if not data:
		print "Client has exited!"
		break
	else:
		print "\nReceived message '", data,"'"


# Close socket
UDPSock.close()

"""
# Server program
import random
from socket import *
import threading
import sys
import time
import __builtin__

import config
import query

class TreeParityMachine ():
    """ ... """
    
    START_SYNC = 0
    SHARE_INPUT = 1
    SHARE_OUTPUT = 2
    DONE_SYNC = 3
#    INPUT_REQUEST

    MSG_TYPE = {
                0 : 'START_SYNC',
                1 : 'SHARE_INPUT',
                2 : 'SHARE_OUTPUT',
                3 : 'DONE_SYNC'
            }
    
    #TODO: SHould be function of N, K, L
    SYNC_COUNT_LIMIT = 100


    def __init__(self, K, L, N, myaddr, partner_addr_list, master_addr, shared_clock_wrapper, sync_algo, H, debug):
        self.debug = debug
        self.EXTRA_DEBUG = False
        self.shared_clock_wrapper = shared_clock_wrapper
        
        self.GOT_INPUT = False        
        self.iterations = 0
        self.sync_algo = sync_algo
        self.H = H
        self.sync_count = 0
#        self.last_recieved_input_from = None
        self.partner_addr_list = partner_addr_list
        self.myaddr = myaddr
        self.master_addr = master_addr
        if self.master_addr == self.myaddr: 
            self.IS_MASTER = True
        else:
            self.IS_MASTER = False

        self.addr_list = list(self.partner_addr_list)
        self.addr_list.append(self.myaddr)
        self.addr_list.sort()
        
        self.K = K
        self.L = L
        self.N = N
        
        self.w = []
        self.partner_ws = {}
        
        self.other_outputs = {}        
        self.x = None
        
        for i in range(self.K):
            l = []
            for j in range(self.N):
                r = random.randint(-self.L, self.L)
#                random.seed(r)
                l.append(r)
#                l.append(1)
            self.w.append(l)


        # Set the socket parameters        
        self.buf = 10 + 3 * self.N * self.K
                
        # Create socket and bind to address
        self.UDPSock = socket(AF_INET, SOCK_DGRAM)
        self.UDPSock.bind(('', self.myaddr[1]))
        
        self.sender_UDPSock = socket(AF_INET, SOCK_DGRAM)

        self.logfilename = "log_" + str(self.myaddr[1]) 
        f = open (self.logfilename, 'w')
        f.close ()
        
    def start(self):
        self.receiver_thread = threading.Thread(target=self.reciever, args=()) 
        self.receiver_thread.start()
        
        print """
        Started tpm with
            myaddr : {0}
            partner_addr_list : {1}
            IS_MASTER : {2}
            K : {3}
            L : {4}
            N : {5}
            H : {6}
            sync_algo : {7}
        """.format (self.myaddr, self.partner_addr_list, self.IS_MASTER, self.K, self.L, self.N, self.H, self.sync_algo)
        
    def log(self, a):
        self.shared_clock_wrapper[0] += 1
        f = open (self.logfilename, 'a')
        s = '{0} - {1} > {2}'.format (self.shared_clock_wrapper[0], self.myaddr, a)
#        print s
        f.write(s + '\n')
        f.close()
    
    def generate_plain_x(self):        
        x = []
        for i in range(self.K) :
            l = []
            for j in range(self.N):
                temp = random.randint(0, 1)
                if temp == 0:
                    l.append(-1)
                else:
                    l.append(1)
            x.append(l)
        return x

    def generate_query_x(self):
        x = []
        for i in range(self.K) :
            x_i = query.generate_x_k(self.N, self.L, self.H, self.w[i])
            x.append(x_i)
        return x

    def generate_x (self):
        
#        print self.myaddr, ' generating x'
        if self.sync_algo == 'queries':
            x = self.generate_query_x()
        else:
            x = self.generate_plain_x()
#            x = self.generate_query_x()
        
        self.log('I generated input {0}'.format(x))
#        random.seed(x)
        
        self.x = x
        self.compute()        
        self.log('I computed output')                
        
        self.GOT_INPUT = True
        if self.sync_algo == 'queries':
            self.switch_master()
        
        data_input = str(self.SHARE_INPUT) + " "

        for i in range(self.K):
            for j in range(self.N):
                data_input += str(self.x[i][j]) + ':'

#        print "data_input : ", data_input

        data_output = " ".join([str(self.SHARE_OUTPUT), str(self.output)])
        
        for addr in self.partner_addr_list:
            self.sender_UDPSock.sendto(data_input, addr)
        for addr in self.partner_addr_list:
            self.sender_UDPSock.sendto(data_output, addr)

    def compute(self):
        
        self.iterations += 1
        if self.iterations <= 1000:
            if self.iterations % 100 == 0:
                print '..', self.iterations, '..'
        elif self.iterations <= 10000:
            if self.iterations % 1000 == 0:
                print '..', self.iterations, '..'
        else:
            if self.iterations % 10000 == 0:
                print '..', self.iterations, '..'
                
        self.output = 1
        self.sigmas = []
        
        for i in range(self.K) :
            locf = 0
            for j in range(self.N) :
                locf += self.w[i][j] * self.x[i][j]
            
            if locf > 0 :
                self.sigmas.append(1)
                self.output *= 1
            else :
                self.sigmas.append(-1)
                self.output *= -1
        
        if self.EXTRA_DEBUG == True:
            s = '{0} given x:{1} with w:{2} gave sigmas:{3} outputed:{4}'.format (self.myaddr, self.x, self.w, self.sigmas, self.output)
            print(s)
            time.sleep(1)

    def theta(self, x, y):
        if x == y :
            return 1
        else :
            return 0
    
    
    def learn(self):
        """ ... """
        
#        self.log ("\nHere\n")
        
        is_equal = 1
        for v in self.other_outputs.values() :
            if v != self.output :
                is_equal = 0
        
        if is_equal == 0 :
            self.log("  sync break at" + str(self.sync_count) + "\n'''''''''''''''''")
            self.sync_count = 0
#            self.log( "-----------" + str(self.other_outputs) + " " + str(self.output) )
            return
        else :
            self.sync_count += 1
#            self.log( "-----------" + "is_equal 1")
            
            
            for i in range(self.K):            
                for j in range(self.N):
                    delta_w = self.x[i][j] * self.theta(self.sigmas[i], self.output) * is_equal
                    self.w[i][j] += delta_w
                    
                    if self.w[i][j] > self.L:
                        self.w[i][j] = self.L
                    elif self.w[i][j] < -self.L:
                        self.w[i][j] = -self.L
            
#            self.log( str(self.myaddr) + " after leanring " + str(self.w) )
    
        
    def switch_master(self):
        
#        return
        
        i = self.addr_list.index(self.master_addr)
        new_i = (i + 1) % len(self.addr_list)
        self.master_addr = self.addr_list[new_i]
        if self.master_addr == self.myaddr:
            self.IS_MASTER = True
        else:
            self.IS_MASTER = False
    
        self.log('I switched master to {0}'.format (self.master_addr))
        
    
    def reciever(self):
        
#        import time
#        s = '.'
#        while True:
#            time.sleep(1)
#            print s
#            s += '.'
            
        
        if self.IS_MASTER :
            self.generate_x()
            
        
        # Receive messages
        while 1:
            data, addr = self.UDPSock.recvfrom(self.buf)
            
            if not data:
                print "Client has exited!"
                break
            
            else:
#                print " received '" + str(data) + "' from " + str(addr)
                l = str(data).split() 
                msg_type = int(l[0])
                try:
                    msg_val = l[1]
                except IndexError:
                    msg_val = None
                    
                self.log("Received {0} from {1} with val {2}".format (self.MSG_TYPE[msg_type], addr, msg_val))
                
#                s = str(data)
#                print "s : ", s
                
#                if msg_type == self.START_SYNC :
#                    self.master_addr = addr
#                    print "sync started"
                
                if msg_type == self.DONE_SYNC :
#                    print "sync done with key : " + str(self.w)
                    s = 'I synced in {0} iterations with w = {1}'.format (self.iterations, self.w)
                    self.log(s)
                    print "\n", self.myaddr, "SYNCED in " + str(self.iterations) + " iterations\n"# with key : \n" + str(self.w) + "\n"
                    sys.exit()
                
                elif msg_type == self.SHARE_INPUT :
#                    print '---------- Recieved inpout from ', addr
#                    self.last_recieved_input_from = addr
                    if self.sync_algo == 'queries':
                        self.switch_master()
                    
#                    s_list = s.split(' ')
#                    x_list = s_list[1].split(':')
                    x_list = msg_val.split(':')
                    
#                    print "s_list : ", s_list
#                    print "x_list : ", x_list
                    
                    x = []
                    cnt = 0
                    #self.log(x_list)
                    for i in range(self.K):
                        l = []
                        for j in range(self.N):                            
                            l.append (int(x_list[cnt]))                            
                            cnt += 1
                        x.append(l)                    
                    self.x = x
                    self.compute()
                                    
                    self.GOT_INPUT = True
                                        
                    data = " ".join([str(self.SHARE_OUTPUT), str(self.output)])                    
                    for addr in self.partner_addr_list:
#                        self.sender_UDPSock.sendto(data, addr)
                        self.sender_UDPSock.sendto(data, addr)
                        
                elif msg_type == self.SHARE_OUTPUT:
#                    s_list = s.split(' ')
#                    output = s_list[1]
                    output = int(msg_val)
                    self.other_outputs[addr] = output
                else: 
                    print 'Invalid received message {0}'.format (data)
                
#                if self.IS_MASTER:
#                    print self.other_outputs.keys(), self.partner_addr_list
                
                if is_unordered_partner_list_equal (self.other_outputs.keys(), self.partner_addr_list):
                    if self.GOT_INPUT == True:
                        self.learn()
                        self.log('I learned')
#                    self.log( str(self.myaddr) + " after learning " + str(self.w) )                        
                        self.other_outputs = {}
                        self.GOT_INPUT = False
                        
                        is_synced = None
                        if __builtin__.local:
                            self.log('comparing {0} - {1}'.format (self.w, self.partner_ws))
                            is_synced = True
                            for p_w in self.partner_ws.values():
                                if self.w != p_w:
                                    is_synced = False                            
                        else:
                            is_synced = self.sync_count == self.SYNC_COUNT_LIMIT
                        
                        if is_synced:
#                        if self.sync_count == self.SYNC_COUNT_LIMIT:
                            s = 'I synced in {0} iterations with w = {1}'.format (self.iterations, self.w)
                            self.log(s)
                            print "\n", self.myaddr, "SYNCED in " + str(self.iterations) + " iterations\n"# with key : \n" + str(self.w) + "\n"
                            
#                            self.EXTRA_DEBUG = True

                            done_sync_msg = str(self.DONE_SYNC)        
                            for addr in self.partner_addr_list :
                                self.sender_UDPSock.sendto(done_sync_msg, addr)
                            
                            sys.exit()
                        
                        if self.IS_MASTER == True:
                            self.generate_x()
                        
                    else:
                        self.log('SHARE_OUTPUTs recvd too early')
#                        print self.myaddr, " SHARE_OUTPUTs recvd too early."
        
        
        # Close socket
        self.UDPSock.close()

def is_unordered_partner_list_equal (l1, l2):
    
    if __builtin__.local:
        return len(l1) == len(l2)    # ports are diffrent and thus aadrs are random.. no security risk in comparing length only since its local only
    
    tl1 = []
    tl2 = []
    for x in l1:
        tl1.append(x[0])
    for x in l2:
        tl2.append(x[0])
        
    for x in tl1:
        if not(x in tl2):
            return False
    for x in tl2:
        if not(x in tl1):
            return False
    return True    


def localtest():
    
    # testing 3 TPMs    
    __builtin__.local = True
    
    shared_clock_wrapper = [0]
    
    b = TreeParityMachine (
                        config.K, config.L, config.N,
                        ("localhost", 22222),
                        [("localhost", 11111), ("localhost", 33333)],
                        ("localhost", 11111),
                        shared_clock_wrapper[0],
                        'plain',
                        0.7                        
                    )
    c = TreeParityMachine (
                        config.K, config.L, config.N,
                        ("", 33333),
                        [("localhost", 11111), ("localhost", 22222)],
                        ("localhost", 11111),
                        shared_clock_wrapper[0],
                        'plain',
                        0.7
                    )

    a = TreeParityMachine (
                        config.K, config.L, config.N,
                        ("localhost", 11111),
                        [("localhost", 22222), ("localhost", 33333)],
                        ("localhost", 11111),
                        shared_clock_wrapper[0],
                        'plain',
                        0.7
                    )
    
    b.start()
    c.start()
    
    a.start()
    
    while threading.activeCount() > 1:
        time.sleep(1)
    
    print " ~~~~~~~~~~~~~~ FINISH ~~~~~~~~~~~~~~ " 
    
    

if __name__ == "__main__" :
    localtest()

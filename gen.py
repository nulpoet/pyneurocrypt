import sys
import __builtin__
import threading
import time

from tpm import TreeParityMachine
import config

class Generator():
    
    def __init__(self, I, N_machines=config.N_machines, K=config.K, L=config.L, N=config.N, sync_algo='plain'):
        
        __builtin__.local = True
        
        self.shared_clock = 0
        
        self.I = I
        self.N_machines = N_machines
        self.K = K
        self.L = L
        self.N = N
        
        self.sync_algo = sync_algo
        
        self.tpm_list = []
        
        self.port_base = 10001
        self.ports = []
        
        self.iterations_list = []
    
    
    def run(self):
        for i in range(self.N_machines):
            self.ports.append(self.port_base + i)
        
        print 'ports : ', self.ports
        
        for i in range(self.I):
            iterations = self.sync()
            print i, ' > ', iterations
            self.iterations_list.append(iterations)
        
        print '>>>>> iterations_list : ', self.iterations_list 
        
    def sync(self):
        
        master_addr = ("localhost", self.port_base)
        
        for i in range(1, self.N_machines):
            port = self.port_base + i
            self.start_machine(port, master_addr)
        
        # Master is started last
        self.start_machine(self.port_base, master_addr)
        
        while threading.activeCount()>1:
            time.sleep(2)
        
        iterations = self.tpm_list[-1].iterations
        self.tpm_list = []
        return iterations
         

        
            
    def start_machine(self, port, master_addr):
        myport = port
        port_list = list(self.ports)
        port_list.remove(myport)
        partner_addr_list = []
        for p in port_list:
            partner_addr_list.append( ('localhost', p) )  
        myaddr = ("localhost", myport)
        
        print 'starting tpm with ', ("", myport), partner_addr_list
        
        tpm = TreeParityMachine (
                        self.K, self.L, self.N,
                        myaddr,
                        partner_addr_list, 
                        master_addr,
                        self.shared_clock,
                        self.sync_algo
                    )
        self.tpm_list.append(tpm)


if __name__ == "__main__" :
        
    args = sys.argv
    sync_algo = 'plain'
    print args
    try:
        args.pop(0)
        if args[0] == '-q':
            args.pop(0)
            sync_algo = 'queries'
    except:
        pass
    
    print args
    if not (len(args)==1 or len(args)==2 or len(args)==5):
        print """ usage : gen.py [-q] I [<N_machines> <K> <L> <N>] """
    elif len(args) == 1:
        I = int(args[0])
        g = Generator(I, sync_algo=sync_algo)
        g.run()
    elif len(args) == 2:
        I = int(args[0])
        N_machines = int(args[1])
        g = Generator(I, N_machines=N_machines, sync_algo=sync_algo)
        g.run()
    elif len(args) == 5: 
        g = Generator( int(args[0]) ,N_machines=int(args[1]), K=int(args[2]), L=int(args[3]), N=int(args[4]), sync_algo=sync_algo )
        g.run()
    else:
        print '~~~~~~~~~~ IMPOSSIBLE CASE ~~~~~~~~~~'
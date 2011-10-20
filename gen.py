import sys
import __builtin__
from tpm import TreeParityMachine
import config

class Generator():
    
    def __init__(self, N_machines, K=config.K, L=config.L, N=config.N):
        
        __builtin__.local = True
        
        self.N_machines = N_machines
        self.K = K
        self.L = L
        self.N = N
        
        self.tpm_list = []
        
        self.port_base = 10001
        self.ports = []
    
    
    def run(self):        
        for i in range(self.N_machines):
            self.ports.append(self.port_base + i)
        
        print 'ports : ', self.ports
        
        for i in range(1, self.N_machines):
            port = self.port_base + i
            self.start_machine(port, master=False)
        
        # Master is started last
        self.start_machine(self.port_base, master=True)
        
            
    def start_machine(self, port, master=False):
            myport = port
            port_list = list(self.ports)
            port_list.remove(myport)
            partner_addr_list = []
            for p in port_list:
                partner_addr_list.append( ('localhost', p) )  
            
            print 'starting tpm with ', ("", myport), partner_addr_list
            
            tpm = TreeParityMachine (
                            self.K, self.L, self.N,
                            myaddr = ("", myport),
                            partner_addr_list = partner_addr_list, 
                            IS_MASTER = master
                        )
            self.tpm_list.append(tpm)


if __name__ == "__main__" :
        
    args = sys.argv    
    if not (len(args) == 2 or len(args) == 5):
        print """ usage : gen.py <N_machines> [<K> <L> <N>] """
    elif len(args) == 2:
        g = Generator( int(args[1]) )
        g.run()
    elif len(args) == 5: 
        g = Generator( int(args[1]), K=int(args[2]), L=int(args[3]), N=int(args[4]) )
        g.run()
    else:
        print '~~~~~~~~~~ IMPOSSIBLE CASE ~~~~~~~~~~'
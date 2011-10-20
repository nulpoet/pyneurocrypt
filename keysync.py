import sys
from tpm import TreeParityMachine
import config

if __name__ == "__main__" :
    
    myaddr = ("", config.port)
    partner_addr_list = []
    IS_MASTER = False    
    
    args = sys.argv    
    if len(args) == 0:
        print """ usage : tpm.py [-m] <IP addr 1> <IP addr 2> ... """
    for x in args[1:]:
        if x == '-m':
            IS_MASTER = True
            continue
        else:
            partner_addr_list.append((x, config.port))
        
    t = TreeParityMachine (
                        K=config.K, 
                        L=config.L,
                        N=config.N,
                        myaddr = myaddr,
                        partner_addr_list = partner_addr_list, 
                        IS_MASTER = IS_MASTER
                    )



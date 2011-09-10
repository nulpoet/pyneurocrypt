import sys
import __builtin__

from tpm import TreeParityMachine
import config


def localtest():
    
    # testing 3 TPMs    
    __builtin__.local = True
    
    b = TreeParityMachine (
                        K=config.K, L=config.L, N=config.N,
                        myaddr = ("", 22222),
                        partner_addr_list = [("localhost", 11111), ("localhost", 33333)], 
                        IS_MASTER = False
                    )
    c = TreeParityMachine (
                        K=config.K, L=config.L, N=config.N,
                        myaddr = ("", 33333),
                        partner_addr_list = [("localhost", 11111), ("localhost", 22222)], 
                        IS_MASTER = False
                    )

    a = TreeParityMachine (
                        K=config.K, L=config.L, N=config.N,
                        myaddr = ("", 11111),
                        partner_addr_list = [("localhost", 22222), ("localhost", 33333)], 
                        IS_MASTER = True
                    )

if __name__ == "__main__" :
    localtest()
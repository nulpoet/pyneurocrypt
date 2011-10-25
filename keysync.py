#!/usr/bin/env python

import sys
import __builtin__
import threading
import time
import random
import json

from tpm import TreeParityMachine
import config

class KeySync():
    
    def __init__(self, am_i_master, iplist, myip, port, K, L, N, sync_algo, H, debug):
        
        __builtin__.local = False
        
        self.shared_clock_wrapper = [0]
        
        self.am_i_master = am_i_master
        self.iplist = iplist
        self.myip = myip
        self.port = port
        self.K = K
        self.L = L
        self.N = N
        self.sync_algo = sync_algo
        self.H = H
        
        self.tpm_list = []

    def run(self):
        
        random.seed(time.localtime())
        
        self.sync()
        

        
    def sync(self):
        
        myaddr = (self.myip, self.port)
        
        partner_addr_list = []
        for p_ip in self.iplist:
            partner_addr_list.append( (p_ip, self.port) )
        
        master_addr = None
        if self.am_i_master:
            master_addr = myaddr
        
        
        tpm = TreeParityMachine (
                    self.K, self.L, self.N,
                    myaddr,
                    partner_addr_list,
                    master_addr,
                    self.shared_clock_wrapper,
                    self.sync_algo,
                    self.H,
                    debug
                )
        tpm.start()
        
        while threading.activeCount()>1:
            time.sleep(1)
        
        return

if __name__ == "__main__" :
    
    args = sys.argv
    
    myip = config.myip
    iplist = config.iplist
    am_i_master = False
    
    port = config.port
    K = config.K
    L = config.L
    N = config.N    
    sync_algo = config.sync_algo
    H = config.H
    res = config.res
    debug = config.debug
     
    args.pop(0)
    for arg in args:
        l = arg.split('=')
        if l[0] == '-q':
            sync_algo = 'queries'
        elif l[0] == '-H':
            H = float(l[1])        
        elif l[0] == '-m':
            am_i_master = True
        elif l[0] == '-K':
            K = int(l[1])
        elif l[0] == '-L':
            L = int(l[1])
        elif l[0] == '-N':
            N = int(l[1])
        elif l[0] == '-res':
            res = l[1]
        elif l[0] == '-d':
            debug = True
        elif l[0] == '-p':
            port = int(l[1])
        elif l[0] == '-h':
            print """ usage : localtest.py [-h] [-d] [-q [-H=[H]]] [-m] [-K=<K>] [-L=<L>] [-N=<N>] """
            sys.exit()
        else:
            print """ usage : localtest.py [-q [-H=[H]]] [-m] [-K=<K>] [-L=<L>] [-N=<N>] """
            sys.exit()
    
    ks = KeySync( am_i_master, iplist, myip, port, K, L, N, sync_algo, H, debug)
    ks.run()
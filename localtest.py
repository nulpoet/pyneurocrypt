#!/usr/bin/env python

import sys
import __builtin__
import threading
import time
import random
import json

from tpm import TreeParityMachine
import config

class LocalTest():
    
    def __init__(self, M, K, L, N, sync_algo, H, debug, port_base):
        
        __builtin__.local = True
        
        self.shared_clock_wrapper = [0]

        self.M = M
        self.K = K
        self.L = L
        self.N = N
        self.sync_algo = sync_algo
        self.H = H
        
        self.tpm_list = []
        
        self.port_base = port_base
        self.ports = []
        
#        self.iterations_list = []


    def run(self):
        
#        f_res = open(res, 'a')
#        f_res.write('Started at ' + time.asctime(time.localtime())+' ...   \n')
#        f_res.close()
        
        random.seed(time.localtime())
        for i in range(self.M):
            self.ports.append(self.port_base + i)
        
#        print 'ports : ', self.ports
        
        self.sync()
        
#        for i in range(self.I):
#            iterations = self.sync()
#            print i, '-> ', iterations
#            self.iterations_list.append(iterations)
#            print '--> iterations_list : ', self.iterations_list
#            print '\n-------------------------------------------------------------------\n'
            
        
#        avg_iters = float(sum(self.iterations_list))/len(self.iterations_list)
#        print '>>>>> iterations_list : ', self.iterations_list
#        print '>>>>> average iterations : ', avg_iters
#                
#        f_res = open(res, 'a')
#        
#        d = {}
#        d['algo'] = self.sync_algo
#        d['H'] = self.H
#        d['avg'] = avg_iters
#        d['M'] = self.M
#        d['K'] = self.K
#        d['L'] = self.L
#        d['N'] = self.N
#        d['I'] = self.I
#        
#        f_res.write(json.dumps(d, indent=4)+'\n')
#        f_res.write( '........ended at ' + time.asctime(time.localtime())+'\n\n')
#        f_res.close()
        
    def sync(self):
        
        master_addr = ("localhost", self.port_base)
        print ''
        
        for i in range(self.M):
            myport = self.port_base + i
            port_list = list(self.ports)
            port_list.remove(myport)
            partner_addr_list = []
            for p in port_list:
                partner_addr_list.append( ('localhost', p) )
            myaddr = ("localhost", myport)
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
            self.tpm_list.append(tpm)
        
        for i in range(self.M):
            partner_indexes = range(self.M)
            partner_indexes.pop(i)
            
            for p_i in partner_indexes:
                p_w = self.tpm_list[p_i].w
                self.tpm_list[i].partner_ws[p_i] = p_w
        
        for i in range(1, self.M):            
            self.tpm_list[i].start()
#            port = self.port_base + i
#            self.start_machine(port, master_addr)
        
        # Master is started last
        self.tpm_list[0].start()
#        self.start_machine(self.port_base, master_addr)
        
        while threading.activeCount()>1:
            time.sleep(1)
        
        iterations = self.tpm_list[-1].iterations
        self.tpm_list = []
        return iterations

if __name__ == "__main__" :
    
    args = sys.argv
        
    M = config.M
    K = config.K
    L = config.L
    N = config.N    
    sync_algo = config.sync_algo
    H = config.H
    res = config.res
    debug = config.debug
    port_base = config.port_base
     
    args.pop(0)
    for arg in args:
        l = arg.split('=')
        if l[0] == '-q':
            sync_algo = 'queries'
        elif l[0] == '-H':
            H = float(l[1])        
        elif l[0] == '-M':
            M = int(l[1])
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
            port_base = int(l[1])
        elif l[0] == '-h':
            print """ usage : localtest.py [-h] [-d] [-q [-H=[H]]] [-M=<M>] [-K=<K>] [-L=<L>] [-N=<N>] """
            sys.exit()
        else:
            print """ usage : localtest.py [-q [-H=[H]]] [-M=<M>] [-K=<K>] [-L=<L>] [-N=<N>] """
            sys.exit()
    
    lt = LocalTest( M, K, L, N, sync_algo, H, debug, port_base)
    lt.run()
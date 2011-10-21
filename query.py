import random
from itertools import combinations
import time

random.seed(time.localtime())

def rand_plus_minus_one():
    x = random.randint(0,100000)%2
    if x == 0:
        x = -1
    return x

def sgn(x):
    if x >= 0:
        return 1
    else:
        return -1

def prod(x, w):
    if len(x) != len(w):
        raise ValueError
    p = 0    
    for i in range(len(x)):
        p += x[i] * w[i]
    return p

N = 40
L = 4
H = 1.4

w = []
for i in range(N):    
    w.append( random.randint(-1*L, L) )

#w = [3, 0, -1, 2, -2, 0, -3, 1]



sigma = rand_plus_minus_one()
h = sigma * H
#h = H

fact = h * (N**0.5)

#print 'h : ', h

n = {}
c = {}
x = []
for i in range(0,L+1):
    n[i] = []
    c[i] = 0

for i in range(len(w)):
    x.append(0)
    wi = w[i]
    n[abs(wi)].append(i)
    
print 'n : ', n

revran = range(1, L+1)
revran.reverse()
for l in revran:    
    rule_chooser = rand_plus_minus_one()
    s = 0
    for j in range(l+1,L+1):
        s += j*(2*c[j] - len(n[j]) )
    
    val = float(len(n[l]) + rule_chooser)/2 + (1/float(2*l))*(fact-s)
    if val > len(n[l]):
        val = len(n[l])
    elif val < 0:
        val = 0
    c[l] = int(val)

print 'c : ', c


for i in n[0]:
    x[i] = rand_plus_minus_one()

for l in range(1, L+1):
    print 'l : ', l
#    chosen = []
#    for bla in range(c[l]):
#        ind = random.randint(0, 100000)
#        ind %= len(n[l])
#        temp = n[l].pop(ind)
#        chosen.append(temp)
    combs = list(combinations(n[l], int(c[l])))
    comb_ind = random.randint(0, len(combs)-1)
    chosen = combs[comb_ind]
    print 'l : ', l, '  chosen : ', chosen
    for i in n[l]:
        if i in chosen:
            x[i] = 1 * sgn(w[i])
        else:
            x[i] = -1 * sgn(w[i])

print 'w : ', w
#print 'x : ', x

print 'fact ', fact, '  h_calc : ', prod(x, w)

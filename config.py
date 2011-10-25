# port on which key exchange protocol should run
port = 5000
iplist = ['10.110.6.252']
myip = '10.110.6.250'

I = 1

# System Parameters that determine security and key length
# These need to be configured based on number of partners participating.

# Optimal value is 3. Increasing K increases key length but on contrary makes protocol inefficient and less exure
K = 3
# For K = 3, increasing L increases security and syncronization time(iterations) steeply 
L = 2
# For 2 partners and K = 3, L = 4, increasing N increases security, syncronization time(iterations) and key length increases linearly.
N = 10

M = 3

sync_algo = 'plain'

H = 4.0

res = 'log_results'

debug = False

port_base = 10000

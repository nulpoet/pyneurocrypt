#!/usr/bin/en python
"""
Example: simple line plot.
Show how to make and save a simple line plot with labels, title and grid
"""
import numpy
import pylab

rho = numpy.arange(0.0, 1.0+0.001, 0.001)
e = numpy.arccos(rho) / 3.14


n=2

Pr_E = 1 - pow((1-e),n-1)



#k = 2
t1 = pow((1-e), (n-1))
t2 = 1-pow(1-e,n-1)

Pu_k2 = pow(t1, 2) + pow(t2, 2)
Pr_k2 = (1.0/Pu_k2) * pow(t2, 2)


#k = 3
t1 = pow((1-e), (n-1))
t2 = 1-pow(1-e,n-1)

Pu_k3 = pow(t1, 3) + 3*t1*pow(t2, 2)
Pr_k3 = (1.0/Pu_k3) * (2 * pow((1-e), n-1) * pow((1-pow(1-e,n-1)), 2))


#k = 4
t1 = pow((1-e), (n-1))
t2 = 1-pow(1-e,n-1)

Pu_k4 = pow(t1, 4) + 6*pow(t1, 2)*pow(t2, 2)  + pow(t2, 4)
Pr_k4 = (1.0/Pu_k4) * (3*pow(t1, 2)*pow(t2, 2) + pow(t2, 4))



pylab.plot (e, Pr_E, 'k--', e, Pr_k2, 'r-', e, Pr_k3, 'g-', e, Pr_k4, 'b-')


pylab.xlabel("'e' : arccos(overlap)/pi\n[Dotted : Simple Attack, Red : k=2, Green : k=3, Blue : k=4]")
pylab.ylabel('Pr')
pylab.title('** Probablity of repulsive steps **')
pylab.grid(True)
pylab.savefig('Pr_for_diff_k_m2_plot')

pylab.show()

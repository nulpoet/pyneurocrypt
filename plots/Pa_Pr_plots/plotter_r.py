#!/usr/bin/en python
"""
Example: simple line plot.
Show how to make and save a simple line plot with labels, title and grid
"""
import numpy
import pylab

rho = numpy.arange(0.0, 1.0+0.001, 0.001)
e = numpy.arccos(rho) / 3.14

n=10
Pr_E = 1 - pow((1-e),n-1)
Pu = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pr_B = (1/Pu) * 2 * pow((1-e), n-1) * pow((1-pow(1-e,n-1)), 2)

n=2
Pr_E_m2 = 1 - pow((1-e),n-1)
Pu_m2 = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pr_B_m2 = (1.0/Pu_m2) * 2 * pow((1-e), n-1) * pow((1-pow(1-e,n-1)), 2)
#Pr_B_m2 =  2 * (1-e)*pow(e,2) / ( pow(1-e,3) + 3*(1-e)*pow(e,2) )

n=3
Pr_E_m3 = 1 - pow((1-e),n-1)
Pu_m3 = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pr_B_m3 = (1.0/Pu_m3) * 2 * pow((1-e), n-1) * pow((1-pow(1-e,n-1)), 2)

n=4
Pr_E_m4 = 1 - pow((1-e),n-1)
Pu_m4 = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pr_B_m4 = (1.0/Pu_m4) * 2 * pow((1-e), n-1) * pow((1-pow(1-e,n-1)), 2)


pylab.plot (e, Pr_E_m2, 'r--', e, Pr_B_m2, 'r-', e, Pr_E_m3, 'g--', e, Pr_B_m3, 'g-', e, Pr_E_m4, 'b--', e, Pr_B_m4, 'b-')

#ylim(-1,4)
#pylab.yticks( numpy.arange(4), ['Pr E', 'Pr B m=2', 'Pr B m=3', 'Pr B m=4'])

pylab.xlabel("'e' : arccos(overlap)/pi")
pylab.ylabel('Pr')
pylab.title('** Probablity of repulsive steps **')
pylab.grid(True)
pylab.savefig('Pr_plot')

pylab.show()

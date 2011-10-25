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
Pa_E = pow((1/2.0),n-1) * pow((1-e),n-1)
Pu = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pa_B = pow((1/2.0),1) * (1/Pu) * ( pow((1-e), (n-1)*3) +  pow((1-e),n-1) * pow((1-pow(1-e,n-1)), 2) )

n=2
Pa_E_m2 = pow((1/2.0),n-1) * pow((1-e),n-1)
Pu_m2 = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pa_B_m2 = pow((1/2.0),1) * (1/Pu_m2) * ( pow((1-e), (n-1)*3) +  pow((1-e),n-1) * pow((1-pow(1-e,n-1)), 2) )


n=3
Pa_E_m3 = pow((1/2.0),n-1) * pow((1-e),n-1)
Pu_m3 = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pa_B_m3 = pow((1/2.0),1) * (1/Pu_m3) * ( pow((1-e), (n-1)*3) +  pow((1-e),n-1) * pow((1-pow(1-e,n-1)), 2) )

n=4
Pa_E_m4 = pow((1/2.0),n-1) * pow((1-e),n-1)
Pu_m4 = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pa_B_m4 = pow((1/2.0),1) * (1/Pu_m4) * ( pow((1-e), (n-1)*3) +  pow((1-e),n-1) * pow((1-pow(1-e,n-1)), 2) )


#n=4
#Pa_B_m4 = (1/2.0) * (pow(1-e,3*(n-1)) + pow((1-e), n-1)*(n-1)*pow(e,2))  /  (pow(1-e,3*(n-1)) + 3*(n-1)*pow((1-e),n-1) * pow(e,2))

pylab.plot (e, Pa_E_m2, 'r--', e, Pa_B_m2, 'r-', e, Pa_E_m3, 'g--', e, Pa_B_m3, 'g-', e, Pa_E_m4, 'b--', e, Pa_B_m4, 'b-')


#pylab.plot (e, Pr_B_m2, color='k')

#ylim(-1,4)
#pylab.yticks( numpy.arange(4), ['Pr E', 'Pr B m=2', 'Pr B m=3', 'Pr B m=4'])

pylab.xlabel("'e' : arccos(overlap)/pi")
pylab.ylabel('Pa')
pylab.title('**Probablity of attractive steps**')
pylab.grid(True)
pylab.savefig('Pa_plot')

pylab.show()

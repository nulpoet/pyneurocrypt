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

n=10
Pr_E = 1 - pow((1-e),n-1)
Pu = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pr_B = (1/Pu) * 2 * pow((1-e), n-1) * pow((1-pow(1-e,n-1)), 2)

Pa_B_rel = Pa_B / (Pa_B + Pr_B)


n=3
Pa_E_m3 = pow((1/2.0),n-1) * pow((1-e),n-1)
Pu_m3 = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pa_B_m3 = pow((1/2.0),1) * (1/Pu_m3) * ( pow((1-e), (n-1)*3) +  pow((1-e),n-1) * pow((1-pow(1-e,n-1)), 2) )

n=3
Pr_E_m3 = 1 - pow((1-e),n-1)
Pu_m3 = pow((1-e), (n-1)*3) + 3*pow((1-e),n-1) * pow((1-pow(1-e,n-1)),2)
Pr_B_m3 = (1.0/Pu_m3) * 2 * pow((1-e), n-1) * pow((1-pow(1-e,n-1)), 2)

Pa_B_rel_m3 = Pa_B_m3 / (Pa_B_m3 + Pr_B_m3)



pylab.plot (e, Pa_B_m3, 'r-', e, Pr_B_m3, 'g-', e, Pa_B_rel_m3, 'k-')
#pylab.plot (e, Pa_B_rel_m3, 'k-')


#ylim(-1,4)
#pylab.yticks( numpy.arange(4), ['Pr E', 'Pr B m=2', 'Pr B m=3', 'Pr B m=4'])

pylab.xlabel("'e' : arccos(overlap)/pi")
pylab.ylabel('Pa')
pylab.title('**Probablity of attractive steps for 3 machines**')
pylab.grid(True)
pylab.savefig('Pa_rel_plot_m3')

pylab.show()


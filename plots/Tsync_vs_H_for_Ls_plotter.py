import numpy
import pylab

H  	   = numpy.array([	0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  1.5,  2.0,  3.0,  4.0,  5.0,  6.0,  7.0])

ts_L_3 = numpy.array([20000, 6000, 1000,  534,  467,  420,  390,  360,  350,  326,  310,  196,  180])
ts_L_4 = numpy.array([ None,40000,12000, 2000,  900,  700,  550,  430,  400,  390,  366,  350,  226])
ts_L_5 = numpy.array([ None, None,70000,20000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000])
ts_L_6 = numpy.array([ None, None, None,90000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000])

#pylab.plot( H, ts_L_3, 'ro--', H, ts_L_4, 'bo--')
pylab.plot( H, ts_L_3, 'ro--', H, ts_L_4, 'bo--', H, ts_L_5, 'go--', H, ts_L_6, 'ko--')

pylab.xlabel("H")
pylab.ylabel('avg T_sync')
pylab.title('T_sync vs H for for L = 3(red), 4(blue), 5(green), 6(black)')
pylab.grid(True)
pylab.savefig('T_sync_vs_H_for_Ls')

pylab.show()

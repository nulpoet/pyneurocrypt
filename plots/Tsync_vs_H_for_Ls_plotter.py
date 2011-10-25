import numpy
import pylab

H  	= [   0.3,    0.4,   0.5,  0.6,  0.7,  0.8,  0.9,   1.0,  1.1,   1.2,   1.3,    1.4,   1.5,  1.6,  1.7,  1.8,  1.9,  2.0,  3.0,  4.0,  5.0,  6.0,  7.0 ]

L_3 = [  None, 180000, 30601, 6403, 1113,  825,  642,   422,   371,  254,  243,     240,   239,  199,  201,  193,  199,  204,  194,  151,  157,  144,  148 ]
L_4 = [  None,   None,  None, None,47215,10720, 2210,   980,  912,   713,  562,     509,   440,  449,  433,  431,  425,  420,  357,  262,  250,  236,  235 ]
L_5 = [  None,   None,  None, None, None, None, None, 50553, 8905,  2398,  1371,   1048,   986,  805,  722,  667,  657,  611,  519,  503,  430,  369,  377 ]
L_6 = [  None,   None,  None, None, None, None, None,  None, None,200000,  7653,   3527,  2769, 2212, 1468, 1359, 1278, 1039,  947,  726,  641,  554,  523 ]
L_7 = [  None,   None,  None, None, None, None, None,  None, None,  None,  None, 150000, 30074,13219, 8411, 5587, 3537, 2194, 1280, 1005,  936,  879,  856 ]

#Originals
#L_3 = [  None, 180000, 30601, 6403, 1113,  825,  642,  None, None,   254,   223,    240,   239,  199,  219,  193,  175,  218,  194,  151,  197,  144,  158 ]
#L_4 = [  None,   None,  None, None,47215,10720, 2210,   980,  912,   713,  None,   None,   440,  449, None, None, None,  450,  357,  262,  250, None,  235 ]
#L_5 = [  None,   None,  None, None, None, None, None, 50553, 8905,  2398,  1371,   1048,   986,  805,  722,  667,  657,  859,  519,  503,  430,  369,  377 ]
#L_6 = [  None,   None,  None, None, None, None, None,  None, None,200000,  7653,   3527,  2569, 2212, 1468, 1459, 1278, 1639,  947,  726,  641,  554,  573 ]
#L_7 = [  None,   None,  None, None, None, None, None,  None, None,  None,  None, 150000, 30074, None, 3537, None, None, 2194, 1280, 1005, None, None, None ]


L_3_log_scaled = []
for x in L_3:
    if x == None:
        L_3_log_scaled.append(None)
    else:
        L_3_log_scaled.append( numpy.log10(x) )

L_4_log_scaled = []
for x in L_4:
    if x == None:
        L_4_log_scaled.append(None)
    else:
        L_4_log_scaled.append( numpy.log10(x) )

L_5_log_scaled = []
for x in L_5:
    if x == None:
        L_5_log_scaled.append(None)
    else:
        L_5_log_scaled.append( numpy.log10(x) )

L_6_log_scaled = []
for x in L_6:
    if x == None:
        L_6_log_scaled.append(None)
    else:
        L_6_log_scaled.append( numpy.log10(x) )

L_7_log_scaled = []
for x in L_7:
    if x == None:
        L_7_log_scaled.append(None)
    else:
        L_7_log_scaled.append( numpy.log10(x) )


#ts_L_3 = numpy.array([ ])
#ts_L_4 = numpy.array([ None,40000,12000, 2000,  900,  700,  550,  430,  400,  390,  366,  350,  226])
#ts_L_5 = numpy.array([ None, None,70000,20000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000])
#ts_L_6 = numpy.array([ None, None, None,90000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000])

#pylab.plot( H, ts_L_3, 'ro--', H, ts_L_4, 'bo--')
pylab.plot(
    numpy.array(H), numpy.array(L_3_log_scaled), 'ro-', 
    numpy.array(H), numpy.array(L_4_log_scaled), 'bo--', 
    numpy.array(H), numpy.array(L_5_log_scaled), 'go--', 
    numpy.array(H), numpy.array(L_6_log_scaled), 'ko--',
    numpy.array(H), numpy.array(L_7_log_scaled), 'co--'
)

pylab.xlabel("H")
pylab.ylabel('avg T_sync (log scaled)')
pylab.title('T_sync vs H for for L = 3(red), 4(blue), 5(green), 6(black), 7(cyan)')
pylab.grid(True)
pylab.savefig('T_sync_vs_H_for_Ls')

pylab.show()

from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
import numpy as np

class MercatorLatitudeScale(mscale.ScaleBase):
    """
    Scales data in range -pi/2 to pi/2 (-90 to 90 degrees) using
    the system used to scale latitudes in a Mercator projection.

    The scale function:
      ln(tan(y) + sec(y))

    The inverse scale function:
      atan(sinh(y))

    Since the Mercator scale tends to infinity at +/- 90 degrees,
    there is user-defined threshold, above and below which nothing
    will be plotted.  This defaults to +/- 85 degrees.

    source:
    http://en.wikipedia.org/wiki/Mercator_projection
    """

    # The scale class must have a member ``name`` that defines the
    # string used to select the scale.  For example,
    # ``gca().set_yscale("mercator")`` would be used to select this
    # scale.
    name = 'mercator'


    def __init__(self, axis, **kwargs):
        """
        Any keyword arguments passed to ``set_xscale`` and
        ``set_yscale`` will be passed along to the scale's
        constructor.

        thresh: The degree above which to crop the data.
        """
        mscale.ScaleBase.__init__(self)
        
        self.thresh = 0.0
        
#        thresh = kwargs.pop("thresh", (85 / 180.0) * np.pi)
#        if thresh >= np.pi / 2.0:
#            raise ValueError("thresh must be less than pi/2")
#        self.thresh = thresh

    def get_transform(self):
        """
        Override this method to return a new instance that does the
        actual transformation of the data.

        The MercatorLatitudeTransform class is defined below as a
        nested class of this one.
        """
        return self.MercatorLatitudeTransform(self.thresh)

    def set_default_locators_and_formatters(self, axis):
        """
        Override to set up the locators and formatters to use with the
        scale.  This is only required if the scale requires custom
        locators and formatters.  Writing custom locators and
        formatters is rather outside the scope of this example, but
        there are many helpful examples in ``ticker.py``.

        In our case, the Mercator example uses a fixed locator from
        -90 to 90 degrees and a custom formatter class to put convert
        the radians to degrees and put a degree symbol after the
        value::
        """
        
        self.set_default_locators_and_formatters(axis)
        
#        class DegreeFormatter(Formatter):
#            def __call__(self, x, pos=None):
#                # \u00b0 : degree symbol
#                return u"%d\u00b0" % ((x / np.pi) * 180.0)
#
#        deg2rad = np.pi / 180.0
#        axis.set_major_locator(FixedLocator(
#                np.arange(-90, 90, 10) * deg2rad))
#        axis.set_major_formatter(DegreeFormatter())
#        axis.set_minor_formatter(DegreeFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        """
        Override to limit the bounds of the axis to the domain of the
        transform.  In the case of Mercator, the bounds should be
        limited to the threshold that was passed in.  Unlike the
        autoscaling provided by the tick locators, this range limiting
        will always be adhered to, whether the axis range is set
        manually, determined automatically or changed through panning
        and zooming.
        """
        self.limit_range_for_scale(vmin, vmax, minpos)
#        return max(vmin, -self.thresh), min(vmax, self.thresh)

    class MercatorLatitudeTransform(mtransforms.Transform):
        # There are two value members that must be defined.
        # ``input_dims`` and ``output_dims`` specify number of input
        # dimensions and output dimensions to the transformation.
        # These are used by the transformation framework to do some
        # error checking and prevent incompatible transformations from
        # being connected together.  When defining transforms for a
        # scale, which are, by definition, separable and have only one
        # dimension, these members should always be set to 1.
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            """
            This transform takes an Nx1 ``numpy`` array and returns a
            transformed copy.  Since the range of the Mercator scale
            is limited by the user-specified threshold, the input
            array must be masked to contain only valid values.
            ``matplotlib`` will handle masked arrays and remove the
            out-of-range data from the plot.  Importantly, the
            ``transform`` method *must* return an array that is the
            same shape as the input array, since these values need to
            remain synchronized with values in the other dimension.
            """
#            masked = ma.masked_where((a < -self.thresh) | (a > self.thresh), a)
#            if masked.mask.any():
#                return ma.log(np.abs(ma.tan(masked) + 1.0 / ma.cos(masked)))
#            else:
#                return np.log(np.abs(np.tan(a) + 1.0 / np.cos(a)))
            
            if a <= self.thresh:
                return float('nan')
            else:
                return np.log10(a)

        def inverted(self):
            """
            Override this method so matplotlib knows how to get the
            inverse transform for this transform.
            """
            return MercatorLatitudeScale.InvertedMercatorLatitudeTransform(self.thresh)

    class InvertedMercatorLatitudeTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            return 10**a
#            return np.arctan(np.sinh(a))

        def inverted(self):
            return MercatorLatitudeScale.MercatorLatitudeTransform(self.thresh)

# Now that the Scale class has been defined, it must be registered so
# that ``matplotlib`` can find it.
mscale.register_scale(MercatorLatitudeScale)


import numpy
import pylab

H      = numpy.array([   0.5,  0.6,  0.7,  0.8,  0.9,  1.0,  1.5,  2.0,  3.0,  4.0,  5.0,  6.0,  7.0])

ts_L_3 = numpy.array([ 20000, 6000, 1000,  534,  467,  420,  390,  360,  350,  326,  310,  196,  180])
ts_L_4 = numpy.array([ None,40000,12000, 2000,  900,  700,  550,  430,  400,  390,  366,  350,  226])
ts_L_5 = numpy.array([ None, None,70000,20000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000])
ts_L_6 = numpy.array([ None, None, None,90000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000])

#pylab.plot( H, ts_L_3, 'ro--', H, ts_L_4, 'bo--')
pylab.plot( H, ts_L_3, 'ro--', H, ts_L_4, 'bo--', H, ts_L_5, 'go--', H, ts_L_6, 'ko--')
pylab.gca().set_yscale('mercator')
pylab.xlabel("H")
pylab.ylabel('avg T_sync')
pylab.title('T_sync vs H for for L = 3(red), 4(blue), 5(green), 6(black)')
pylab.grid(True)
pylab.savefig('T_sync_vs_H_for_Ls')

pylab.show()



#from pylab import *
#import numpy as np
#
#t = arange(-180.0, 180.0, 0.1)
#s = t / 360.0 * np.pi
#
#plot(t, s, '-', lw=2)
#gca().set_yscale('mercator')
#
#xlabel('Longitude')
#ylabel('Latitude')
#title('Mercator: Projection of the Oppressor')
#grid(True)
#
#show()

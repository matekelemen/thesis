# --- External Imports ---
import numpy
import scipy.interpolate
import matplotlib.pyplot as pyplot
import matplotlib.ticker

# --- STL Imports ---
import json


pyplot.rc( "font", size=16 )

axesLabelStyle = {
    "family"    : "serif",
    "weight"    : "normal",
    "color"     : "black",
    "size"      : 20
}

axesLegendStyle = {
    "family"    : "serif",
    "weight"    : "normal",
    "size"      : 20
}

axesTickStyle = {
    "labelsize"     : 16,
    "labelcolor"    : "black",
    "labelrotation" : False
}


def getDisplacement( time ):
    return numpy.sin( 10*2.0*numpy.pi * (time-0.2) )


def quadraticSplineRoots(spl):
    roots = []
    knots = spl.get_knots()
    for a, b in zip(knots[:-1], knots[1:]):
        u, v, w = spl(a), spl((a+b)/2), spl(b)
        t = numpy.roots([u+w-2*v, w-u, 2*v])
        t = t[numpy.isreal(t) & (numpy.abs(t) <= 1)]
        roots.extend(t*(b-a)/2 + (b+a)/2)
    return numpy.array(roots)


def findInterpolatedExtremum( x, y ):
    '''Fit a cubic spline around the absolute max value and find location of its extremum'''

    # Find absolute max index
    index = numpy.argmax( numpy.abs( y ) )

    # Fit spline
    indexRange = slice(
        max( index - 3, 0 ),
        min( index + 3, len(x) ),
        1
    )

    try:
        spline = scipy.interpolate.InterpolatedUnivariateSpline(
            x[indexRange],
            y[indexRange],
            k=3
        )
    except Exception as exception:
        return numpy.nan

    # Find extremum
    try:
        roots = quadraticSplineRoots( spline.derivative() )
    except Exception as exception:
        return x[index]

    if len(roots) > 0:
        absValues = [ numpy.abs(spline(t)) for t in roots ]
        return roots[ numpy.argmax(absValues) ]
    else:
        return x[index]


if __name__ == "__main__":

    JSONContents = {}

    with open( "generate_data_for_envelope_centroid.json", "r" ) as file:
        JSONContents = json.load( file )

    time = numpy.linspace( 0.2, 0.3, num=35 )
    displacement = getDisplacement(time)

    timeOfArrival = findInterpolatedExtremum( time, displacement )

    nMax = numpy.argmax( numpy.abs(displacement) )
    dn = 1
    indexRadius = 3 * dn
    splineIndexRadius = 2 * dn

    indexRange = slice( nMax-indexRadius, nMax+indexRadius+1, dn )
    splineIndexRange = slice( nMax-splineIndexRadius, nMax+splineIndexRadius+1, dn )

    splineTime = time[splineIndexRange]

    spline = scipy.interpolate.InterpolatedUnivariateSpline(
        time[splineIndexRange],
        displacement[splineIndexRange],
        k=3
    )

    time = time[indexRange]
    displacement = displacement[indexRange]

    samples = numpy.linspace( time[0], time[-1], num=100 )
    values = spline( samples )
    analyticalValues = getDisplacement(samples)

    splineSamples = numpy.linspace( splineTime[0], splineTime[-1], num=100 )

    figure, axis = pyplot.subplots( 1 )
    axis.set_xlabel( "t", fontdict=axesLabelStyle )
    axis.set_ylabel( "u", fontdict=axesLabelStyle )
    axis.tick_params( **axesTickStyle )

    #axis.plot(
    #    samples, analyticalValues,
    #    "-",
    #    color=numpy.asarray( [218,215,203] ) / 255.0,
    #    linewidth=1.0
    #)

    axis.plot(
        time, displacement,
        "+",
        color=numpy.asarray([0,82,147]) / 255.0,
        linewidth=3.0,
        mew=2, ms=8
    )

    axis.plot(
        splineSamples, spline(splineSamples),
        "-.",
        color=numpy.asarray([227,114,34]) / 255.0,
        linewidth=2.5
    )

    axis.plot(
        [timeOfArrival,timeOfArrival], [numpy.min(displacement), numpy.max(displacement)],
        linestyle="dotted",
        color=[0,0,0]
    )

    legend = [ "$u(t_k)$", "$s(t)$", "$t^a_u$" ]
    
    axisMultiplier = matplotlib.ticker.ScalarFormatter(useMathText=True)
    axis.yaxis.set_major_formatter(axisMultiplier)
    axis.legend( legend, prop=axesLegendStyle )

    axis.set_xticks( [0.22, 0.225, 0.23, 0.235] )
    axis.set_yticks( [0.8, 0.85, 0.9, 0.95, 1.0] )

    figure.set_size_inches( 8, 5 )
    figure.set_dpi( 60 )
    figure.tight_layout()

    figure.savefig( "cubic_interpolation_max.eps", format="eps" )

    pyplot.show()
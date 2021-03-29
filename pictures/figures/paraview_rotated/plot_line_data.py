import numpy
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker

import sys



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



filePath = sys.argv[1]

data = [[],[],[],[]]

with open( filePath, "r" ) as file:
    for line in file:
        line = line.split(",")
        for index, value in enumerate(line):
            value = float(value)
            data[index].append(value)
            
data = [ numpy.array(data[3]), numpy.array(data[1]) ]
data[0] -= numpy.mean(data[0])

uMin = numpy.min(data[1])
uMax = numpy.max(data[1])

yMin = -0.01
yMax = 0.01

figure, axes = pyplot.subplots( 1, 1 )

axes.set_xlabel( r"$\tilde{y}$", fontdict=axesLabelStyle )
axes.set_ylabel( r"$u$", fontdict=axesLabelStyle )
axes.tick_params( **axesTickStyle )

axisMultiplierStyler = ticker.ScalarFormatter( useMathText=True )
axes.yaxis.set_major_formatter( axisMultiplierStyler )

axes.grid(
    color=numpy.asarray([218, 215, 203]) / 255.0,
    linestyle="--",
    linewidth=1.0
)

axes.plot(
    data[0], data[1],
    color=numpy.array([ 0, 82, 147 ])/255.0
)

axes.plot(
    [yMin, yMin], [uMin, uMax],
    [yMax, yMax], [uMin, uMax],
    color=[0,0,0],
    lineWidth=1.0,
    linestyle="-."
)

figure.tight_layout()
figure.savefig( "plot_over_line.eps", format="eps" )
pyplot.show()

# --- External Imports ---
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker

# --- STL Imports ---
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


colors = [
    [ 0, 82, 147 ],
    [ 227, 114, 34 ],
    [ 186, 129, 160 ],
    [ 120, 120, 21 ],
    [234, 25, 32]
]



if __name__=="__main__":

    filePath = sys.argv[1]

    values = []
    with open( filePath, "r" ) as file:
        for value in file:
            value = float(value)
            if 0 < value: 
                values.append( value )

    values = numpy.asarray( values )

    figure, axes = pyplot.subplots( 1, 1 )
    
    axes.hist(
        values,
        bins=50,
        color=numpy.array(colors[0]) / 255.0
    )

    axes.set_xlabel( r"$\eta$", fontdict=axesLabelStyle )
    axes.set_ylabel( "number of cells", fontdict=axesLabelStyle )
    axes.tick_params( **axesTickStyle )

    axisMultiplierStyler = ticker.ScalarFormatter( useMathText=True )
    axes.yaxis.set_major_formatter( axisMultiplierStyler )
    axes.set_yscale( "log" )

    axes.grid(
            color=numpy.asarray([218, 215, 203]) / 255.0,
            linestyle="--",
            linewidth=1.0
        )

    pyplot.savefig( "ellipsoid_fill_ratio_histogram.eps", format="eps" )
    pyplot.show()
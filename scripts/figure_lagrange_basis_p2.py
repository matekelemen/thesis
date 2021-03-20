import numpy
import matplotlib.pyplot as pyplot


def lagrangeBasis( coordinate: float,
                   activeNode: float,
                   inactiveNodes: list ):
    value = 1.0
    for node in inactiveNodes:
        value *= (coordinate - node) / (activeNode - node)
    return value


if __name__ == "__main__":

    # Quadrature poitns
    lobattoNodes = [
        -1.0,
        0.0,
        1.0
    ]

    # Sample points
    samples = numpy.linspace( -1.0, 1.0, 100 )

    # Line style
    lineWidth = 2

    colors = [
        [51, 51, 51],
        [0, 82, 147],
        [227, 114, 34]
    ]

    # Plot basis functions
    for node, color in zip(lobattoNodes, colors):
        inactiveNodes = lobattoNodes.copy()
        inactiveNodes.remove( node )
        pyplot.plot(
            samples,
            [ lagrangeBasis(coordinate, node, inactiveNodes) for coordinate in samples ],
            linewidth=lineWidth,
            color=numpy.array(color)/255.0
        )

    # Axes labels
    axesLabelStyle = {
        "family"    : "serif",
        "weight"    : "normal",
        "color"     : "black",
        "size"      : 20
    }

    # Axes ticks
    pyplot.tick_params(
        labelsize=16,
        labelcolor="black",
        labelrotation=False
    )

    pyplot.xticks( [] )
    pyplot.yticks( [] )

    # Figure size and resolution
    figure = pyplot.gcf()
    figure.set_size_inches( 6, 4 )
    figure.set_dpi( 125 )
    figure.subplots_adjust( bottom=0.15, left=0.15 )

    # Event loop
    figure.savefig( "figure_lagrange_basis_p2.eps", format="eps" )
    pyplot.show()
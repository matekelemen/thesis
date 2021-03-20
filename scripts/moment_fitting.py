import numpy
import scipy.integrate


lobattoNodes = numpy.asarray([-1.0, 0.0, 1.0])
lobattoWeights = numpy.asarray([1.0, 4.0, 1.0]) / 3.0

def lagrangeBasis( coordinate: float,
                   activeNode: float,
                   inactiveNodes: list ):
    value = 1.0
    for node in inactiveNodes:
        value *= (coordinate - node) / (activeNode - node)
    return value


def makeLagrangeBasis( activeNode, inactiveNodes ):
    return lambda x: lagrangeBasis(x, activeNode, inactiveNodes)


if __name__ == "__main__":

    basis = []
    for node in lobattoNodes:
        inactiveNodes = list(lobattoNodes)
        inactiveNodes.remove(node)
        basis.append( makeLagrangeBasis(node, inactiveNodes) )


    # Build ansatz space from the basis (2D)
    ansatzSpace = [
        lambda x, y: basis[0](x) * basis[0](y),
        lambda x, y: basis[0](x) * basis[1](y),
        lambda x, y: basis[0](x) * basis[2](y),
        lambda x, y: basis[1](x) * basis[0](y),
        lambda x, y: basis[1](x) * basis[1](y),
        lambda x, y: basis[1](x) * basis[2](y),
        lambda x, y: basis[2](x) * basis[0](y),
        lambda x, y: basis[2](x) * basis[1](y),
        lambda x, y: basis[2](x) * basis[2](y)
    ]

    # Integration points from lobatto nodes
    integrationPoints = [
        numpy.asarray([ lobattoNodes[0], lobattoNodes[0] ]),
        numpy.asarray([ lobattoNodes[0], lobattoNodes[1] ]),
        numpy.asarray([ lobattoNodes[0], lobattoNodes[2] ]),
        numpy.asarray([ lobattoNodes[1], lobattoNodes[0] ]),
        numpy.asarray([ lobattoNodes[1], lobattoNodes[1] ]),
        numpy.asarray([ lobattoNodes[1], lobattoNodes[2] ]),
        numpy.asarray([ lobattoNodes[2], lobattoNodes[0] ]),
        numpy.asarray([ lobattoNodes[2], lobattoNodes[1] ]),
        numpy.asarray([ lobattoNodes[2], lobattoNodes[2] ]),
    ]

    integrationWeights = [
        lobattoWeights[0] * lobattoWeights[0],
        lobattoWeights[0] * lobattoWeights[1],
        lobattoWeights[0] * lobattoWeights[2],
        lobattoWeights[1] * lobattoWeights[0],
        lobattoWeights[1] * lobattoWeights[1],
        lobattoWeights[1] * lobattoWeights[2],
        lobattoWeights[2] * lobattoWeights[0],
        lobattoWeights[2] * lobattoWeights[1],
        lobattoWeights[2] * lobattoWeights[2]
    ]

    # Compute moment fitting RHS
    # Cube over the integration domain [-1,1]^3
    # cut in half in the x-direction (positive halfspace is the physical one)
    momentFittingRHS = []
    for ansatz in ansatzSpace:
        momentFittingRHS.append( scipy.integrate.dblquad(
            ansatz,
            -1.0, 0.0,
            -1.0, 1.0
        )[0] )

    momentFittingWeights = []
    for ansatz, point, rhs in zip(ansatzSpace, integrationPoints, momentFittingRHS):
        momentFittingWeights.append(
            rhs / ansatz(point[0], point[1])
        )

    print("Moment fitting weights: {}".format( momentFittingWeights ))

    # "Mass matrix"
    massMatrix = numpy.zeros( (9,9) )

    alphaFCM = 1e-5
    def alpha( x, y ):
        if 0.0 <= x:
            return alphaFCM
        else:
            return 1.0

    for i in range(9):
        for j in range(9):

            integrand = lambda x, y: alpha(x,y) * ansatzSpace[i](x,y) * ansatzSpace[j](x,y)

            for point, weight in zip(integrationPoints, momentFittingWeights):
                massMatrix[i,j] += weight * integrand(point[0], point[1])

    print(massMatrix)

    numpy.savetxt( "mass_matrix_moment_fitting.txt", massMatrix, delimiter="   ", newline="\n", fmt="%.1e" )
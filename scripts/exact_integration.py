import numpy
import matplotlib.pyplot as plt


def lobattoQuadratureMaxOrder( polynomialOrder: int,
                               dimension: int ):
    return (2*polynomialOrder - 1)**dimension
    
    
def gaussQuadratureMaxOrder( polynomialOrder: int,
                             dimension: int ):
    return (2*polynomialOrder + 1)**dimension
    
def massIntegrandOrder( polynomialOrder: int,
                        dimension: int ):
    return (dimension*polynomialOrder)**2
    
def stiffnessIntegrandOrder( polynomialOrder: int,
                             dimension: int ):
    return (dimension*polynomialOrder - 1)**2


if __name__ == "__main__":
    
    dimension = 2
    polynomialOrders = numpy.arange(1, 5)
    
    
    lobattoOrders    = [ lobattoQuadratureMaxOrder(p, dimension) - massIntegrandOrder(p, dimension) for p in polynomialOrders ]
    gaussOrders      = [ gaussQuadratureMaxOrder(p,dimension) - massIntegrandOrder(p, dimension) for p in polynomialOrders ]
    
    plt.plot( polynomialOrders, [0 for p in polynomialOrders],
              polynomialOrders, gaussOrders,
              polynomialOrders, lobattoOrders )
    plt.legend( ["0", "gauss", "lobatto"] )
    plt.show()
    
    lobattoOrders    = [ lobattoQuadratureMaxOrder(p, dimension) - stiffnessIntegrandOrder(p, dimension) for p in polynomialOrders ]
    gaussOrders      = [ gaussQuadratureMaxOrder(p,dimension) - stiffnessIntegrandOrder(p, dimension) for p in polynomialOrders ]
    
    plt.plot( polynomialOrders, [0 for p in polynomialOrders],
              polynomialOrders, gaussOrders,
              polynomialOrders, lobattoOrders )
    plt.legend( ["0", "gauss", "lobatto"] )
    plt.show()

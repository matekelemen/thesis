import sympy
import numpy
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # Symbols
    x, y, E, rho, gamma = sympy.symbols("x y E rho gamma")

    # Basis functions
    #basisFunctions = [
    #    (1 - x) / 2,
    #    (1 + x) / 2
    #]
    basisFunctions = [
        x * (x-1) / 2,
        x * (x+1) / 2,
        - (x+1) * (x-1)
    ]

    N = numpy.tensordot( basisFunctions, [basisFunction.subs('x',y) for basisFunction in basisFunctions], axes=0 )
    N = numpy.ravel(N)

    # Basis function derivatives
    dN = sympy.Matrix([ [sympy.diff(n,'x'), sympy.diff(n,'y')] for n in N ])

    # Stiffness matrix
    Kc = dN * dN.transpose()
    Kc = sympy.integrate( Kc, ('y',-1,0) ) + sympy.integrate( gamma * Kc, ('y',0,1) )
    Kc = sympy.integrate( E * Kc, ('x', -1, 1) )

    # Mass matrix (consistent)
    Mc = sympy.Matrix([
        [ sympy.integrate(rho * Ni * Nj, ('x',-1,1), ('y',-1,0)) for Nj in N ] for Ni in N
    ]) + sympy.Matrix([
        [ sympy.integrate( gamma * rho * Ni * Nj, ('x',-1,1), ('y',0,1)) for Nj in N ] for Ni in N
    ])

    traceMc = 0
    massMc = 0
    for i in range(len(N)):
        traceMc += Mc[i,i]
        for j in range(len(N)):
            massMc += Mc[i,j]

    # Mass matrix (uncut)
    Mu = Mc.copy()
    Mu = Mu.subs("gamma", 1)

    traceMu = 0
    massMu = 0
    for i in range(len(N)):
        traceMu += Mu[i,i]
        for j in range(len(N)):
            massMu += Mu[i,j]
    
    # Mass matrix (density scaling)
    Mds = massMc / traceMu * sympy.diag(
        *[ Mu[i,i] for i in range(len(N)) ]
    )

    # Mass matrix (hrz)
    Mhrz = massMc / traceMc * sympy.diag(
        *[ Mc[i,i] for i in range(len(N)) ]
    )

    # -------------------------------------------------
    
    def C( massMatrix ):
        return sympy.simplify( (massMatrix**(-1)) * Kc )

    def subsAnsPrint( matrix, E=1, rho=1, gamma=0 ):
        kwargs = {}
        if issubclass( type(E), (int) ):
            kwargs["E"] = E
        if issubclass( type(rho), (int) ):
            kwargs["rho"] = rho
        if issubclass( type(gamma), (int) ):
            kwargs["gamma"] = gamma
        sympy.pprint( matrix.subs( kwargs ) )
        print()

    Cc = C(Mc)
    Cds = C(Mds)
    Chrz = C(Mhrz)

    subsAnsPrint(Cc, gamma=0)
    subsAnsPrint(Cds, gamma=0)
    subsAnsPrint(Chrz, gamma=0)
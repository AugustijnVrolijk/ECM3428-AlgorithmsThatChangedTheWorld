from matplotlib import *
from matplotlib.pyplot import *
from numpy import *
from numpy import linspace
from scipy.optimize import rosen
import math

def rosen_contours(Nx=100, Ny=100):
    """
    Draw contours of the Rosenbrock test function
    """
    x = linspace(-2.0, 2.0, Nx)
    y = linspace(-2.0, 2.0, Ny)

    R = zeros((Nx, Ny))
    for i in range(Nx):
        for j in range(Ny):
            X = asarray([x[i], y[j]])
            R[i,j] = rosen(X)

    v = concatenate((arange(20), arange(25, 500, 10)))
    clf()
    contour(x, y, R.T, v, alpha=0.3)
    colorbar()
    plot(1.0, 1.0, marker='o', color='yellow')


def cycle(s):
    """
    Yield elements of s cyclically
    """
    n = 0
    while True:
        yield s[n%len(s)]
        n += 1


def maybe_wait(interact):
    if interact:
        return input('>>> Press "Enter" on keyboard to continue -----> ')


def draw_simplex(S, colours):
    """
    Draw the simplex S in the colour given by the colour generator colours.
    """
    # Put the vertices of the simplex in an array for plotting,
    # repeating the last one to close the curve
    rosen_contours()
    ion()
    D = len(S[0][1])
    v = zeros((D+2, 2))
    for i in range(D+1):
        v[i,:] = S[i][1]
    v[-1,:] = S[0][1]
    plot(v[:,0], v[:,1], color=next(colours))
    show()


def distance(p1, p2):
    """
    Calculate the distance between two vector points (x,y).
    """
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])


def termination(simplex, iterations, tolx, tolf, Niter):
    """
    Determinate if thtermination criteria are met
    Return a tulple of (boolean, string)
    """
    if iterations > Niter:
        return(True, "Reach the maximum number of iterations")
    if simplex[0][0] + simplex[1][0] + simplex[2][0] < tolf:
        return(True, "Meet the function tolerence")
    if (distance(simplex[0][1], simplex[1][1])<tolx and
        distance(simplex[1][1], simplex[2][1])<tolx and
        distance(simplex[2][1], simplex[0][1])<tolx):
        return(True, "Meet vertex proximity tolerence")

    return False

def vectorAddition(x1, x2, D):
    """
    for 2 vectors, x1 and x2 returns their sum

    D is the number of dimensions in the vectors

    returns: x3 The addition of both vectors
    """
    x3 = []
    for i in range(D):
        x3.append([])
        x3[i] = x1[i] + x2[i]
    
    return x3

def neldermead(x0, func, tolx=1e-3, tolf=1e-3, Niter=1000, draw=True, interact=True):
    """
    Nelder Mead optimisation of func(x) using the Nelder-Mead simplex algorithm.

    Arguments
    ---------
    x0        Initial guess (vector/list)
    func      The function to be minimised. 
              func(x) should return the function value at x.
    tolx      Stop when the vertices of the simpex are closer than this
    tolf      Stop if the values of the function evaluated at the vertices 
              of the simplex are closer than this.
    Niter     Maximum number of iterations.

    draw      Draw the simplices if True
    interact  Wait for the user to press return after each iteration if True.

    Returns
    -------
    fmin, x  The function value at the minimum and the minimising x.
    """

    # This stub chooses an initial simplex and takes
    # a single step in an arbitrary direction

    D = len(x0) #dimensions of vector
    simplex = []
    simplex.append( (func(x0), x0) )

    # This should use insertion sort to order the vertices
    for i in range(D):
        # Generate new points by moving one coordinate of x in each
        # coordinate direction by 10% of the value in that direction.
        x = x0.copy()
        x[i] *= 1.3
        simplex.append( (func(x), x) )

    colours = cycle("rgbmky")

    iterations = 0

    while True:
        if draw:
            draw_simplex(simplex, colours)
        maybe_wait(interact)

        #[W, G, B] = 0, 1, 2
        simplex = sorted(simplex, key=lambda s: s[0])
        print (simplex[0]) # Print the best point

        if termination(simplex,iterations,tolx,tolf,Niter): # Check the termination point
            print ('\nIterations: %d' % iterations)
            break
        
        iterations +=1

        #*** Task 1 ***#
        #calculate centroid
        c = zeros(D)
        for v in simplex[1:]:
            c += v[1]
        c /=D
        x = c + (c - simplex[0][1])
        simplex[0] = (func(x), x)
        
        
        #*** Task 2 ***#
        
        

        break #Uncomment this line after you write the code for task 2
        #*** End of Task 2 ***#
        
    return simplex[2]

if __name__ == "__main__":
    rosen_contours()
    x0 = asarray([-1.0, 1.0])
    neldermead(x0, rosen, draw=True, interact=True)  # interact=True - if run code in an iterative way
    maybe_wait(True)

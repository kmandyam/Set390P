from solver import *

# This file contains an example of how to use the necessary Z3 features
# to write a set solver.

T = Integer
def CreateMagicSquare(size):
    reset()
    # We would like to create a size x size magic square.  So, we need to create an
    # integer variable for each square.  We use a (nested) list comprehension for this:

    square = [[declare("(" + str(i) + ", " + str(j) + ")", T) for j in range(size)] for i in range(size)]
    for i in range(size):
    # Distinct(-)
    # And(-), Or(-), Not(-), Implies(-)

    return solve(1)

N = 5
print("-"*26)
for square in CreateMagicSquare(N):
    print_2D_array(square, N)
    print("-" * 26)

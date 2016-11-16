from solver import *

# This file contains an example of how to use the necessary Z3 features
# to write a set solver.

T = Integer
def CreateMagicSquare(size):
    reset()
    # We would like to create a size x size magic square.  So, we need to create an
    # integer variable for each square.  We use a (nested) list comprehension for this:

    square = [[declare("(" + str(i) + ", " + str(j) + ")", T) for j in range(size)] for i in range(size)]
    sum_a = sum_b = 0
    for i in range(size):
        test_eq = sum(square[i]) == sum(square[:][i])
        print(simplify(test_eq))
        assume(sum(square[i]) == sum(square[:][i]))
        sum_a += square[i][i]
        sum_b += square[size - 1 - i][i]
    
    # Distinct(-)
    # And(-), Or(-), Not(-), Implies(-)
    assume(sum_a == sum_b)
    return solve(1)

N = 3
print("-"*26)
for square in CreateMagicSquare(N):
    print_2D_array(square, N)
    print("-" * 26)

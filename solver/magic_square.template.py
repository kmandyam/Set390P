from solver import *
import itertools
# This file contains an example of how to use the necessary Z3 features
# to write a set solver.

T = Integer
def CreateMagicSquare(size, num_solutions=1):
    reset()
    # We would like to create a size x size magic square.  So, we need to create an
    # integer variable for each square.  We use a (nested) list comprehension for this:

    square = [[declare("(" + str(i) + ", " + str(j) + ")", T) for j in range(size)] for i in range(size)]

    flat_square = list(itertools.chain.from_iterable(square)) # Reduces one level of nesting 
    assume(Distinct(flat_square))
    for i in flat_square:
        assume(i >= 0)

    sum_rows = [sum(row) for row in square]
    sum_columns = [sum(col) for col in zip(*square)] # Neat trick to get the transpose
    sum_diagonals = [0, 0]
    for i in range(size):
        sum_diagonals[0] += square[i][i]
        sum_diagonals[1] += square[i][size - i - 1]
    sum_all = sum_rows + sum_columns + sum_diagonals
    magic_constant = sum_all.pop() # Has different solutions from sum_all[0]. Why?
    for s in sum_all:
        assume(s == magic_constant)
    # Distinct(-)
    # And(-), Or(-), Not(-), Implies(-)
    return solve(num_solutions)

N = 4 
print("-"*26)
for square in CreateMagicSquare(N):
    print_2D_array(square, N)
    print("-" * 26)

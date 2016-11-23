from solver import *

# This file contains an example of how to use the necessary Z3 features
# to write a set solver.

# We begin simple:
#   Suppose we want to write a modular equation solver.
#   That is "What integer x solves the equation a*x mod m = b mod m".
def SolveModularEquation(a, b, m):
    # We begin by resetting the solver.  This removes all variables and constraints
    # so we can solve a new problem.
    reset()

    # The "x" in the equation is a variable.  So, we need to define it.  We also must
    # tell Z3 what "type" it is.  The only "built-in" types we care about are "Integer"
    # and "Boolean".
    x = declare("x", Integer)

    # In Z3, there are many useful built-in functions that we can use.  In particular,
    # even though our equation will have a variable in it, we can still use ==, !=, <, >, %, etc.
    # To tell Z3 that we want to insist that something is true, we use "assume":
    assume(a*x % m == b % m)

    # In this case, we want to add a section assertion that x is in the right range.
    # Z3 also has built-in relational operators: And, Or, Not, Implies
    assume(And(0 <= x, x < m)) 

    # Now, we ask Z3 to solve the equation for us.  If we give solve() no arguments,
    # it will find all solutions.  Otherwise, we give it the maximum number of solutions
    # we want it to find.
    return solve(20)

# Try it out...
print(SolveModularEquation(13, 21, 5))
print(SolveModularEquation(10, 20, 4))
print(SolveModularEquation(1000, 1, 21))

# Try omitting the range assumption to see what happens!

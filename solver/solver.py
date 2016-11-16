from z3 import *

from itertools import product

## Global State #########
CONSTANTS_BY_NAME = set()
CONSTANTS = set()
FUNCTIONS = set()
FUNCTION_DOMAINS = {}
ASSUMPTIONS = set()
SOLVER = Solver()
#########################

def uniqer():
    i = [-1]
    def uniq():
        i[0] += 1
        return "_" + str(i[0])
    return uniq
uniq = uniqer()


Boolean = BoolSort()
Integer = IntSort()
Character = BitVecSort(8)

def sort(name, L):
    return EnumSort(name, L)

def declare(L, t1, t2=None, domain=None):
    out = []

    if not isinstance(L, (list, tuple)): L = [L]
    if not isinstance(t1, (list, tuple)): t1 = [t1]

    for x in L:
        if x in CONSTANTS_BY_NAME:
            raise Z3Exception("You may not define two constants or functions with the same name!")
        CONSTANTS_BY_NAME.add(x)
        A = [x] + t1 if t2 is None else [x] + t1 + [t2]
        out.append(Const(*A) if t2 is None else Function(*A))
        if t2 is None:
            CONSTANTS.add(out[-1])
        else:
            FUNCTIONS.add(out[-1])
            if domain is not None:
                FUNCTION_DOMAINS[out[-1]] = domain
    return tuple(out) if len(out) > 1 else out[0]

def assume(P):
    ASSUMPTIONS.add(P)
    SOLVER.add(P)

def reset():
    global SOLVER, CONSTANTS_BY_NAME, CONSTANTS, FUNCTIONS, FUNCTION_DOMAINS, ASSUMPTIONS
    SOLVER = Solver()
    ASSUMPTIONS = set()
    CONSTANTS_BY_NAME = set()
    CONSTANTS = set()
    FUNCTIONS = set()
    FUNCTION_DOMAINS = {}

def from_start():
    global SOLVER
    SOLVER = Solver()
    for A in ASSUMPTIONS:
        SOLVER.add(A)

def solve(MIN=0):
    i = 0

    out = []

    while sat == SOLVER.check() and (i < MIN or MIN <= 0):
        m = SOLVER.model()
        decls = m.decls()

        solution = set([])

        outf = {}
        for c in CONSTANTS:
            interp = m.get_interp(c)
            solution.add(c == interp)
            outf[str(c)] = interp

        for f in FUNCTIONS: 
            f_out = {}
            interp = m.get_interp(f)
            if interp is None:
                continue

            _interp = interp.as_list()

            if len(_interp) > 1:
                for idx in range(len(_interp) - 1):
                    k = _interp[idx][:-1]
                    v = _interp[idx][-1] 
                    _interp[idx] = [k, v]

            fixed = _interp[:-1]
            others = _interp[-1]

            fixed_args = set()

            for x, V in fixed:
                f_out[str(x)[1:-1]] = simplify(V)
                solution.add(f(x) == V)
                fixed_args.add(tuple(x))

            domain = []
            if f in FUNCTION_DOMAINS:
                domain = FUNCTION_DOMAINS[f]
            else:
                for arg in range(f.arity()): 
                    domain.append(set())
                    try:
                        for idx in range(f.domain(arg).num_constructors()):
                            domain[-1].add(f.domain(arg).constructor(idx)())
                    except AttributeError:
                        raise Z3Exception("Only finite domains are allowed for this question")

            for I in set(product(*domain)):
                if str(list(I))[1:-1] not in f_out:
                    f_out[str(list(I))[1:-1]] = simplify(others)
                    solution.add(f(I) == others)

            constructors = []
            if f not in FUNCTION_DOMAINS:
                for arg in range(f.arity()): 
                    constructors.append(set())
                    try:
                        for idx in range(f.domain(arg).num_constructors()):
                            constructors[-1].add(f.domain(arg).constructor(idx)())
                    except AttributeError:
                        raise Z3Exception("Only finite domains are allowed for this question")

                    covered = set([next(iter(x[0])) for x in _interp[:-1]])
                    for x in covered:
                        constructors[-1].remove(x)

            if f in FUNCTION_DOMAINS:
                _interp = _interp[:-1]
            elif len(constructors[-1]) > 0:
                _interp[-1] = (constructors + [_interp[-1]])
            else:
                _interp = _interp[:-1]

            _interp = [(L[:-1], L[-1]) for L in _interp]
            outf[str(f) + ("(" + str(k)[1:-1] + ")" if f not in FUNCTION_DOMAINS else "")] = f_out

        out.append(outf)

        
        SOLVER.add(Not(And(*solution)))
        i += 1

    if sat != SOLVER.check():
        from_start()

    sorted(out, key=lambda x:str(x))
    return out

def AllEqual(L):
    if len(L) == 0:
        return True
    b = [] 
    for x in L[1:]:
        b.append(L[0] == x)
    return And(*b)

def ExactlyN(b, n):
    if n == 0:
        return True 
    else:
        out = False
        for i in range(len(b)):
            out = Or(out, And(b[i], ExactlyN(b[:i] + b[i + 1:], n - 1)))
        return simplify(out)

def print_2D_array(square, size):
    result = [[0 for x in range(size)] for y in range(size)]
    for pos in square:
        if pos.startswith("("):
            x, y = tuple([int(z) for z in pos[1:-1].replace(" ", "").split(",")])
            result[x][y] = square[pos]

    s = [[str(e) for e in row] for row in result]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

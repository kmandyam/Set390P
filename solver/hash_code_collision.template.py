from solver import *

def hashCode(s):
    h = 0
    for byte in s:
        h = h * 31 + ZeroExt(32, byte)
    return h

def is_letter(x):
    # Hint: ord is useful here
    # Fill me in!
    return And(ord(x) >= ord('a') and ord(x) <= ord('z') or ord(x) >= ord('A') and ord(x) <= ord('Z')) 

def get_bits(s):
    return [BitVecVal(ord(x), 8) for x in s]

# Return an iterable of all strings of size SIZE that have the same hashcode as original
def collide(original, SIZE):
    reset()
    orig = get_bits(original)

    # Fill me in!
    output=[]
    bit_vec = declare("bit_vec", BitVecSort(8))
    list_bv = [declare(str(i), BitVecSort(8)) for i in range(SIZE)]
    assume(hashCode(list_bv) == hashCode(orig))
    return solve(100)


print(BitVecSort(8))
WORD = "deer"
for i in range(len(WORD) + 1):
    print("Searching " + str(i) + "...")
    for ans in collide(WORD, i):
        print(ans)

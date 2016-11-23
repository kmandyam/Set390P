from solver import *

def hashCode(s):
    h = 0
    for byte in s:
        h = h * 31 + ZeroExt(32, byte)
    return h

def is_letter(x):
    # Hint: ord is useful here
    # Fill me in!
    return True

def get_bits(s):
    return [BitVecVal(ord(x), 8) for x in s]


def collide(original, SIZE):
    reset()
    orig = get_bits(original)

    # Fill me in!

    return output

WORD = "deer"
for i in range(len(WORD) + 1):
    print("Searching " + str(i) + "...")
    for ans in collide(WORD, i):
        print(ans)

from functools import reduce

bits = [1,0,0,1,0,1,0,0,0,1,0,1,1,0,1,1]

'''
def hamming(bits):
    return reduce(
        lambda x, y: x ^ y,
        [i for (i, b) in enumerate(bits)]
    )
'''

def calc(x, y):
    print("Calculating " + str(x) + " " + str(y))
    return x ^ y

def hamming(bits):
    return reduce(
        calc,
        [i for (i, b) in enumerate(bits)]
    )

print(hamming(bits))
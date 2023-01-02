def getUpperHalf1(c):
    return int(((c - 0x10000) - (c % 0x400)) / 0x400) + 0xd800

def getUpperHalf2(c):
    return int(((c - 65536) - (c % 1024)) / 1024) + 55296

'''
High:

( (C - 65536) - (C % 1024) ) / 1024 + 55296

'''

def getLowerHalf1(c):
    return (c % 0x400) + 0xdc00

def getLowerHalf2(c):
    return (c % 1024) + 56320

'''
Low:

(C % 1024) + 56320

'''

'''

*High Surrogate (first): {{Math|((C - 65536) - (C % 1024)) / 1024 + 55296}}
*Low Surrogate (second): {{Math|(C % 1024) + 56320}}

'''

#point = 0x1f603 # mc wiki example
#point = 0x10437 # wikipedia example

point = 0x1f9ea # tube

print('Input:')
print(hex(point))

print('Result 1:')
print(hex(getUpperHalf1(point)))
print(hex(getLowerHalf1(point)))

print('Result 2:')
print(hex(getUpperHalf2(point)))
print(hex(getLowerHalf2(point)))

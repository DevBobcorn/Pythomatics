atlasSize = 4096
textureSize = 16

texPerLine = int(atlasSize / textureSize)

def getUpperHalf(c):
    return int(((c - 0x10000) - (c % 0x400)) / 0x400) + 0xd800

def getLowerHalf(c):
    return (c % 0x400) + 0xdc00

def getCodeForIndex(index: int): # index range: [0, 65536)
    #print(index)

    if index < 0x1900: # index range [0, 6400)
        # Use Unicode Private Use Area U+E000 to U+F8FF (6400 code points)
        return f'\\u{((hex(index + 0xe000))[2:]).zfill(4)}'
    elif index <= 0xffff: # index range [6400, 65536)
        # Use Unicode Private Use Area-A U+F0000 to U+FE6FF (59136 code points)
        codePoint = 0xf0000 + (index - 0x1900)
        return f'\\u{hex(getUpperHalf(codePoint))[2:]}\\u{hex(getLowerHalf(codePoint))[2:]}'
    else: # Treat as 0
        return '\\ue000'

with open(r'mc_glyph\glyph_mapping.json', 'w+') as f:
    for i in range(texPerLine):
        f.write(',\n\"')

        for j in range(texPerLine):
            index = (i << 8) + j
            f.write(getCodeForIndex(index))
        
        f.write('\"')

# Horizontal stripes ===========================================
print('/tellraw @a "', end='')

for i in range(4): # Red to Yellow
    glyphIndex = 0

    for proc in range(i + 1):
        glyphIndex |= 1 <<  proc
        glyphIndex |= 1 << (proc +  4)
        glyphIndex |= 1 << (proc +  8)
        glyphIndex |= 1 << (proc + 12)
    
    print(getCodeForIndex(glyphIndex), end='')

for i in range(4): # Yellow to Red
    glyphIndex = 0

    for proc in range(i + 1):
        glyphIndex |= 1 <<  proc
        glyphIndex |= 1 << (proc +  4)
        glyphIndex |= 1 << (proc +  8)
        glyphIndex |= 1 << (proc + 12)
    
    glyphIndex = (~glyphIndex) & 0xffff
    
    print(getCodeForIndex(glyphIndex), end='')


print('"')

# Vertical stripes =============================================
print('/tellraw @a "', end='')

for i in range(4):
    glyphIndex = 0

    for proc in range(i + 1):
        glyphIndex |= 1 <<  (proc * 4)
        glyphIndex |= 1 << ((proc * 4) + 1)
        glyphIndex |= 1 << ((proc * 4) + 2)
        glyphIndex |= 1 << ((proc * 4) + 3)
    
    print(getCodeForIndex(glyphIndex), end='')

for i in range(4):
    glyphIndex = 0

    for proc in range(i + 1):
        glyphIndex |= 1 <<  (proc * 4)
        glyphIndex |= 1 << ((proc * 4) + 1)
        glyphIndex |= 1 << ((proc * 4) + 2)
        glyphIndex |= 1 << ((proc * 4) + 3)
    
    glyphIndex = (~glyphIndex) & 0xffff
    
    print(getCodeForIndex(glyphIndex), end='')

print('"')
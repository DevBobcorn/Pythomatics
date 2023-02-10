from math import log

atlasSize = 1024
textureSize = 16

texPerLine = int(atlasSize / textureSize)
bitsPerValue = int(log(texPerLine, 2))

print(f'Bits per value: {bitsPerValue}')

indexOffset = 65536

def getUpperHalf(c):
    return int(((c - 0x10000) - (c % 0x400)) / 0x400) + 0xd800

def getLowerHalf(c):
    return (c % 0x400) + 0xdc00

def getCodeForIndex(index: int): # index range: [0, 65536)
    if index < 0x1900: # index range [0, 6400)
        # Use Unicode Private Use Area U+E000 to U+F8FF (6400 code points)
        return f'\\u{((hex(index + 0xe000))[2:]).zfill(4)}'
    elif index < 71934: # index range [6400, 71934)
        # Use Unicode Private Use Area-A U+F0000 to U+FFFFD (65534 code points)
        codePoint = 0xf0000 + (index - 0x1900)
        return f'\\u{hex(getUpperHalf(codePoint))[2:]}\\u{hex(getLowerHalf(codePoint))[2:]}'
    else: # Treat as 0
        return '\\ue000'

with open(r'mc_glyph\glyph_mapping.json', 'w+') as f:
    for i in range(texPerLine):
        f.write(',\n\"')

        for j in range(texPerLine):
            index = (i << bitsPerValue) + j + indexOffset
            f.write(getCodeForIndex(index))
        
        f.write('\"')

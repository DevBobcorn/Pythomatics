import cv2

atlasSize = 4096
textureSize = 16

texPerLine = int(atlasSize / textureSize)

def getUpperHalf(c):
    return int(((c - 0x10000) - (c % 0x400)) / 0x400) + 0xd800

def getLowerHalf(c):
    return (c % 0x400) + 0xdc00

def getCodeForIndex(index: int): # index range: [0, 65536)
    if index < 0x1900: # index range [0, 6400)
        # Use Unicode Private Use Area U+E000 to U+F8FF (6400 code points)
        return f'\\u{((hex(index + 0xe000))[2:]).zfill(4)}'
    else: # index range [6400, 65536)
        # Use Unicode Private Use Area-A U+F0000 to U+FE6FF (59136 code points)
        codePoint = 0xf0000 + (index - 0x1900)
        return f'\\u{hex(getUpperHalf(codePoint))[2:]}\\u{hex(getLowerHalf(codePoint))[2:]}'

def GetMapping():
    mapping = { }

    for i in range(texPerLine):
        for j in range(texPerLine):
            index = (i << 8) + j
            mapping[index] = getCodeForIndex(index)
    
    return mapping

def GetGlyphPoints(ix: int, iy: int):
    if iy == 0:
        return [(ix, iy)]
    if iy == 2:
        return [(ix, iy + 1)]
    
    # Otherwise iy is 1
    return [(ix, iy), (ix, iy + 1)]

sourceImagePath = 'mc_glyph\\apple-140-87.png'

# Load the source image
source = cv2.imread(sourceImagePath)

srch, srcw, srcc = source.shape # Height, Width and Channels

unitw = 4
unith = 4

srcw = srcw - (srcw % unitw)
srch = srch - (srch % unith)

unitCntX = int(srcw / unitw)
unitCntY = int(srch / unith)

codes = [[0 for i in range(unitCntX)] for j in range(unitCntY)]

for uy in range(unitCntY):
    for ux in range(unitCntX):
        xpos = ux * unitw
        ypos = uy * unith
        for iy in range(4):
            for ix in range(4):
                posIndex = iy * 4 + ix

                px = xpos + ix
                py = ypos + iy
                    
                # Sample the color on source image at (px, py)
                if source[py, px][0] > 127:
                    codes[uy][ux] = codes[uy][ux] | (1 << posIndex)
        
        #print(f"{hex(codes[uy][ux])}"[2:].zfill(3), end = ' ')
    #print()

mapping = GetMapping()

savePath = 'C:\\Users\\DevBo\\AppData\\Roaming\\.minecraft\\saves\\FONTEST\\datapacks\\mc_glyph'

with open(f'{savePath}\\data\\glyph_image\\functions\\test.mcfunction', 'w+') as f:
    for i in range(unitCntY):
        a = "tellraw @a {\"text\":\""
        for j in range(unitCntX):
            a += mapping[codes[i][j]]

        a += "\"}\n"

        f.write(a)

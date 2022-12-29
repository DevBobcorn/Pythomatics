import cv2

def GetMapping():
    mapping = { }

    for i in range(64):
        for j in range(64):
            index = (i << 6) + j
            mapping[index] = f"\\ue{((hex(index))[2:]).zfill(3)}"
    
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
        for iy in range(3):
            for ix in range(4):
                pts = GetGlyphPoints(ix, iy)
                posIndex = iy * 4 + ix

                sample = 0

                for pt in pts:
                    px = xpos + ix
                    py = ypos + iy
                    
                    # Sample the color on source image at (px, py)
                    sample += source[py, px][0]

                if sample / len(pts) > 127:
                    codes[uy][ux] = codes[uy][ux] | (1 << posIndex)
        
        #print(f"{hex(codes[uy][ux])}"[2:].zfill(3), end = ' ')
    #print()

mapping = GetMapping()

savePath = 'C:\\Users\\DevBo\\AppData\\Roaming\\.minecraft\\saves\\FONTEST\\datapacks'

with open(f'{savePath}\\mc_glyph\\data\\glyph_image\\functions\\test.mcfunction', 'w+') as f:
    for i in range(unitCntY):
        a = "tellraw @a {\"text\":\""
        for j in range(unitCntX):
            a += mapping[codes[i][j]]

        a += "\"}\n"

        f.write(a)

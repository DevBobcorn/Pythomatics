import cv2
import numpy as np

enableBlending = False

unitW = 4
unitH = 3

textureSize = 16
pixelSize = int(textureSize / unitW)

def ClampInt(val: int, minVal: int, maxVal: int):
    return max(minVal, min(maxVal, val))

def ClampFloat(val: float, minVal: float, maxVal: float):
    return max(minVal, min(maxVal, val))

def GetGlyphPoints(ix: int, iy: int):
    if iy == 0:
        return [(ix, iy)]
    if iy == unitH - 1:
        return [(ix, iy + 1)]
    
    # Otherwise iy is between 0 and unitH - 1
    return [(ix, iy), (ix, iy + 1)]

def GetPosIndex(ix: int, iy: int):
    return iy * unitW + ix

def GetClampedPosIndex(ix: int, iy: int):
    return ClampInt(iy, 0, unitH - 1) * unitW + ClampInt(ix, 0, unitW - 1)

def GetNeighborPosIndices(ix: int, iy: int):
    indices = []
    indices.append(GetClampedPosIndex(ix - 1, iy))
    indices.append(GetClampedPosIndex(ix + 1, iy))
    indices.append(GetClampedPosIndex(ix, iy - 1))
    indices.append(GetClampedPosIndex(ix, iy + 1))

    return indices

def BlendSamples(sampleB, sampleA, blendFactor: float):
    return sampleB + (sampleA - sampleB) * blendFactor

# Pre-calculate these for they're intensively accessed
def GetNeighborPosIndexMapping():
    mapping = { }
    for y in range(0, unitH):
        for x in range(0, unitW):
            mapping[x, y] = GetNeighborPosIndices(x, y)
    
    return mapping

neighborPosIndexMapping = GetNeighborPosIndexMapping()

#textureA = cv2.imread('mc_glyph\\diamond_block.png', cv2.IMREAD_UNCHANGED)
#textureB = cv2.imread('mc_glyph\\emerald_block.png', cv2.IMREAD_UNCHANGED)
#textureA = cv2.imread('mc_glyph\\apple.png', cv2.IMREAD_UNCHANGED)
#textureB = cv2.imread('mc_glyph\\golden_apple.png', cv2.IMREAD_UNCHANGED)
textureA = cv2.imread('mc_glyph\\white.png', cv2.IMREAD_UNCHANGED)
textureB = cv2.imread('mc_glyph\\black.png', cv2.IMREAD_UNCHANGED)

 # Flip the images both vertically and horizontally
textureA = textureA.transpose(1, 0, 2)
textureB = textureB.transpose(1, 0, 2)

glyphAtlas = np.arange(65536 * pixelSize * pixelSize * 4)
glyphAtlas = glyphAtlas.reshape(256 * pixelSize, 256 * pixelSize, 4)

blendXp = [0, 1]

# For each single glyph texture in the atlas
for ih in range(64):
    for iw in range(64):
        glyphIndex = (ih << 6) + iw
        ypos = ih * 4
        xpos = iw * 4

        # For each part on this glyph
        for iy in range(unitH):
            for ix in range(unitW):
                pts = GetGlyphPoints(ix, iy)

                for pt in pts: # For each point on this part
                    ptx = xpos + pt[0]
                    pty = ypos + pt[1]

                    # For each final pixel on this point
                    for pxx in range(pixelSize):
                        for pxy in range(pixelSize):
                            px = ptx * pixelSize + pxx
                            py = pty * pixelSize + pxy

                            samplex = pt[0] * pixelSize + pxx
                            sampley = pt[1] * pixelSize + pxy

                            sampleA = textureA[samplex, sampley]
                            sampleB = textureB[samplex, sampley]

                            blendFactor = 0 # 0 means B, 100 means A

                            if ((glyphIndex >> GetPosIndex(ix, iy)) & 1) != 0:
                                blendFactor = 1.0
                            else:
                                blendFactor = 0.0
                            
                            if enableBlending:
                                # Check horizontal neighbors
                                if pxx == 0:
                                    if ((glyphIndex >> GetClampedPosIndex(ix - 1, iy)) & 1) != 0:
                                        blendFactor += 0.4
                                    else:
                                        blendFactor -= 0.4
                                elif pxx == pixelSize - 1:
                                    if ((glyphIndex >> GetClampedPosIndex(ix + 1, iy)) & 1) != 0:
                                        blendFactor += 0.4
                                    else:
                                        blendFactor -= 0.4
                                
                                # Check vertical neighbors
                                if pxy == 0:
                                    if ((glyphIndex >> GetClampedPosIndex(ix, iy - 1)) & 1) != 0:
                                        blendFactor += 0.4
                                    else:
                                        blendFactor -= 0.4
                                elif pxy == pixelSize - 1:
                                    if ((glyphIndex >> GetClampedPosIndex(ix, iy + 1)) & 1) != 0:
                                        blendFactor += 0.4
                                    else:
                                        blendFactor -= 0.4
                            
                                # Clamp the blending factor after tweaking
                                blendFactor = ClampFloat(blendFactor, 0.0, 1.0)
                            
                            
                            glyphAtlas[px, py] = [
                                np.interp(blendFactor, blendXp, [sampleA[0], sampleB[0]]),
                                np.interp(blendFactor, blendXp, [sampleA[1], sampleB[1]]),
                                np.interp(blendFactor, blendXp, [sampleA[2], sampleB[2]]),
                                np.interp(blendFactor, blendXp, [sampleA[3], sampleB[3]])
                            ]
                            
                            # Set alpha to at least 20, otherwise MC's gonna trim the transparent part
                            glyphAtlas[px, py, 3] = max(20, glyphAtlas[px, py, 3])

        #print(f"({i}, {j}) ", end = '')
    #print()

# Flip the image both vertically and horizontally
glyphAtlas = glyphAtlas.transpose(1, 0, 2)

cv2.imwrite('mc_glyph\\example_resource\\assets\\minecraft\\textures\\font\\test.png', glyphAtlas)

resPath = 'C:\\Users\\DevBo\\AppData\\Roaming\\.minecraft\\resourcepacks'
cv2.imwrite(f'{resPath}\\mc_glyph\\assets\\minecraft\\textures\\font\\test.png', glyphAtlas)

'''
chars = '' #=========================================== E000 TO E7FF

for i in range(32):
    print(f"{(63 << 6) + 63}")
    chars += ',\n\"'
    for j in range(64):
        index = (i << 6) + j
        chars += f"\\ue{((hex(index))[2:]).zfill(3)}"



print(chars)

chars = '' #=========================================== E800 TO EFFF

for i in range(64):
    print(f"{(63 << 6) + 63}")
    chars += ',\n\"'
    for j in range(64):
        index = (i << 6) + j
        chars += f"\\ue{((hex(index))[2:]).zfill(3)}"
    
    chars += '\"'

print(chars)
'''
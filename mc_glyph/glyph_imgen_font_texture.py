import cv2
import numpy as np

enableBlending = True

unitW = 4
unitH = 4

atlasSize = 4096
textureSize = 16

pixelSize = int(textureSize / unitW)
texPerLine = int(atlasSize / textureSize)

def ClampInt(val: int, minVal: int, maxVal: int):
    return max(minVal, min(maxVal, val))

def ClampFloat(val: float, minVal: float, maxVal: float):
    return max(minVal, min(maxVal, val))

def GetPosIndex(ix: int, iy: int):
    return iy * unitW + ix

def GetClampedPosIndex(ix: int, iy: int):
    return ClampInt(iy, 0, unitH - 1) * unitW + ClampInt(ix, 0, unitW - 1)

def BlendSamples(sampleB, sampleA, blendFactor: float):
    return sampleB + (sampleA - sampleB) * blendFactor

#textureA = cv2.imread('mc_glyph\\diamond_block.png', cv2.IMREAD_UNCHANGED)
#textureB = cv2.imread('mc_glyph\\emerald_block.png', cv2.IMREAD_UNCHANGED)
textureA = cv2.imread('mc_glyph\\apple.png', cv2.IMREAD_UNCHANGED)
textureB = cv2.imread('mc_glyph\\golden_apple.png', cv2.IMREAD_UNCHANGED)

 # Flip the images both vertically and horizontally
textureA = textureA.transpose(1, 0, 2)
textureB = textureB.transpose(1, 0, 2)

glyphAtlas = np.empty((atlasSize, atlasSize, 4), dtype=int)

blendXp = [0, 1]

sampleA = [   0,   0,   0,   0 ]
sampleB = [ 255, 255, 255, 255 ]

# For each single glyph texture in the atlas
for ih in range(texPerLine):
    print(f'{(ih / (texPerLine - 1) * 100):.2f}% complete')
    for iw in range(texPerLine):
        glyphIndex = (ih << 8) + iw
        ypos = ih * 4
        xpos = iw * 4

        # For each part on this glyph
        for iy in range(unitH):
            for ix in range(unitW):
                ptx = xpos + ix
                pty = ypos + iy

                # For each final pixel on this point
                for pxx in range(pixelSize):
                    for pxy in range(pixelSize):
                        px = ptx * pixelSize + pxx
                        py = pty * pixelSize + pxy

                        samplex = ix * pixelSize + pxx
                        sampley = iy * pixelSize + pxy

                        #sampleA = textureA[samplex, sampley]
                        #sampleB = textureB[samplex, sampley]
                        
                        if enableBlending:
                            blendFactor = 0 # 0 means B, 100 means A

                            if ((glyphIndex >> GetPosIndex(ix, iy)) & 1) != 0:
                                blendFactor = 1.0
                            else:
                                blendFactor = 0.0

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
                        else:
                            if ((glyphIndex >> GetPosIndex(ix, iy)) & 1) != 0:
                                glyphAtlas[px, py] = sampleB
                            else:
                                glyphAtlas[px, py] = sampleA
                        
                        # Set alpha to at least 20, otherwise MC's gonna trim the transparent part
                        glyphAtlas[px, py, 3] = max(20, glyphAtlas[px, py, 3])

        #print(f"({i}, {j}) ", end = '')
    #print()

# Flip the image both vertically and horizontally
glyphAtlas = glyphAtlas.transpose(1, 0, 2)

resPath = 'C:\\Users\\DevBo\\AppData\\Roaming\\.minecraft\\resourcepacks'
cv2.imwrite(f'{resPath}\\mc_glyph\\assets\\minecraft\\textures\\font\\test.png', glyphAtlas)

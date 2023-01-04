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

mapping = GetMapping()

cap = cv2.VideoCapture(r'mc_glyph/bad_apple.mp4')

unitw = 4
unith = 4

step = 1

width  = 136
height =  88

unitCntX = int(width  / unitw)
unitCntY = int(height / unith)

time = -1
cnt = 0

tpf = 1 # Tick per frame

start = 0
limit = 10000

outPath = 'C:/Users/DevBo/AppData/Roaming/.minecraft/saves/FONTEST/datapacks/mc_glyph/data/glyph_image/functions'

def getCallCommand(tick, frame):
    return f'execute if score @p play_tick matches {tick} run function glyph_image:f/{frame}\n'

# Output clear up function
emptyCode = getCodeForIndex(0)
emptyLine = ''

for ux in range(unitCntX):
    emptyLine += emptyCode

with open(f'{outPath}/core/clear.mcfunction', 'w+') as f:
    f.write('scoreboard objectives remove play_tick\n')

    for uy in range(unitCntY):
        f.write(f'tellraw @a "{emptyLine}"\n')

# Output video function
with open(f'{outPath}/core/tick.mcfunction', 'w+') as script:
    while True:
        time += 1
        
        # Get a frame
        ret, image = cap.read()
        
        if (image is None) or (cnt > limit):
            break

        flag = (time % step) == 0

        if flag and time >= start: # Use this frame, otherwise skip
            cnt += 1 # Increase frame count
            print(f'Generating frame {cnt}')
            
            image = cv2.resize(image, (width, height))

            frameChanged = False

            tickCnt = cnt * tpf

            # Register this frame
            script.write(getCallCommand(tickCnt, cnt))

            # Output this frame
            with open(f'{outPath}/f/{tickCnt}.mcfunction', 'w+') as f:
                for uy in range(unitCntY):
                    command = 'tellraw @a "'

                    for ux in range(unitCntX):
                        xpos = ux * unitw
                        ypos = uy * unith

                        glyphIdx = 0

                        for iy in range(unith):
                            for ix in range(unitw):
                                posIndex = iy * 4 + ix
                                px = xpos + ix
                                py = ypos + iy
                                    
                                # Sample the color on source image at (px, py)
                                if image[py, px][0] > 127:
                                    glyphIdx = glyphIdx | (1 << posIndex)
                        
                        command += getCodeForIndex(glyphIdx)
                    
                    command += '"\n'
                    f.write(command)

    script.write('execute if score @p play_tick matches 0.. run scoreboard players add @p play_tick 1\n')
    script.write(f'execute if score @p play_tick matches {cnt * tpf + 10}.. run scoreboard players add @p play_tick 1')

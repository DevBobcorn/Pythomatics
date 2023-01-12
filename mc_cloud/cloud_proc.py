import numpy as np
import cv2

atlasSize = 4096

videoPath = 'mc_cloud/bad_apple.mp4'

orgCloudPath = 'mc_cloud/clouds_xxxl.png'
outPath = 'mc_cloud/clouds.png'

cap = cv2.VideoCapture(videoPath)

unitw = 64
unith = 48

step = 1

unitCntX = int(atlasSize / unitw)
unitCntY = int(atlasSize / unith)

time = -1
cnt = 0

tpf = 1 # Tick per frame

start = 0
limit = 10000

atlas = np.empty((atlasSize + atlasSize, atlasSize, 4), dtype=int)

# Output video function
while True:
    time += 1
    
    # Get a frame
    ret, image = cap.read()
    
    if (image is None) or (cnt > limit):
        break

    flag = (time % step) == 0

    if flag and time >= start: # Use this frame, otherwise skip
        cnt += 1 # Increase frame count
        print(f'Generating frame {cnt}...')
        
        image = cv2.resize(image, (unitw, unith))

        spriteX = cnt % unitCntX
        spriteY = int(cnt / unitCntX)

        posX = spriteX * unitw
        posY = spriteY * unith

        # Output this frame
        #atlas[posY:posY + unith, posX:posX + unitw] = image

        for y in range(unith):
            for x in range(unitw):
                atlas[posY + y, posX + x] = [ 255, 255, 255, image[y, x][0] ]

print(f'Pasting original cloud texture...')
orgCloud = cv2.imread(orgCloudPath, cv2.IMREAD_UNCHANGED)

for y in range(atlasSize):
    for x in range(atlasSize):
        atlas[atlasSize + y, x] = orgCloud[y, x]

cv2.imwrite(outPath, atlas)
import glob, os

curdir = os.path.dirname(os.path.abspath(__file__))

sourceDir   = 'res\m13_p12' # 'src' 'res\m13_p12'
magic       = -13
procByteCnt =  12

saveInPlace = False

print(f'Start proc under {curdir}')

for path in glob.glob(fr'{curdir}\{sourceDir}\*.*'):
    print(f'Processing {path}...')
    with open(path, mode = 'r+b') as file:
        bts = list(file.read(procByteCnt))
        #print(f'File pointer pos: {file.tell()}')

        for bi in range(len(bts)):
            byte = bts[bi]
            bts[bi] = (byte + magic + 256) % 256
            #print(str(byte) + ' ' + str(bts[bi]))

        if saveInPlace:
            file.seek(0) # Reset file pointer
            file.write(bytes(bts))
        else:
            savePath = fr'{curdir}\res\m{magic}_p{procByteCnt}\{os.path.basename(path)}'
            print(f'Saving processed file to {savePath}')
            # Create directory if not present
            os.makedirs(fr'{curdir}\res\m{magic}_p{procByteCnt}', exist_ok = True)

            with open(savePath, 'wb') as saveFile:
                bytesLeft = file.read()
                saveFile.write(bytes(bts))
                saveFile.write(bytesLeft)

print('End proc')

import json

srcPath = 'mc_atlas/hut.txt'
outPath = 'C:/Users/DevBo/AppData/Roaming/.minecraft/saves/23_06AppleShot/datapacks/mc_glyph/data/glyph_image/functions'

def main():
    with open('mc_atlas/mc_atlas_dict.json') as f:
        dictJson = json.load(f)

        with open(srcPath, 'r+') as src:
            srcLines = src.readlines()

            mode = 0 # 0: None   1: Ascii art   2: Char Map
            asciiLines = [ ]
            charMap = { }

            for srcLine in srcLines:
                if srcLine.startswith('#'): # Mode switch
                    if 'ASCII' in srcLine.upper():
                        mode = 1
                    elif 'CHARS' in srcLine.upper():
                        mode = 2
                    else:
                        print(f'Invalid mode switch: {srcLine}, mode remains unchanged')
                else: # Data
                    if mode == 1:
                        srcLine = srcLine.replace('\n', '')

                        asciiLines.append(srcLine)
                    elif mode == 2:
                        srcLine = srcLine.rstrip()

                        if srcLine == '': # Skip empty lines
                            continue
                        
                        charData = srcLine.split(' ')
                        charKey = charData[0] # Ascii character
                        charValue = charData[1] # Glyph resource location

                        if charKey.upper() == 'SPACE':
                            charKey = ' '

                        if charValue in dictJson.keys():
                            charMap[charKey] = dictJson[charValue]['code']

                            # print(f'[{charKey}] => {charValue} => {charMap[charKey]}')
                        else:
                            print(f'Character glyph not defined: {charValue}')
                
            resultLines = [ ]

            '''
            for asciiLine in asciiLines:
                resultLine = ''

                for c in asciiLine:
                    if c in charMap.keys():
                        resultLine += charMap[c]
                    else:
                        #print(f'[{c}] is not defined in character map')
                        resultLine += c
                
                resultLines.append(resultLine)
            '''

            # 14 7 30 19 (+16 +12) 4 * (+4 +3)
            for ll in range(19):
                resultLine = ''

                for c in range(30):
                    resultLine += '\\ue000' # charMap['Q']
                
                resultLines.append(resultLine)
            
            resultText = '\\n'.join(resultLines).replace('\\', '\\\\')

            command = 'data modify entity @e[type=minecraft:text_display,limit=1] text set value \'{"text":"' + resultText + '"}\'\n'

            #print(command)

            with open(f'{outPath}/next4.mcfunction', 'w+') as f:
                f.write(command)

if __name__ == '__main__':
    main()
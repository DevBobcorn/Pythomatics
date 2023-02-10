import re, base64, json

root = 'mc_lyric/lyrics'

srcName = 'bad_apple' # 'キタニタツヤ - 悪夢'

class LyricWord:
    def __init__(self, start: int, end: int, txt: str):
        self.startTime = start
        self.endTime = end
        self.text = txt

class LyricLine:
    def __init__(self, start: int, duration: int):
        self.startTime = start
        self.duration = duration
        self.words = [ ]
        self.translation = ''
        self.fullText = ''

    def appendWord(self, wordStart: int, wordEnd: int, wordTxt: str):
        newWord = LyricWord(wordStart, wordEnd, wordTxt)
        self.words.append(newWord)
    
    def recalcFullText(self):
        text = ''
        for word in self.words:
            text += word.text
        self.fullText = text

class Lyric:
    def __init__(self):
        self.lines = [ ]

    def appendLine(self, newLn: LyricLine):
        self.lines.append(newLn)
    
    def finalize(self):
        # Special process is required for the last line of lyrics
        lastLine = self.lines[-1]
        lyricEnd = 0

        if lastLine.duration > lastLine.startTime:
            lyricEnd = lastLine.duration
            lastLine.duration = lyricEnd - lastLine.startTime
        else:
            lyricEnd = lastLine.startTime + lastLine.duration
        
        self.endTime = lyricEnd
        self.emptyLine = LyricLine(lyricEnd, 999999)

        # Build time maps
        self.startTimeMap = [ ]
        self.endTimeMap = [ ]

        for line in self.lines:
            self.startTimeMap.append(line.startTime)
            self.endTimeMap.append(line.startTime + line.duration)
            line.recalcFullText()
    
    def getLineIndexAtMilSec(self, milsec: int) -> int:
        if milsec < self.startTimeMap[0]:
            return -1
        
        lnIdx = 0
        while lnIdx < len(self.lines) and milsec > self.endTimeMap[lnIdx]:
            lnIdx += 1
            if lnIdx < len(self.lines) and milsec < self.startTimeMap[lnIdx]:
                return -1
            
        return lnIdx
    
    def getLineAtMilSec(self, milsec: int) -> LyricLine:
        lnIdx = self.getLineIndexAtMilSec(milsec)
        if lnIdx == -1:
            return self.emptyLine
        if lnIdx < len(self.lines):
            return self.lines[lnIdx]
        return self.emptyLine
    
    def getDynamicLineAtMilSec(self, milsec: int) -> tuple:
        lnIdx = self.getLineIndexAtMilSec(milsec)
        if lnIdx == -1:
            return ( '', '', '' , self.emptyLine )
        if lnIdx < len(self.lines):
            line = self.lines[lnIdx]

            lnMilsec = milsec - line.startTime

            prevText = ''
            curText = ''
            nextText = ''

            for word in line.words:
                if word.startTime > lnMilsec:
                    nextText += word.text
                else:
                    if word.endTime >= lnMilsec:
                        curText += word.text
                    else:
                        prevText += word.text
            
            return ( prevText, curText, nextText, line )
        return ( '', '', '' , self.emptyLine )

    def buildFromFile(self, krcTextPath: str):
        with open(krcTextPath, 'r+', encoding='utf-8') as src:
            srcText = src.read()

            title = re.search('\[ti:(.*)\]', srcText).groups()[0]
            artist = re.search('\[ar:(.*)\]', srcText).groups()[0]

            print(f'Processing: {title} - {artist}')

            translationSrc = re.search('\[language:([a-zA-Z0-9+=/]+)\]', srcText).groups()[0]
            translationJsonText = base64.b64decode(translationSrc).decode('utf-8')
            #print(translationJsonText)
            translationJson = json.loads(translationJsonText)
            translationContents = translationJson['content']

            translationLines = [ ]

            for transCont in translationContents:
                if transCont['type'] == 1:
                    transContLines = transCont['lyricContent']
                    for transContLine in transContLines:
                        translationLines.append(transContLine[0])
                    break

            lnDataIter = re.finditer('\[(\d+),(\d+)\](.*)$', srcText, re.M)

            lineCount = 0

            for lineData in lnDataIter:
                lnData = lineData.groups()

                lnStart = int(lnData[0])
                lnEnd = int(lnData[1])
                line = LyricLine(lnStart, lnEnd)

                wdDataIter = re.finditer('<(\d+),(\d+),\d+>([^<]*)', lnData[2])

                for wordData in wdDataIter:
                    wdData = wordData.groups()

                    wdStart = int(wdData[0])
                    wdEnd = int(wdData[1])
                    wdText = wdData[2]

                    line.appendWord(wdStart, wdEnd, wdText)
                
                if lineCount >= len(translationLines):
                    print(f'Line count({lineCount}) more than translation line count({len(translationLines)})')
                else:
                    line.translation = translationLines[lineCount]

                self.appendLine(line)

                lineCount += 1

        self.finalize()

def main():
    lyric = Lyric()
    lyric.buildFromFile(f'{root}/{srcName}.txt')

    msPerTick = 50
    maxRefreshInterval = 30 # Interval in ticks

    tmpText = ''
    lastActiveTick = 0

    for milsec in range(0, lyric.endTime, msPerTick):
        tick = int(milsec / msPerTick)

        #tmpLine = lyric.getLineAtMilSec(ms)
        #tmpLineText = tmpLine.fullText

        aaa = lyric.getDynamicLineAtMilSec(milsec)
        tmpLineText = f'[{aaa[0]}][{aaa[1]}][{aaa[2]}]'

        if tick - lastActiveTick >= maxRefreshInterval or tmpLineText != tmpText:
            tmpText = tmpLineText
            print(f'{milsec}({tick}) => {tmpLineText} | {aaa[3].translation}')

            lastActiveTick = tick

if __name__ == '__main__':
    main()

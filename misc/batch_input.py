from pyautogui import typewrite
import os, time

root_path = f'{os.getcwd()}'

enNameMap = { }
zhNameMap = { }

with open(f'{root_path}/fur_list_en.txt', encoding='utf-8') as enMap:
    for ln in enMap.readlines():
        fur = ln.split(':', 1)

        furNum  = int(fur[0].strip())
        furName = fur[1].strip()
        #print(f'{furNum:7} {furName}')
        enNameMap[furNum] = furName

with open(f'{root_path}/fur_list_zh.txt', encoding='utf-8') as chsMap:
    for ln in chsMap.readlines():
        fur = ln.split(':', 1)

        furNum  = int(fur[0].strip())
        furName = fur[1].strip()
        #print(f'{furNum:7} {furName}')
        zhNameMap[furNum] = furName

time.sleep(1.5)

uid = 10002

for furNum in enNameMap.keys():
    print(f'{furNum:7} | {zhNameMap[furNum]} {enNameMap[furNum]}')
    typewrite(f'g @{uid} {furNum} 20\n')
    time.sleep(0.1)

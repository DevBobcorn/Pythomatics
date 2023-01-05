import json, shutil

cats = [
    'XiuRen',   'MFStar',   'MiStar',   'MyGirl',
    'Imiss',    'BoLoli',   'YouWu',    'Uxing',
    'MiiTao',   'FeiLin',   'WingS',    'Taste',
    'LeYuan',   'HuaYan',   'DKGirl',   'MintYe',
    'YouMi',    'Candy',    'MTMeng',   'Micat',
    'HuaYang',  'XingYan',  'XiaoYu'
]

col2cat  = [ ]
col2desc = [ ]
col2page = [ ]

listLen = 13000

latestCoverIdx = 0

for i in range(listLen):
    col2cat.append(-1)
    col2desc.append('')
    col2page.append('')

for catIdx in range(len(cats)):
    cat = cats[catIdx]

    leadingCatNameLower = f'{cat.lower()}'

    with open(f'web/cats/cat_dict_{cat.lower()}.json') as f:
        catText = f.read()
        catDict = json.loads(catText)

        for coverImgIdx in catDict: # For each collection
            # Remove duplicate leading category names in page url, and getting only
            # the collection index number  (only to deal with a few exceptions)
            colIdx = int(coverImgIdx)

            if colIdx > latestCoverIdx:
                latestCoverIdx = colIdx
    
            if colIdx > 0 and colIdx < listLen:
                if col2cat[colIdx] != -1:
                    print(f'Collection #{colIdx} previously registered in another category! Overwriting! ({cats[col2cat[colIdx]]} => {cats[catIdx]})')

                col2cat[colIdx]  = catIdx
                col2desc[colIdx] = catDict[coverImgIdx]['desc']
                col2page[colIdx] = catDict[coverImgIdx]['pageIdx']
            else:
                print(f'Collection index out of bound: {colIdx}')

targets = [ ]

with open('web/list.txt', 'r') as f:
    for ln in f.readlines():
        targets.append(int(ln))

#for ci in range(1, latestCoverIdx + 1):
#for ci in range(8000, 9000):
for ci in targets:
    catIdx = col2cat[ci]

    if catIdx != -1:
        pageLink = f'[{cats[catIdx]}/{col2page[ci]}]'

        print(f'{str(ci).rjust(5)} {pageLink.ljust(20)} {col2desc[ci].ljust(20)}')

        # Clone the cover file
        shutil.copyfile(f'web/downloaded/covers/{ci}.jpg', f'web/downloaded/selected/{ci}.jpg')
    else:
        print(f'Category for collection #{str(ci)} is unknown')

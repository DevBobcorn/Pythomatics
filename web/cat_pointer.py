import json

cats = [
    'XiuRen',   'MFStar',   'MiStar',   'MyGirl',
    'Imiss',    'BoLoli',   'YouWu',    'Uxing',
    'MiiTao',   'FeiLin',   'WingS',    'Taste',
    'LeYuan',   'HuaYan',   'DKGirl',   'MintYe',
    'YouMi',    'Candy',    'MTMeng',   'Micat',
    'HuaYang',  'XingYan',  'XiaoYu'
]

col2cat = [ ]
listLen = 13000

latestColIdx = 0

for colName in range(listLen):
    col2cat.append(-1)

for catIdx in range(len(cats)):
    cat = cats[catIdx]

    leadingCatNameLower = f'{cat.lower()}'

    with open(f'web/cats/cat_dict_{cat.lower()}.json') as f:
        catText = f.read()
        catDict = json.loads(catText)

        for colName in catDict: # For each collection
            #print(f'{str(colName).rjust(7)} {catDict[colName]}')

            # Remove duplicate leading category names in page url, and getting only
            # the collection index number  (only to deal with a few exceptions)
            colIdx = int(colName.lower().replace(leadingCatNameLower, '').replace('/', ''))

            if colIdx > latestColIdx:
                latestColIdx = colIdx
    
            if colIdx > 0 and colIdx < listLen:
                if col2cat[colIdx] != -1:
                    print(f'Collection #{colIdx} previously registered to another category! ({cats[col2cat[colIdx]]} => {cats[catIdx]})')

                col2cat[colIdx] = catIdx
            else:
                print(f'Collection index out of bound: {colIdx}')

'''
for ci in range(1, latestColIdx + 1):
    catIdx = col2cat[ci]

    catName = ''

    if catIdx != -1:
        catName = cats[catIdx]
    else:
        print(f'Category for collection #{str(ci)} is unknown')
'''

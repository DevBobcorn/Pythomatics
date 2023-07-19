import requests, base64, bs4, os, json, time, random, sys, shutil, datetime
from bs4 import BeautifulSoup

# Ignore ssl hostname matching check (uncomment to enable if necessary)
#import ssl
#ssl.match_hostname = lambda cert, hostname: True

# First get the full URL
domain = f"xi{base64.b64decode('VXJl').decode('utf-8')}nb."
root = fr"https://www.{domain}vip"
picroot = fr"https://p.{domain}top"

proxies = {
    #'http': r'http://localhost:19180',
    #'https': r'http://localhost:19180'
}

curColPath = '' # Current collection page path
lnx = { }

# Current image count
imgcnt = 0

# Image count until last page
lastimgcnt = 0

dlroot = 'web/'
os.chdir('../')
ci = 13001

dlPath = f'{dlroot}downloaded'

def dumpCurrentInfo(colIndex):
    # Dump current info
    jsonObj = json.dumps({
        'current_index': curColPath,
        'links': lnx,
        'image_count_till_last_page': lastimgcnt
    }, indent=4, separators=(',', ': '))

    logPath = f'{dlPath}/{getChunkFolder(colIndex)}/{colIndex}/download_info.json'

    with open(logPath, 'w+') as f:
        f.write(jsonObj)

def getCoverImage(colIndex):
    print(f'Grabbing cover for collection #{colIndex}...')

    resp = requests.get(f"{root}/UploadFile/pic/{colIndex}.jpg", stream=True, proxies=proxies)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200: # Ready
        with open(fr'{dlPath}/covers/{colIndex}.jpg', 'wb') as f:
            f.write(resp.content)
    else:
        raise Exception(f"Failed to grab cover for collection #{colIndex}. Error Code: {resp.status_code}")

def getMetaInfo(colIndex, colPath):
    print(f'Grabbing meta info for collection #{colIndex}... ({root}{colPath}.html)')

    resp = requests.get(f'{root}{colPath}.html', proxies=proxies)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200: # Ready
        ful = BeautifulSoup(resp.text, features="html.parser")
        bod = ful.body

        item1 = bod.find(name='div',attrs={'class':'item_title'})
        item2 = bod.find(name='div',attrs={'class':'item_info'})

        with open(fr'{dlPath}/metaInfo/{colIndex}.txt', 'w+', encoding='utf-8') as f:
            f.write(f'{item1}\n{item2}')
    else:
        raise Exception(f"Failed to grab meta info for collection #{colIndex}. Error Code: {resp.status_code}")

def getChunkFolder(colIndex):
    chunkIdx = int(((colIndex - 1) - ((colIndex - 1) % 400)) / 400) + 1
    return str(chunkIdx).zfill(3)

def markImage(mark, image):
    marksObj = { }

    if os.path.exists(fr'{dlPath}/marks.json'):
        with open(fr'{dlPath}/marks.json', 'r+', encoding='utf-8') as f:
            marksObj = json.loads(f.read())
    
    if mark not in marksObj.keys():
        marksObj[mark] = [ ]
    
    marksObj[mark].append(image)
    
    with open(fr'{dlPath}/marks.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(marksObj, indent=4, separators=(',', ': ')))
        #print(marksObj)

def getImage(chunkFolder, colIndex, url):
    global curColPath, imgcnt

    resp = requests.get(url, stream=True, proxies=proxies)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200: # Ready
        with open(fr'{dlPath}/{chunkFolder}/{colIndex}/{imgcnt}.jpg', 'wb') as f:
            f.write(resp.content)
    elif resp.status_code == 404: # Not found, mark it and skip
        markImage('not_found', f'[{colIndex}:{imgcnt}]{url}')
        print(f'Image {url} is not available, skipped')
    else:
        raise Exception(f"Failed to grab image from {url}. Error Code: {resp.status_code}")

def getCollection(chunkFolder, colIndex, colPath):
    global lnx, imgcnt, curColPath
    curColPath = colPath  # Set current processing collection index
    lnx.clear()   # Reset links dictionary
    imgcnt = 0    # Reset image count
    lastimgcnt = 0
    
    if not os.path.exists(f"{dlPath}/{chunkFolder}/{colIndex}"): # Create the directory for storing images
        print(f'Collection {colPath} starts...')
        os.makedirs(f"{dlPath}/{chunkFolder}/{colIndex}")
        # First search the index page, and get links to the rest of current collection
        getPage(chunkFolder, colIndex, f"{colPath}.html")
    else: # Look for download_info.json if the folder presents
        if os.path.exists(f"{dlPath}/{chunkFolder}/{colIndex}/download_info.json"):
            with open(f'{dlPath}/{chunkFolder}/{colIndex}/download_info.json', 'r+') as f:
                print(f'Restoring download process for collection #{colIndex} ({colPath})...')
                infotxt = f.read()
                jsonObj = json.loads(infotxt)

                for lnk, vis in jsonObj['links'].items():
                    lnx[lnk] = vis # Restore this link
                
                lastimgcnt = imgcnt = int(jsonObj['image_count_till_last_page'])
                print(f'lastimgcnt restored to {lastimgcnt}')

            # Delete it
            #os.remove(f"{dlPath}/{chunkFolder}/{colIndex}/download_info.json")

            if f"{colPath}.html" in lnx.keys() and lnx[f"{colPath}.html"]:
                print("Landing page already collected, skip...")
            else:
                getPage(chunkFolder, colIndex, f"{colPath}.html")
                
        else:
            print(f'Collection #{colIndex} is present... skip')
            return
    
    for lnk, vis in lnx.items():
        if not vis:
            getPage(chunkFolder, colIndex, lnk)
    print(f"Collection complete: {len(lnx)} pages searched. {imgcnt} images found.\n")
    # Now that the collection is complete, delete the dump file
    if os.path.exists(f"{dlPath}/{chunkFolder}/{colIndex}/download_info.json"):
        os.remove(f"{dlPath}/{chunkFolder}/{colIndex}/download_info.json")

def getPage(chunkFolder, colIndex, path):
    global lnx, imgcnt, lastimgcnt

    # Update last image count
    lastimgcnt = imgcnt

    print(f'Gettin page {path}', end='')

    resp = requests.get(f'{root}{path}', proxies=proxies)
    resp.encoding = resp.apparent_encoding

    dumpCurrentInfo(ci)

    # Sleep for a short period of time so that we ain't gonna be blocked
    for i in range(random.randint(3, 7)):
        print('.', end='')
        sys.stdout.flush()
        time.sleep(0.1)

    print('') # New line

    if resp.status_code == 200:
        # Ready
        ful = BeautifulSoup(resp.text, features="html.parser")
        bod = ful.body.find(name='div',attrs={'class':'main'}).find(name='div',attrs={'class':'main_inner'}).find(name='div',attrs={'class':'main_left'})

        cont = None
        navc = None

        for el in bod.contents:
            if type(el) == bs4.element.Tag and 'class' in el.attrs:
                if el.attrs['class'] == ['content']:
                    # Try find image container
                    imgCont = el.find(name='p')
                    if imgCont != None and cont == None:
                        cont = imgCont
                    # Try find navigation button container
                    navCont = el.find(name='div', attrs={'class':'content_left'})
                    if navCont != None and navc == None:
                        navc = navCont.find(name='div', attrs={'class':'page'})

        if cont != None: # Image container is successfully found
            # Process Images...
            for img in cont.findAll(name='img'):
                # For each image element
                imgcnt += 1
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Grabbing [{curColPath}:{imgcnt}]", end='')
                # Sleep for a short period of time so that we ain't gonna be blocked
                for i in range(random.randint(3, 10)):
                    print('.', end='')
                    sys.stdout.flush()
                    time.sleep(0.1)

                stampStart = time.time()
                getImage(chunkFolder, colIndex, f"{root}{img.attrs['src']}")
                print(f'{(time.time() - stampStart) * 1000:.0f}ms') # Print download time and start new line

        # All images collected, mark as visited(or add into the dictionary if
        # it is not yet present)
        if path not in lnx or not lnx[path]: # Short-circuit logic here
            lnx[path] = True

        if navc != None: # Navigation bar container is successfully found
            # Process Navigation Links...
            for lnk in navc.findAll(name='a'):
                if 'href' in lnk.attrs.keys() and lnk.attrs['href'].lower() not in lnx:
                    lnx[lnk.attrs['href'].lower()] = False
                    #print('New link found: ' + lnk.attrs['href'])
        else:
            print("Main content cannot be found!")
    else:
        raise Exception(f"Error Code: {resp.status_code}")

# Content Crawler =================================================================================
cats = [
    'XiuRen',   'MFStar',   'MiStar',   'MyGirl',
    'IMiss',    'BoLoli',   'YouWu',    'Uxing',
    'MiiTao',   'FeiLin',   'WingS',    'Taste',
    'LeYuan',   'HuaYan',   'DKGirl',   'MintYe',
    'YouMi',    'Candy',    'MTMeng',   'Micat',
    'HuaYang',  'XingYan',  'XiaoYu'
]

col2cat  = [ ]
col2page = [ ]

listLen = 14000

latestCoverIdx = 0

for i in range(listLen):
    col2cat.append(-1)
    col2page.append('')

# Load all the category mappings
for catIdx in range(len(cats)):
    cat = cats[catIdx]

    leadingCatNameLower = f'{cat.lower()}'

    with open(f'{dlroot}cats/cat_dict_{cat.lower()}.json') as f:
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
                col2page[colIdx] = catDict[coverImgIdx]['pageIdx']
            else:
                print(f'Collection index out of bound: {colIdx}')

print(f'Total count: {latestCoverIdx}')

while ci <= latestCoverIdx:
    try:
        catIdx = col2cat[ci]

        if catIdx != -1:
            # Get this collection
            getCollection(getChunkFolder(ci), ci, f'/{cats[catIdx]}/{col2page[ci]}'.lower())
            
            # Get collection cover
            #if not os.path.exists(f"{dlPath}/covers/{ci}.jpg"):
            #    getCoverImage(ci)
            #    time.sleep(0.4 + random.random())

            # Get collection meta info
            #if not os.path.exists(f"{dlPath}/metaInfo/{ci}.txt"):
            #    getMetaInfo(ci, f'/{cats[catIdx]}/{col2page[ci]}')
            #    time.sleep(0.4 + random.random())
        else:
            print(f'Category for collection #{str(ci)} is unknown')
        
        ci += 1
            
    except Exception as e:
        print(f"Un4tun8ly, the download process is interrupted: {e}")
        dumpCurrentInfo(ci)
        print(f"Download info of this collection is dumped under the collection folder")
        #break
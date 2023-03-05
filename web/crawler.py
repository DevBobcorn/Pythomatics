import requests, base64, bs4, os, json, time, random
from bs4 import BeautifulSoup

# Ignore ssl hostname matching check (uncomment to enable if necessary)
#import ssl
#ssl.match_hostname = lambda cert, hostname: True

# First get the full URL
domain = f"xi{base64.b64decode('VXJl').decode('utf-8')}nb."
root = fr"https://www.{domain}vip"
picroot = fr"https://p.{domain}top"

proxies = {
    'http': r'http://localhost:19180',
    'https': r'http://localhost:19180'
}

curColPath = '' # Current collection page path
lnx = {}

# Current image count
imgcnt = 0

# Image count until last page
lastimgcnt = 0

dlPath = 'web/downloaded'

def getCoverImage(colIndex):
    print(f'Grabbing cover for collection #{colIndex}...')

    resp = requests.get(f"{root}/UploadFile/pic/{colIndex}.jpg", stream=True, proxies=proxies)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200: # Ready
        with open(fr'{dlPath}/covers/{colIndex}.jpg', 'wb') as f:
            f.write(resp.content)
    else:
        raise Exception(f"Failed to grab cover for collection #{colIndex}. Error Code: {resp.status_code}")

def getImage(colIndex, url):
    global curColPath, imgcnt

    resp = requests.get(url, stream=True, proxies=proxies)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200: # Ready
        with open(fr'{dlPath}/{colIndex}/{imgcnt}.jpg', 'wb') as f:
            f.write(resp.content)
    else:
        raise Exception(f"Failed to grab image from {url}. Error Code: {resp.status_code}")

def getCollection(colIndex, colPath):
    global lnx, imgcnt, curColPath
    curColPath = colPath  # Set current processing collection index
    lnx.clear()   # Reset links dictionary
    imgcnt = 0    # Reset image count
    lastimgcnt = 0

    print(f'Collection {colPath} starts...')
    
    if not os.path.exists(f"{dlPath}/{colIndex}"): # Create the directory for storing images
        os.makedirs(f"{dlPath}/{colIndex}")
        # First search the index page, and get links to the rest of current collection
        getPage(colIndex, f"{colPath}.html")
    else: # Look for download_info.json if the folder presents
        if os.path.exists(f"{dlPath}/{colIndex}/download_info.json"):
            with open(f'{dlPath}/{colIndex}/download_info.json', 'r+') as f:
                print(f'Restoring download process for collection #{colIndex} ({colPath})...')
                infotxt = f.read()
                jsonObj = json.loads(infotxt)

                for lnk, vis in jsonObj['links'].items():
                    lnx[lnk] = vis # Restore this link
                
                lastimgcnt = imgcnt = int(jsonObj['image_count_till_last_page'])
                print(f'lastimgcnt restored to {lastimgcnt}')

            # Delete it
            os.remove(f"{dlPath}/{colIndex}/download_info.json")

            if f"{colPath}.html" in lnx.keys() and lnx[f"{colPath}.html"]:
                print("Landing page already collected, skip...")
            else:
                getPage(colIndex, f"{colPath}.html")
                
        else:
            # First search the index page, and get links to the rest of current collection
            #getPage(colIndex, f"{colPath}.html")
            print("Collection is present... skipping...")
            return
    
    for lnk, vis in lnx.items():
        if not vis:
            getPage(colIndex, lnk)
    print(f"Collection complete: {len(lnx)} pages searched. {imgcnt} images found.\n")

def getPage(colIndex, path):
    global lnx, imgcnt, lastimgcnt

    # Update last image count
    lastimgcnt = imgcnt;

    print(f'Gettin page {root} => {path}')

    resp = requests.get(f'{root}{path}', proxies=proxies)
    resp.encoding = resp.apparent_encoding

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
            print(f"Images found on {path}:")
            # Process Images...
            for img in cont.findAll(name='img'):
                # For each image element
                imgcnt += 1
                print(f"Grabbing [{curColPath}:{imgcnt}] {img.attrs['src']}", end='')
                # Sleep for a short period of time so that we ain't gonna be blocked
                time.sleep(0.2 + random.random())
                print('...')
                getImage(colIndex, f"{root}{img.attrs['src']}")
            
            # Sleep for a short period of time so that we ain't gonna be blocked
            time.sleep(0.5 + random.random())

        # All images collected, mark as visited(or add into the dictionary if
        # it is not yet present)
        if path not in lnx or not lnx[path]: # Short-circuit logic here
            lnx[path] = True

        if navc != None: # Navigation bar container is successfully found
            # Process Navigation Links...
            for lnk in navc.findAll(name='a'):
                if 'href' in lnk.attrs.keys() and lnk.attrs['href'] not in lnx:
                    lnx[lnk.attrs['href']] = False
                    print('New link found: ' + lnk.attrs['href'])
        else:
            print("Main content cannot be found!")
    else:
        raise Exception(f"Error Code: {resp.status_code}")

os.chdir('../')

# Cover Crwaler ===================================================================================
'''
idx = 1

while idx < 20001:
    try:
        getCoverImage(idx)
        time.sleep(0.4 + random.random())
        idx += 1
    except Exception as e:
        print(f'Exception occurred while getting cover for #{idx}: {e} Retrying...')
'''


# Content Crawler =================================================================================
cats = [
    'XiuRen',   'MFStar',   'MiStar',   'MyGirl',
    'Imiss',    'BoLoli',   'YouWu',    'Uxing',
    'MiiTao',   'FeiLin',   'WingS',    'Taste',
    'LeYuan',   'HuaYan',   'DKGirl',   'MintYe',
    'YouMi',    'Candy',    'MTMeng',   'Micat',
    'HuaYang',  'XingYan',  'XiaoYu'
]

col2cat  = [ ]
col2page = [ ]

listLen = 13000

latestCoverIdx = 0

for i in range(listLen):
    col2cat.append(-1)
    col2page.append('')

# Load all the category mappings
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
                col2page[colIdx] = catDict[coverImgIdx]['pageIdx']
            else:
                print(f'Collection index out of bound: {colIdx}')

ci = 2001

while ci < 20001:
    try:
        catIdx = col2cat[ci]

        if catIdx != -1:
            # Get this collection
            getCollection(ci, f'/{cats[catIdx]}/{col2page[ci]}')

            # Clone the cover file
            #shutil.copyfile(f'web/downloaded/covers/{ci}.jpg', f'web/downloaded/selected/{ci}.jpg')
        else:
            print(f'Category for collection #{str(ci)} is unknown')
        
        ci += 1
            
    except Exception as e:
        print(f"Un4tun8ly, the download process is interrupted: {e}")

        # Dump current info
        jsonObj = json.dumps({
            'current_index': curColPath,
            'links': lnx,
            'image_count_till_last_page': lastimgcnt
        })
        with open(f'{dlPath}/{ci}/download_info.json', 'w+') as f:
            f.write(jsonObj)
        
        print(f"Download info of this collection can be found here: {dlPath}/{ci}/download_info.json")
        #break

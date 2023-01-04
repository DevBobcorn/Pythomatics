import requests, base64, bs4, os, json, time, random
from bs4 import BeautifulSoup

# Ignore ssl hostname matching check (uncomment to enable if necessary)
#import ssl
#ssl.match_hostname = lambda cert, hostname: True

# First get the full URL
domain = f"xi{base64.b64decode('VXJl').decode('utf-8')}nb."
folder = base64.b64decode("L1hpdVJlbi8=").decode("utf-8")
root = fr"https://www.{domain}vip"
picroot = fr"https://p.{domain}top"

proxies = {
    'http': r'http://localhost:19180',
    'https': r'http://localhost:19180'
}

curidx = 0
lnx = {}

# Current image count
imgcnt = 0

# Image count until last page
lastimgcnt = 0

dlPath = 'web/downloaded'

def getCoverImage(idx):
    print(f'Grabbing cover for collection #{idx}...')

    resp = requests.get(f"{root}/UploadFile/pic/{idx}.jpg", stream=True, proxies=proxies)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200: # Ready
        with open(fr'{dlPath}/covers/{idx}.jpg', 'wb') as f:
            f.write(resp.content)
    else:
        raise Exception(f"Failed to grab cover for collection #{idx}. Error Code: {resp.status_code}")

def getImage(url):
    global curidx, imgcnt

    resp = requests.get(url, stream=True, proxies=proxies)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200: # Ready
        with open(fr'{dlPath}/{curidx}/{imgcnt}.jpg', 'wb') as f:
            f.write(resp.content)
    else:
        raise Exception(f"Failed to grab image from {url}. Error Code: {resp.status_code}")

def getCollection(idx):
    global lnx, imgcnt, curidx
    curidx = idx  # Set current processing collection index
    lnx.clear()   # Reset links dictionary
    imgcnt = 0    # Reset image count
    lastimgcnt = 0

    print(f'Collection #{idx} starts...')

    # Grab the collection cover
    if not os.path.exists(f"{dlPath}/covers"): # Create the directory for storing cover images
        os.makedirs(f"{dlPath}/covers")
    
    if not os.path.exists(f"{dlPath}/{idx}"): # Create the directory for storing images
        os.makedirs(f"{dlPath}/{idx}")
        # First search the index page, and get links to the rest of current collection
        getPage(f"{folder}{idx}.html")
    else: # Look for download_info.json if the folder presents
        if os.path.exists(f"{dlPath}/{idx}/download_info.json"):
            with open(f'{dlPath}/{idx}/download_info.json', 'r+') as f:
                print(f'Restoring download process for collection #{idx}.')
                infotxt = f.read()
                jsonObj = json.loads(infotxt)

                for lnk, vis in jsonObj['links'].items():
                    lnx[lnk] = vis # Restore this link
                
                lastimgcnt = imgcnt = int(jsonObj['image_count_till_last_page'])
                print(f'lastimgcnt restored to {lastimgcnt}')

            if f"{folder}{idx}.html" in lnx.keys() and lnx[f"{folder}{idx}.html"]:
                print("Landing page already collected, skip...")
            else:
                getPage(f"{folder}{idx}.html")
                
        else:
            # First search the index page, and get links to the rest of current collection
            getPage(f"{folder}{idx}.html")
    
    for lnk, vis in lnx.items():
        if not vis:
            getPage(lnk)
    print(f"Collection complete: {len(lnx)} pages searched. {imgcnt} images found.\n")

def getPage(path):
    global lnx, imgcnt, lastimgcnt

    # Update last image count
    lastimgcnt = imgcnt;

    resp = requests.get(f"{root}{path}", proxies=proxies)
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
                print(f"Grabbing [{curidx}:{imgcnt}] {img.attrs['src']}", end='')
                # Sleep for a short period of time so that we ain't gonna be blocked
                time.sleep(0.2 + random.random())
                print('...')
                getImage(f"{root}{img.attrs['src']}")
            
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


idx = 1938

while idx < 10001:
    try:
        getCoverImage(idx)
        time.sleep(0.4 + random.random())
        idx += 1
    except Exception as e:
        print(f'Exception occurred while getting cover for #{idx}: {e} Retrying...')

'''
with open(r'web\list.txt') as f:
    lnz = f.readlines()
    collecount = 0

    commented = False

    for ln in lnz:
        ln = ln.strip()

        if (ln.upper().startswith('#E')): # Comment section end
            commented = False
            continue
        elif ln.upper().startswith('#S'): # Comment section start
            commented = True
            continue

        if commented or ln == '' or ln.startswith('#'):
            continue
        
        collecount = collecount + 1
        idxs = ln.strip().split(' ', 2)
        idx = idxs[1].replace('+','').replace('*','')

        try:
            getCollection(idx)
        except Exception as e:
            print(f"Un4tun8ly, the download process is interrupted: {e}")

            # Dump current info
            jsonObj = json.dumps({
                'current_index': curidx,
                'links': lnx,
                'image_count_till_last_page': lastimgcnt
            })
            with open(f'{dlPath}/{idx}/download_info.json', 'w+') as f:
                f.write(jsonObj)
            
            print(f"Download info of this collection can be found here: downloaded/{curidx}/download_info.json")
            break
'''
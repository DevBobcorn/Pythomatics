import requests, base64, bs4, os
from bs4 import BeautifulSoup

# First get the full URL
domain = "xi" + base64.b64decode("VXJl").decode("utf-8") + "n" + chr(106) + "i.v"
folder = base64.b64decode("L1hpdVJlbi8=").decode("utf-8")
root = "https://www." + domain + "ip"

curidx = 0
lnx = {}
imgcnt = 0

def getImage(url):
    global curidx, imgcnt
    resp = requests.get(url, stream=True)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200:
        # Ready
        imgcnt = imgcnt + 1
        with open(r'downloaded/' + str(curidx) + '/' + str(imgcnt) + '.jpg', 'wb') as f:
            f.write(resp.content)
    else:
        print("Failed to download image from " + url)

def getCollection(idx):
    global lnx, imgcnt, curidx
    curidx = idx  # Set current processing collection index
    lnx.clear()   # Reset links dictionary
    imgcnt = 0    # Reset image count
    # Create the directory for storing images
    if not os.path.exists("downloaded/" + str(idx)):
        os.makedirs("downloaded/" + str(idx))
    print('Collection ' + idx + ' starts...')
    # First search the index page, and get links to the rest of current collection
    getPage(folder + str(idx) + ".html")
    for lnk, vis in lnx.items():
        if not vis:
            getPage(lnk)
    print("Collection complete: " + str(len(lnx)) + " pages searched, " + str(imgcnt) + " images found.")

def getPage(path):
    global lnx
    if path not in lnx or not lnx[path]: # Short-circuit logic here
        lnx[path] = True
    
    resp = requests.get(root + path)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200:
        # Ready
        ful = BeautifulSoup(resp.text, features="html.parser")
        bod = ful.body

        cont = None

        for el in bod.contents:
            if type(el) == bs4.element.Tag and 'class' in el.attrs:
                if el.attrs['class'] == ['nr3']:
                    cont = el

        if cont != None:
            # Process Images...
            for iel in cont.findAll(name='div',attrs={'class':'img'}):
                # For each image container
                print("Images found on " + path + ":")
                for img in iel.findAll(name='img'):
                    print(img.attrs['src'])
                    getImage(root + img.attrs['src'])
            # Process Navigation Links...
            for tel in cont.findAll(name='div',attrs={'class':'page'}):
                for lnk in tel.contents:
                    if lnk.attrs['href'] not in lnx:
                        lnx[lnk.attrs['href']] = False
                        print('New link found: ' + lnk.attrs['href'])
        else:
            print("Main content cannot be found!")
    else:
        print("Error Code: " + str(resp.status_code))

with open(r'list.txt') as f:
    lnz = f.readlines()
    cnt = 0
    for ln in lnz:
        cnt = cnt + 1
        idxs = ln.strip().split(' ', 2)
        idx = idxs[1].replace('+','').replace('*','')
        getCollection(idx)
        if cnt >= 5:
            break

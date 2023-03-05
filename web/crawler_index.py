import requests, base64, json, time, random
from bs4 import BeautifulSoup
from json import JSONEncoder

# First get the full URL
domain = f"xi{base64.b64decode('VXJl').decode('utf-8')}nb."
root = fr"https://www.{domain}vip"

proxies = {
    'http': r'http://localhost:19180',
    'https': r'http://localhost:19180'
}

updatingFromExistingData = True

class CollectionInfo:
  def __init__(self, pageIdx, desc):
    self.pageIdx = pageIdx
    self.desc = desc

class CollectionInfoEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

catDictionary = { }

catNames = [
    'XiuRen',   'MFStar',   'MiStar',   'MyGirl',
    'Imiss',    'BoLoli',   'YouWu',    'Uxing',
    'MiiTao',   'FeiLin',   'WingS',    'Taste',
    'LeYuan',   'HuaYan',   'DKGirl',   'MintYe',
    'YouMi',    'Candy',    'MTMeng',   'Micat',
    'HuaYang',  'XingYan',  'XiaoYu'
]

catName = 'ABCD'
catNameLen = 0

# Returns True if reached the end
def getIndexPage(index):
    global catName, catNameLen

    print(f'Getting index page #{index}...')

    url = f'{root}/{catName}/'

    if index > 1:
        url += f'index{index}.html'

    resp = requests.get(url, proxies=proxies)
    resp.encoding = resp.apparent_encoding

    if resp.status_code == 200:
        # Ready
        ful = BeautifulSoup(resp.text, features="html.parser")
        items = ful.find_all('li', class_='list_n2')

        updateComplete = False

        for item in items:
            link = item.find('a')
            pageIdx = link.get('href')[catNameLen + 2:-5]

            coverImgIdx = item.find('img').get('src').split('/')[-1][:-4]

            if updatingFromExistingData and coverImgIdx in catDictionary.keys():
                updateComplete = True
            else:
                catDictionary[coverImgIdx] = CollectionInfo(str(pageIdx), link.get('title'))
                print(f'New entry updated for {catName}: [{coverImgIdx}] {pageIdx}')
        
        if updateComplete:
            return True
        
        if (len(items) < 1):
            return True

    return False

for nm in catNames:
    print(f'Updating cat: {nm}...')
    catName = nm
    catNameLen = len(nm)
    catDictionary.clear()

    if updatingFromExistingData:
        with open(f'web/cats/cat_dict_{catName.lower()}.json', 'r+') as f:
            jsonText = f.read()
            jsonObj = json.loads(jsonText)

            for coverImgIdx in jsonObj:
                info = jsonObj[coverImgIdx]
                catDictionary[coverImgIdx] = CollectionInfo(info['pageIdx'], info['desc'])

    
    for idx in range(1, 1000):
        try:
            if getIndexPage(idx):
                break

            time.sleep(0.4 + random.random())
            idx += 1
        except Exception as e:
            print(f'Exception occurred while getting index page #{idx}: {e}')
            break
    

    with open(f'web/cats_updated/cat_dict_{catName.lower()}.json', 'w+') as f:
        jsonObj = json.dumps(catDictionary, indent=4, separators=(',', ': '), cls=CollectionInfoEncoder)

        f.write(jsonObj)

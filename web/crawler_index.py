import requests, base64, bs4, os, json, time, random
from bs4 import BeautifulSoup

# First get the full URL
domain = f"xi{base64.b64decode('VXJl').decode('utf-8')}nb."
root = fr"https://www.{domain}vip"

proxies = {
    'http': r'http://localhost:19180',
    'https': r'http://localhost:19180'
}

catDictionary = { }

catNames = [ ]

catName = 'ABCD'
catNameLen = 0

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

        for item in items:
            link = item.find('a')
            num = link.get('href')[catNameLen + 2:-5]
            #print(f"{num} {link.get('title')}")

            catDictionary[str(num)] = link.get('title')
        
        if (len(items) < 1):
            raise Exception(f"Index page is empty!")

for nm in catNames:
    print(f'Current cat: {nm}')
    catName = nm
    catNameLen = len(nm)
    catDictionary.clear()

    for idx in range(1, 300):
        try:
            getIndexPage(idx)
            time.sleep(0.4 + random.random())
            idx += 1
        except Exception as e:
            print(f'Exception occurred while getting index page #{idx}: {e}')
            break

    with open(f'web/cats/cat_dict_{catName.lower()}.json', 'w+') as f:
        jsonObj = json.dumps(catDictionary, indent=4)

        f.write(jsonObj)

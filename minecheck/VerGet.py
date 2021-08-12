from urllib.request import urlopen
import json,time,datetime

def getTime(timestr):
    return time.strftime("%b/%d/%Y,%H:%M:%S(%a)", time.strptime(timestr[0:-7],'%Y-%m-%dT%H:%M:%S'))

json_url = 'http://launchermeta.mojang.com/mc/game/version_manifest.json'
 
response = urlopen(json_url)

#req is a string
req = response.read()

'''
with open('version_manifest.json','wb') as f:
    f.write(req)
'''

versions = json.loads(req)
print('Welcome to the Minecraft Version Checker!\nThis week is %s%s%s\n' %(datetime.datetime.now().isocalendar()[0]-2000,'w',datetime.datetime.now().isocalendar()[1]))
print('Latest Release:  ',versions['latest']['release'])
print('Latest Snapshot: ',versions['latest']['snapshot'],'\n\nRecent Versions:')

print('%-21s%-14s%-30s' %('Version Id:','Type:','Release Time(GMT):'))

i = 0
for ver in versions['versions']:
    print('%-21s%-14s%-30s' %(ver['id'],ver['type'],getTime(ver['releaseTime'])))
    i += 1
    if i == 10:
        break
print('\n')

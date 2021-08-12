# LUOGU P1003 铺地毯
# Simplest Solution

tot = int(input())

mapSize = 150
map = []

def get(x, y):
    if (x >= 0 and y >=0 and x < mapSize and y < mapSize):
        return map[x][y]
    else:
        return -1

for x in range(0, mapSize):
    map.append([])
    for y in range(0, mapSize):
        map[x].append(-1);

for mat in range(0, tot):
    a = input().split()
    i, j, w, h = int(a[0]), int(a[1]), int(a[2]), int(a[3])
    for x in range(0, w):
        for y in range(0, h):
            map[i + x][j + y] = mat + 1 # Index Number: mat + 1

pos = input().split()
print(get(int(pos[0]), int(pos[1])))

'''
def printMap(sizex, sizey):
    for x in range(0, sizex):
        for y in range(0, sizey):
            print("%d" % map[x][y], end='')
        print('')

printMap(8, 8)
'''
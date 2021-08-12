# LUOGU P1003 铺地毯
# Smart Solution

tot = int(input())

mats = []

# first get all these carpets
for mat in range(0, tot):
    a = input().split()
    i, j, w, h = int(a[0]), int(a[1]), int(a[2]), int(a[3])
    mats.append((i, j, i + w, j + h))

pos = input().split()
posx = int(pos[0])
posy = int(pos[1])

found = False

# then iterate inversely
for mat in range(tot - 1, -1, -1):
    if (posx >= mats[mat][0] and posx <= mats[mat][2] and posy >= mats[mat][1] and posy <= mats[mat][3]):
        print(mat + 1)  # Index Number: mat + 1
        found = True
        break

if not found:
    print(-1)

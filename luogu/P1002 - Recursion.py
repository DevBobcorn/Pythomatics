# LUOGU P1002 过河卒
# Recursion Version
s = input().split()

map = []
sol = []

bx = int(s[0])
by = int(s[1])
hx = int(s[2])
hy = int(s[3])

def check(x, y):
    return x >= 0 and y >= 0 and x <= bx and y <= by

def dot(x, y):
    if check(x, y):
        map[x][y] = 1

for x in range(0, bx + 1): # 0 -> bx
    map.append([])
    sol.append([])
    for y in range(0, by + 1): # 0 -> by
        map[x].append(0)
        sol[x].append(0)

dot(hx, hy)
dot(hx + 2, hy + 1)
dot(hx + 1, hy + 2)
dot(hx + 2, hy - 1)
dot(hx + 1, hy - 2)
dot(hx - 2, hy + 1)
dot(hx - 1, hy + 2)
dot(hx - 2, hy - 1)
dot(hx - 1, hy - 2)

sol[0][0] = 0

for x in range(0, bx + 1):
    for y in range(0, by + 1):
        if map[x][y] != 1:
            if x == 0 and y == 0:
                sol[x][y] = 1;
            elif x == 0 and y > 0:
                sol[x][y] = sol[x][y - 1]
            elif x > 0 and y == 0:
                sol[x][y] = sol[x - 1][y]
            else:
                sol[x][y] = sol[x - 1][y] + sol[x][y - 1]

print(sol[bx][by])
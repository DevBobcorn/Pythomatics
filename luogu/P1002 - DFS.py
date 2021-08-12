# LUOGU P1002 过河卒
# DFS Version
s = input().split()

map = []

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
    for y in range(0, by + 1): # 0 -> by
        map[x].append(0)

dot(hx, hy)
dot(hx + 2, hy + 1)
dot(hx + 1, hy + 2)
dot(hx + 2, hy - 1)
dot(hx + 1, hy - 2)
dot(hx - 2, hy + 1);
dot(hx - 1, hy + 2)
dot(hx - 2, hy - 1)
dot(hx - 1, hy - 2)

cnt = 0

def dfs(x, y):
    global cnt
    if map[x][y] == 1:
        return
    if x == bx and y == by: # Gotcha
        cnt = cnt + 1
        return
    if x < bx:
        dfs(x + 1, y)
    if y < by:
        dfs(x, y + 1)

dfs(0, 0)
print(cnt)
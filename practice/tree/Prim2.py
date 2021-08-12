# Tree - Prim Algorithm

graph = []
visited = []
result = []
visnum = 0

pts = int(input())
rds = int(input())

for idx in range(0, pts + 1):
    visited.append(False)

# Input the graph
for idx in range(0, rds):
    info = input().split()
    a, b, l = int(info[0]), int(info[1]), int(info[2])
    graph.append((a, b, l))
    graph.append((b, a, l))

# Prim
sel = graph[0] # TODO
# 1. Select a point randomly
visited[0] = True
visnum = 1

# 2. Repeat the process
while visnum < pts:
    min = 999999999
    for rd in graph:
        if (visited[rd[0]] and not visited[rd[1]] and rd[2] < min):
            min = rd[2]
            sel = rd
    visited[sel[1]] = True
    visnum += 1
    result.append(sel)

# 3. Output the result
print(result)


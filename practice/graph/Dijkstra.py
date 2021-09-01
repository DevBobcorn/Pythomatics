# Graph - Dijkstra Algorithm

INF = 999999999

graph = []
dis = []
proc = [] # Processed points, or to say, points whose minimum distance has been determined

def printDis():
    print(dis[1:]) # Skip dis[0]

pts = int(input())
rds = int(input())

for pt in range(0, pts + 1):
    dis.append(INF) # We'll use dis[0] as a placeholder, as the distance index starts from 1

# Input the graph
for idx in range(0, rds):
    info = input().split()
    a, b, l = int(info[0]), int(info[1]), int(info[2])
    graph.append([a, b, l])

# Input the source point
src = int(input())
dis[src] = 0
proc.append(src)

# Dijkstra
# 1. Process points adjacent to the source point
for idx in range(0, rds):
    if (graph[idx][0] == src and graph[idx][2] < dis[graph[idx][1]]):
        dis[graph[idx][1]] = graph[idx][2]

def procPt(pt):
    # Find all adjacent points this point could be leading to
    for idx in range(0, rds):
        if (graph[idx][0] == pt and dis[pt] + graph[idx][2] < dis[graph[idx][1]]):
            #print("Trying shortening path through " + str(pt) + " -> " + str(graph[idx][1]))
            dis[graph[idx][1]] = dis[pt] + graph[idx][2]
    proc.append(pt)
    #printDis()

# 2. Repeat the work
while len(proc) < pts:
    min = INF + 1 # Trick, making those 'Infinite Length Edges' actually selectable
    sel = 0 # Not a point
    for pt in range(1, pts + 1):
        if pt not in proc and dis[pt] < min: # This point not processed yet
            min = dis[pt]
            sel = pt
    procPt(sel)

printDis()

'''
Test Data
6
8
1 6 100
2 3 5
1 3 10
3 4 50
5 4 20
1 5 30
5 6 60
4 6 10
1
'''
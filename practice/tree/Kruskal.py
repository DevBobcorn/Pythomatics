# Tree - Kruskal Algorithm

graph = []
trees = [] # [[point, parent, tree],...]
visited = [] # Whether an edge is visited or not

visEdge = 0

pts = int(input())
rds = int(input())

def mergeTree(point1, point2):  # Parent of its own
    mergeResult = getTree(point2)
    
    if (trees[point1][1] == -1):
        trees[point1][1] = mergeResult
        trees[point1][2] = mergeResult
    else:
        mergeTree(trees[point1][1], mergeResult) # First merge its parent

def getTree(point):
    if (trees[point][1] == -1): # Parent of its own
        return trees[point][2]
    else:
        parentTree = getTree(trees[point][1]) # Ask its parent
        # trees[point][2] = parentTree        # Update its tree (Not necessary since we ask its parent every time)
        return trees[point][2]

trees.append([0, -1, 0]) # First append a placer holder, for our point index starts at 1
for idx in range(1, pts + 1):
    trees.append([idx, -1, idx]) # No parent, every point's a tree

# Input the graph
for idx in range(0, rds):
    info = input().split()
    a, b, l = int(info[0]), int(info[1]), int(info[2])
    graph.append([a, b, l])
    visited.append(False)

# Kruskal
# 1. Sort all edges by their length, short to long
graph.sort(key = lambda rd:rd[2], reverse = False)
# The 'visited' list doesn't need to be resorted, since they're all set to False now

# 2. Repeat the process
while visEdge < pts - 1:
    for rd in range(0, rds):
        if (not visited[rd]) and getTree(graph[rd][0]) != getTree(graph[rd][1]):
            visited[rd] = True                    # Visit(select) the Edge
            mergeTree(graph[rd][0], graph[rd][1]) # Merge 2 end points into one tree
            print(graph[rd])
            # print(trees)
            break
            
    visEdge += 1


'''
Test Data
7
10
3 1 7
1 2 5
1 7 2
3 5 8
5 6 5
6 7 6
2 7 3
2 4 9
4 6 4
5 7 4
'''

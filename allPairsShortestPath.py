import argparse
import os
import re
import sys
import time
import math
import cProfile

# Command line arguments
parser = argparse.ArgumentParser(description='Calculate the shortest path between all pairs of vertices in a graph')
parser.add_argument('--algorithm', default='a', \
                    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ellman-ford only or (f)loyd-warshall only')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('--profile', action='store_true')
parser.add_argument('filename', metavar='<filename>', help='Input file containing graph')

graphRE = re.compile("(\\d+)\\s(\\d+)")
edgeRE = re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices = []
edges = []

pr = cProfile.Profile()
pr.enable()

start = time.time()



def BellmanFord(G):
    pathPairs = []
    edges = []
    l = len(vertices)
    for i in range(l):
        for j in range(l):
            if math.isinf(float(G[1][i][j])) is not None:
                e = [(int(i), int(j)), float(G[1][i][j])]
                edges.append(e)
    for k in range(len(vertices)):
        dist = []
        for g in range(l):
            dist.append(float("inf"))
            if g == k:
                dist[g] = 0
        for i in range(l - 1):
            for j in range(len(edges)):
                if dist[edges[j][0][1]] > dist[edges[j][0][0]] + edges[j][1]:
                    dist[edges[j][0][1]] = dist[edges[j][0][0]] + edges[j][1]
    for i in range(len(edges)):
        if dist[edges[i][0][1]] > dist[edges[i][0][0]] + edges[i][1]:
            print("negative circle")
            return 0
    for x in range(len(G[0])):
        edge = ((k, x), dist[x])
        pathPairs.append(edge)
    print(pathPairs)
    return pathPairs



def FloydWarshall(G):
    """O(n^3)"""
    pathPairs = []
    d = []
    l = len(G[0])
    for i in range(l):
        temp = []
        for j in range(l):
            temp.append(float(edges[i][j]))
        d.append(temp)
        d[i][i] = 0
    for k in range(l):
        for i in range(l):
            for j in range(l):
                if d[i][j] > d[i][k] + d[k][j]:
                    d[i][j] = d[i][k] + d[k][j]
    #### CHECKING FOR NEGATIVE CYCLES####
    for i in range(l):
        if (d[i][i] < 0):
            print("negative circle")
            return 0

    for i in range(l):
        for j in range(l):
            edge = ((i, j), d[i][j])
            pathPairs.append(edge)
    print(pathPairs)
    return pathPairs


def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile = open(filename, 'r')
    line1 = inFile.readline()
    graphMatch = graphRE.match(line1)
    if not graphMatch:
        print(line1 + " not properly formatted")
        quit(1)
    vertices = list(range(int(graphMatch.group(1))))
    edges = []
    for i in range(len(vertices)):
        row = []
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch = edgeRE.match(line)
        if edgeMatch:
            source = edgeMatch.group(1)
            sink = edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print(
                    "Attempting to insert an edge between " + source + " and " + sink + " in a graph with " + vertices + " vertices")
                quit(1)
            weight = edgeMatch.group(3)
            edges[int(source) - 1][int(sink) - 1] = weight
    G = (vertices, edges)
    return (vertices, edges)


def matrixEquality(a, b):
    if len(a) == 0 or len(b) == 0 or len(a) != len(b): return False
    if (a[0]) != (b[0]): return False
    for i, row in enumerate(a):
        for j, value in enumerate(b):
            if a[i][j] != b[i][j]:
                return False
    return True


def main(filename, algorithm):
    G = readFile(filename)
    pathPairs = []
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    #if algorithm == 'b' or algorithm == 'B':
        #pathPairs = BellmanFord(G)
    #if algorithm == 'f' or algorithm == 'F':
        # TODO: Insert timing code here
        #pathPairs = FloydWarshall(G)
    if algorithm == 'a':
        print('running both')

        pathPairsBellman = BellmanFord(G)
        pathPairsFloyd = FloydWarshall(G)

        #pathPairs = pathPairsBellman
        print("--- %s seconds ---" % (time.time() - start))
    #if matrixEquality(pathPairsBellman, pathPairsFloyd):
        #print('Floyd-Warshall and Bellman-Ford did not produce the same result')
   # with open(os.path.splitext(filename)[0] + '_shortestPaths.txt', 'w') as f:
        #for row in pathPairs:
         #   for weight in row:
         #       f.write(str(weight) + ' ')
         #   f.write('\n')
#

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.filename, args.algorithm)


pr.print_stats(sort='time')
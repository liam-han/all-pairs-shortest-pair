import sys
import re
import time
import math

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

class edgeNode:
    u = 0
    v = 0
    w = 0.0
    def __init__(self,u,v,w):
        self.u = u
        self.v = v
        self.w = w

    def __repr__(self):
        return "((%s,%s),%s)"%(self.u,self.v,self.w)



def negCyclefloydWarshall(graph):

        # dist[][] will be the
        # output matrix that will
        # finally have the shortest
        # distances between every
        # pair of vertices
        dist = [[0 for i in range(len(vertices + 1))] for j in range(len(vertices + 1))]

        # Initialize the solution
        # matrix same as inputx
        # graph matrix. Or we can
        # say the initial values
        # of shortest distances
        # are based on shortest
        # paths considering no
        # intermediate vertex.
        for i in range(vertices):
            for j in range(vertices):
                dist[i][j] = graph[i][j]

        ''' Add all vertices one
            by one to the set of 
            intermediate vertices.
        ---> Before start of a iteration,
             we have shortest
            distances between all pairs
            of vertices such 
            that the shortest distances
            consider only the
            vertices in set {0, 1, 2, .. k-1}
            as intermediate vertices.
        ----> After the end of a iteration,
              vertex no. k is 
            added to the set of
            intermediate vertices and 
            the set becomes {0, 1, 2, .. k} '''
        for k in range(len(vertices)):

            # Pick all vertices
            # as source one by one
            for i in range(len(vertices)):

                # Pick all vertices as
                # destination for the
                # above picked source
                for j in range(len(vertices)):

                    # If vertex k is on
                    # the shortest path from
                    # i to j, then update
                    # the value of dist[i][j]
                    if (dist[i][k] + dist[k][j] < dist[i][j]):
                        dist[i][j] = dist[i][k] + dist[k][j]

        # If distance of any
        # vertex from itself
        # becomes negative, then
        # there is a negative
        # weight cycle.
        for i in range(len(vertices)):
            if (dist[i][i] < 0):
                return True

        return False

def BellmanFord(G):
    pathPairs=[]
    edgeList = []
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            if not math.isinf(float(G[1][i][j])):
                e = edgeNode(int(i), int(j), float(G[1][i][j]))
                edgeList.append(e)
    # Fill in your Bellman-Ford algorithm here
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    
    print (len(edgeList))
    print (len(vertices))
    for k in range(len(vertices)):
        dist = []
        for z in range(len(vertices)):
            dist.append(float("inf"))
            if z == k:
                dist[z] = 0
        for i in range(len(vertices)-1):
            for j in range(len(edgeList)):
                if dist[edgeList[j].v] > dist[edgeList[j].u] + edgeList[j].w:
                    dist[edgeList[j].v] = dist[edgeList[j].u] + edgeList[j].w
        for i in range(len(edgeList)):
            if dist[edgeList[i].v] > dist[edgeList[i].u] + edgeList[i].w:
                print ("There is negative circle")
                return 0
#break

        for i in range(len(G[0])):
            e = edgeNode(k,i,dist[i])
            pathPairs.append(e)

    return pathPairs

def FloydWarshall(G):
    pathPairs=[]
    # Fill in your Floyd-Warshall algorithm here
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    dist=[]
    for i in range(len(G[0])):
        new = []
        for j in range(len(G[0])):
            new.append(float(edges[i][j]))
        dist.append(new)
        dist[i][i] = 0
    for k in range(len(G[0])):
        for i in range(len(G[0])):
            for j in range(len(G[0])):
                if(dist[i][j] > dist[i][k]+dist[k][j]):
                    dist[i][j] = dist[i][k] + dist[k][j]

    for i in range(len(G[0])):
        for j in range(len(G[0])):
            e = edgeNode(i,j,dist[i][j]);
            pathPairs.append(e)
    #print dist
    return pathPairs



def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...

    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    #Debugging
    #for i in G:
        #print(i)
    return (vertices,edges)

def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)

    if algorithm == 'b' or algorithm == 'B':
        BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        FloydWarshall(G)
    if algorithm == "both":
        start=time.clock()
        print (BellmanFord(G))
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        #print (FloydWarshall(G))
        FloydWarshall(G)
        start=time.clock()
        end=time.clock()
        FWTime=end-start
        print("Bellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python bellman_ford.py -<f|b> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])

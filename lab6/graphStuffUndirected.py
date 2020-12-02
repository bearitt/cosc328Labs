import heapdict as heapdict # you will need to install the heapdict package to use this
import math
# Implementation of undirected graphs with weighted edges

class Vertex:
    def __init__(self, v):
        self.neighbors = [] # list of pairs (nbr, wt), where nbr is a Vertex and wt is a weight
        #self.outNeighbors = [] # same as above
        self.value = v
        # useful for DFS/BFS/Dijkstra/Bellman-Ford
        self.inTime = None
        self.outTime = None
        self.status = "unvisited"
        self.parent = None
        self.estD = math.inf
        
    def hasNeighbor(self,v):
        if v in self.getNeighbors():
            return True
        return False
        
    def getNeighbors(self):
        return [ v[0] for v in self.neighbors ]
    
    def getNeighborsWithWeights(self):
        return self.neighbors
    
    def addNeighbor(self,v,wt):
        self.neighbors.append((v,wt))
    
    def __str__(self):
        return str(self.value) 
        
# This is an undirected graph class.
class Graph:
    def __init__(self):
        self.vertices = []
        
    def addVertex(self,n):
        self.vertices.append(n)
        
    # add a directed edge from Node u to Node v
    def addEdge(self,u,v,wt=1):
        u.addNeighbor(v,wt=wt)
        v.addNeighbor(u,wt=wt)
    
    # get a list of all the edges
    def getEdges(self):
        ret = []
        for v in self.vertices:
            for u, wt in v.getNeighborsWithWeights():
                ret.append( [v,u,wt] )
        return ret
    
    def __str__(self):
        ret = "Graph with:\n"
        ret += "\t Vertices:\n\t"
        for v in self.vertices:
            ret += str(v) + ","
        ret += "\n"
        ret += "\t Edges:\n\t"
        for a,b,wt in self.getEdges():
            ret += "(" + str(a) + "," + str(b) + "; wt:" + str(wt) + ") "
        ret += "\n"
        return ret
    

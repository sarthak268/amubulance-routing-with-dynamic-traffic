from collections import defaultdict 
  
class Graph: 
  
    def __init__(self, vertices): 
        self.V = vertices
        self.graph = []
   
    def addEdge(self, u, v, w): 
        self.graph.append([u, v, w])

    def add_edge_weight(self, u, v, w):
        if ([u, v, 1] in self.graph):
            if ([u,v,1] in self.graph):
                ind = self.graph.index([u,v,1])
            else:
                ind = -1
            if(ind!=-1):
                self.graph[ind][2] = w
          
    def printArr(self, dist): 
        print("Vertex   Distance from Source") 
        for i in range(self.V): 
            print("% d \t\t % d" % (i, dist[i])) 
      
    def BellmanFord(self, src): 
  
        dist = [float("Inf")] * self.V
        dist[(int)(src)] = 0 
        print('src', src)
  
        for i in range(self.V - 1): 
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]: 
                        dist[v] = dist[u] + w 
  
        # for u, v, w in self.graph: 
        #         if dist[u] != float("Inf") and dist[u] + w < dist[v]: 
        #                 print "Graph contains negative weight cycle"
        #                 return
                          
        # self.printArr(dist)
        return dist
  
# g = Graph(5) 
# g.addEdge(0, 1, -1) 
# g.addEdge(0, 2, 4) 
# g.addEdge(1, 2, 3) 
# g.addEdge(1, 3, 2) 
# g.addEdge(1, 4, 2) 
# g.addEdge(3, 2, 5) 
# g.addEdge(3, 1, 1) 
# g.addEdge(4, 3, -3) 
  
# # Print the solution 
# g.BellmanFord(0)
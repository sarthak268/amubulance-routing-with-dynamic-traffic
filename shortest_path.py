from collections import defaultdict 
  
class Graph: 
  
    def __init__(self, vertices): 
        self.V = vertices
        self.graph = []
        self.parent_node = [-1] * self.V
   
    def addEdge(self, u, v, w): 
        self.graph.append([u, v, w])
          
    def printArr(self, dist): 
        print("Vertex   Distance from Source") 
        for i in range(self.V): 
            print("% d \t\t % d" % (i, dist[i])) 
      
    def BellmanFord(self, src): 
  
        dist = [float("Inf")] * self.V
        dist[(int)(src)] = 0
        self.parent_node[(int)(src)] = (int)(src)
        
        for i in range(self.V - 1): 
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]: 
                    dist[v] = dist[u] + w
                    self.parent_node[v] = u

        return dist, self.parent_node
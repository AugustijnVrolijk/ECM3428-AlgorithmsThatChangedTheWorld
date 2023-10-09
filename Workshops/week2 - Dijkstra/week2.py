from collections import defaultdict
import numpy as np

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)  # This is simmilar to the PageRank graph.
        self.edge_distances = dict()
        
    def addNode(self, name):
        self.nodes.add(name)
        
    def addEdge(self, start, end, distance):
        self.edges[start].add(end)
        self.edge_distances[(start, end)] = distance
    
    def printGraph(self):
        for s, e in self.edge_distances:
            print(f"{s} -> {e} : {self.edge_distances[(s,e)]}")

def dijkstra(graph:Graph, startNode):
    
    # Set all nodes as unvisited.
    unvisited_nodes = set(graph.nodes)
    candidate_distance = {}
    
    # Set all distances to infinity except for the start node which is 0.
    for node in unvisited_nodes:
        if node not in graph.edges[startNode]:
            candidate_distance[node] = np.inf
        else:
            candidate_distance[node] = graph.edge_distances[(startNode, node)]
    # Set the start node as the current node.
    currentNode = startNode
    candidate_distance[startNode] = 0
    
    print(candidate_distance)
    print("%f hello \n\n\n asdasd".format(unvisited_nodes))
    while unvisited_nodes:
        # Task: write your code below
        for node in graph.edges[currentNode]:
            newDistance = candidate_distance[currentNode] + graph.edge_distances[(currentNode, node)]
            if newDistance < candidate_distance[node]:
                candidate_distance[node] = newDistance
        # End task
        # Mark current node as visited and select the new current node. 
        if unvisited_nodes:
            current_node = min(candidate_distance.keys() & unvisited_nodes, key=candidate_distance.get)
        unvisited_nodes.remove(currentNode)        
        # print the distance and unvisited nodes
        print(candidate_distance)
        print(unvisited_nodes)
        print(current_node)

def main():
    myGraph = Graph()
    myGraph.addNode("A")
    myGraph.addNode("B")
    myGraph.addNode("C")
    myGraph.addNode("D")
    myGraph.addNode("E")
    myGraph.addEdge("A", "B", 1)
    myGraph.addEdge("A", "D", 3)
    myGraph.addEdge("B", "C", 2)
    myGraph.addEdge("B", "E", 6)
    myGraph.addEdge("C", "E", 4)
    myGraph.addEdge("D", "E", 1)
    print(myGraph.edges)
    myGraph.printGraph()
    dijkstra(myGraph, "A")
    return()

if __name__ == "__main__":
    main()
""" Title: <title of program/source code>
Author: <author(s) names>
Date: <date>
Code version: <code version>
Availability: <where it's located> """


import queue  
from collections import namedtuple

Edge = namedtuple('Edge', ['vertex', 'weight'])
class GraphUndirectedWeighted(object):  
    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.adjacency_list = [[] for _ in range(vertex_count)]

    def add_edge(self, source, dest, weight):
        assert source < self.vertex_count
        assert dest < self.vertex_count
        self.adjacency_list[source].append(Edge(dest, weight))
        self.adjacency_list[dest].append(Edge(source, weight))

    def get_edge(self, vertex):
        for e in self.adjacency_list[vertex]:
            yield e

    def get_vertex(self):
        for v in range(self.vertex_count):
            yield v


class dijkstra_manager:

    def __init__(self, matrix):

        self.graph = build_graph(matrix)
        self.shortest_path_map = {}


    def dijkstra(self, source, dest):  
        if (source, dest) in self.shortest_path_map.keys():
            # print('time saved ')
            return self.shortest_path_map.get((source, dest))

        q = queue.PriorityQueue()
        parents = []
        distances = []
        start_weight = float("inf")

        for i in self.graph.get_vertex():
            weight = start_weight
            if source == i:
                weight = 0
            distances.append(weight)
            parents.append(None)

        q.put(([0, source]))

        while not q.empty():
            v_tuple = q.get()
            v = v_tuple[1]

            for e in self.graph.get_edge(v):
                candidate_distance = distances[v] + e.weight
                if distances[e.vertex] > candidate_distance:
                    distances[e.vertex] = candidate_distance
                    parents[e.vertex] = v
                    # primitive but effective negative cycle detection
                    if candidate_distance < -1000:
                        raise Exception("Negative cycle detected")
                    q.put(([distances[e.vertex], e.vertex]))

        shortest_path = []
        end = dest
        while end is not None:
            shortest_path.append(end)
            end = parents[end]

        shortest_path.reverse()

        self.shortest_path_map[(source, dest)] = [shortest_path, distances[dest]]

        return shortest_path, distances[dest]




def build_graph(matrix):  
    # Input matrix is the raw adjacency matrix
    # return the "graph" needed for dijkstra shortest path calculation
    size = len(matrix)
    g = GraphUndirectedWeighted(size)
    for i in range(size):
        for j in range(i+1, size):
            entry = matrix[i][j]
            if entry != 'x':
                g.add_edge(i, j, entry)

    return g

"""
    def build(self):  
        g = GraphUndirectedWeighted(9)
        g.add_edge(0, 1, 4)
        g.add_edge(1, 7, 6)
        g.add_edge(1, 2, 1)
        g.add_edge(2, 3, 3)
        g.add_edge(3, 7, 1)
        g.add_edge(3, 4, 2)
        g.add_edge(3, 5, 1)
        g.add_edge(4, 5, 1)
        g.add_edge(5, 6, 1)
        g.add_edge(6, 7, 2)
        g.add_edge(6, 8, 2)
        g.add_edge(7, 8, 2)
        # for testing negative cycles
        # g.add_edge(1, 9, -5)
        # g.add_edge(9, 7, -4)

        shortest_path, distance = self.dijkstra(g, 0, 1)
        assert shortest_path == [0, 1] and distance == 4
        print(shortest_path)

        for i in range(10000):
            shortest_path, distance = self.dijkstra(g, 0, 8)
            assert shortest_path == [0, 1, 2, 3, 7, 8] and distance == 11
        print(shortest_path)

        # shortest_path, distance = dijkstra(g, 5, 0)
        # assert shortest_path == [5, 3, 2, 1, 0] and distance == 9
        # print(shortest_path)

        # shortest_path, distance = dijkstra(g, 1, 1)
        # assert shortest_path == [1] and distance == 0
        # print(shortest_path)
"""

# if __name__ == "__main__": 
#     d_manager = dijkstra_manager()
#     d_manager.build()
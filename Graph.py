import networkx as nx
import matplotlib.pyplot as plt
# This is a modified version of
# https://gist.github.com/anirudhjayaraman/272e920079fd8cea97f81487ef1e78a3


# An undirected graph object.
class Graph:
    def __init__(self):
        # This is directional
        self.vertices = {}
        # This just makes it easier to visualize in python
        # This is undirectional
        self.visual = []

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex not in self.vertices:
            self.vertices[vertex.name] = vertex.neighbors
        else:
            return False

    def add_edge(self, vertex_parent, vertex_child):
        if isinstance(vertex_parent, Vertex) and isinstance(vertex_child, Vertex):
            vertex_parent.add_neighbor(vertex_child)
            self.vertices[vertex_parent.name] = vertex_parent.neighbors
            self.vertices[vertex_child.name] = vertex_child.neighbors
        temp = [vertex_parent.name, vertex_child.name]
        if temp not in self.visual:
            self.visual.append(temp)

    def visualize(self):
        graph = nx.Graph()
        graph.add_edges_from(self.visual)
        nx.draw_networkx(graph)
        plt.show()


# A Vertex class.
# Stores information about this vertex such as its neighbors.
# The name is essentially the key
class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def add_neighbor(self, neighbor):
        if isinstance(neighbor, Vertex):
            # Checking if it is already a neighbor
            if neighbor.name not in self.neighbors:
                self.neighbors.append(neighbor.name)
                neighbor.neighbors.append(self.name)
            else:
                return False

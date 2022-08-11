import networkx as nx
import matplotlib.pyplot as plt


# This is a modified version of
# https://gist.github.com/anirudhjayaraman/272e920079fd8cea97f81487ef1e78a3


# An undirected graph object.
class Graph:
    """
    Class for graph object.
    Uses the vertex class.
    Use to create an UNDIRECTED graph.
    For the purposes of this project, there is no point in having directed edges.
    """

    def __init__(self):
        """
        INIT: Initializes the vertices.
        """
        # This is directional
        self.vertices = []
        # This just makes it easier to visualize in python
        # This is un-directional
        self.visual = []

    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph.
        If false, then either: the vertex is already in the graph.
        Or, the vertex is not of type Vertex.
        TODO: ! isinstance should throw error, whilst already in graph should return False?
            See issue #8 https://github.com/20004427/SCRAN/issues/8

        :param vertex: (Vertex)
        :return: (BOOLEAN) True == success, False == Failed
        """
        if isinstance(vertex, Vertex) and vertex.name not in [i.name for i in self.vertices]:
            self.vertices.append(vertex)
            return True
        else:
            return False

    def add_edge(self, vertex_parent, vertex_child):
        """
        Adds an undirected edge too the graph.

        :param vertex_parent: (Vertex)
        :param vertex_child: (Vertex)
        :return: (NONE)
        """
        if isinstance(vertex_parent, Vertex) and isinstance(vertex_child, Vertex):
            vertex_parent.add_neighbor(vertex_child)
        temp = [vertex_parent.name, vertex_child.name]
        if temp not in self.visual:
            self.visual.append(temp)

    def visualize(self):
        """
        Draws the graph using pyplot

        :return: (NONE)
        """
        graph = nx.Graph()
        graph.add_edges_from(self.visual)
        nx.draw_networkx(graph)
        plt.show()

    def clean_up_graph(self):
        """
        This function will remove:
        - edges onto itself i.e. [cost, cost]
        - situations such as [raw, rawmaterial]

        :return:
        """
        # list of tuples to store a vertex to remove, and the
        # vertex's neighbor that edges need to now connect too.
        nodes_to_remove = []
        for vertex in self.vertices:
            for neighbor in vertex.neighbors:
                if vertex.name in neighbor.name:
                    nodes_to_remove.append([vertex.name, neighbor.name])

        for node_to_remove in nodes_to_remove:
            # Need to remove the edge from
            print(node_to_remove)


# A Vertex class.
# Stores information about this vertex such as its neighbors.
# The name is essentially the key
class Vertex:
    """
    Class for a vertex.
    This is more for directed graph - as it allows each vertex to
    keep track of its own neighbors.
    However, I though I might as well just leave it in.
    In this case, we could just use an array of tuples, i.e.
    [(node0, node1), (node0, node3), etc.]
    The visual variable stores the nodes in this way.
    """

    def __init__(self, name, vertex_id):
        """
        Initializes the name,
        Sets neighbors to empty array.

        :param name: (String)
        :param vertex_id: (int)
        """
        self.name = name
        self.neighbors = []
        self.vertex_id = vertex_id

    def add_neighbor(self, neighbor):
        """
        Adds a neighbor to the vertex.
        # TODO: issue 8, https://github.com/20004427/SCRAN/issues/8

        :param neighbor: (Vertex)
        :return: (BOOLEAN) False == neighbor already exists, True == Success
        """
        if isinstance(neighbor, Vertex):
            # Checking if it is already a neighbor
            if neighbor.name not in [i.name for i in self.neighbors]:
                self.neighbors.append(neighbor)
                return True
            else:
                return False

    def remove_neighbor(self, neighbor):
        """
        Function to remove a neighbor from this vertex.

        :param neighbor: (Vertex)
        :return: (Boolean) True: Success, False: passed vertex is not a neighbor of this vertex.
        """
        if isinstance(neighbor, Vertex):
            if neighbor.name not in self.neighbors:
                return False
            else:
                self.neighbors.remove(neighbor)
                return True

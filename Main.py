import APIs
import Config
import Graph

word_list = []
graph = Graph.Graph()

if Config.USE_TEST_DATA:
    word_list = ["Bamboozled", "Risk", "Shipping", "Packaging"]

for word in word_list:
    # Creating a node for each word
    word_node = Graph.Vertex(word)
    graph.add_vertex(word_node)
    definition = APIs.get_word_definition(word)
    print(definition)

for vertex in graph.vertices:
    print(vertex)

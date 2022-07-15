import APIs
import Config
import Graph
import HelperFunctions

word_list = []
graph = Graph.Graph()

if Config.USE_TEST_DATA:
    word_list = ["Bamboozled", "Risk", "Shipping", "Packaging"]
else:
    # TODO: have file in teams and use webhook?
    word_list = HelperFunctions.read_keywords(Config.PATH_TO_WORD_LIST, Config.WORD_LIST_SHEET_NAME)

for word in word_list:
    # Creating a node for each word
    word_node = Graph.Vertex(word)
    graph.add_vertex(word_node)
    definition = APIs.get_word_definition(word)
    print(definition)

for vertex in graph.vertices:
    print(vertex)

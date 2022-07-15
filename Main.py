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
    if Config.DEBUG:
        # Printing the first 10 rows of the df
        print("Word list:")
        print(word_list[:10])
# Looping through the words
for row_index, row in word_list.iterrows():
    # Creating a node for each word
    print(row[0])
    word_node = Graph.Vertex(row[0])
    graph.add_vertex(word_node)
    definition = APIs.get_word_definition(row[0])
    if Config.DEBUG:
        print(f"Original definition for {row[0]}: \n{definition}")

    # Running find and replace on the definition
    # For every word in the word list
    for inner_row_index, inner_row in word_list.iterrows():
        for word in inner_row[1:]:
            # looping through the words in the row until an empty cell is found
            if word == "nan" or type(word) == float:
                break
            if Config.DEBUG:
                print("Word: " + word)
            definition.replace(word, inner_row[0])
    if Config.DEBUG:
        print(f"New Definition for {row[0]}: \n{definition}")

for vertex in graph.vertices:
    print(vertex)

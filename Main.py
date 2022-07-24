import APIs
import Config
import Graph
import HelperFunctions
from pattern.text.en import lexeme

word_list = []
graph = Graph.Graph()
lexeme_dictionary = {}

if Config.USE_TEST_DATA:
    word_list = ["Bamboozled", "Risk", "Shipping", "Packaging"]
    # For each key word. Finding the Lexeme of each.
    # Lexeme is a unit of lexical meaning that underlies a set of words that are related through inflection
    # So if the key word was "ship" then the lexeme set would be ["shipping", "shipped"]
    for word in word_list:
        # Unfortunately, lexeme() will throw an error if no inflections exist for the word.
        try:
            lexeme_dictionary[word] = lexeme(word)
        except RuntimeError as e:
            lexeme_dictionary[word] = []
else:
    # TODO: have file in teams and use webhook?
    word_list = HelperFunctions.read_keywords(Config.PATH_TO_WORD_LIST, Config.WORD_LIST_SHEET_NAME)
    if Config.DEBUG:
        # Printing the first 10 rows of the df
        print("Word list:")
        print(word_list[:10])
    # For each key word. Finding the Lexeme of each.
    # Lexeme is a unit of lexical meaning that underlies a set of words that are related through inflection
    # So if the key word was "ship" then the lexeme set would be ["shipping", "shipped"]
    for row in word_list.iterrows():
        # row[0] is the row index, row[1] is the row data
        inflections = []
        words = row[1]
        word = words[0]
        for w in words:
            if w != "" and type(w) is not float:
                inflections.append(w)
        # trying to get the lexeme set for the word
        try:
            lexeme_set = lexeme(word)
        except RuntimeError as e:
            lexeme_set = []
        # Getting the union of the two lists.
        lexeme_dictionary[word] = list(set(lexeme_set) | set(inflections))


# Looping through the words
for key in lexeme_dictionary:
    # Creating a node for each word
    print(key)
    word_node = Graph.Vertex(key)
    graph.add_vertex(word_node)
    definition = APIs.get_word_definition(key)
    if Config.DEBUG:
        print(f"Original definition for {key}: \n{definition}")

    # Running find and replace on the definition
    # For every word in the word list
    # if the definition is found
    if definition != -1:
        for word in lexeme_dictionary:
            for inflection in lexeme_dictionary[word]:
                definition.replace(inflection, word)
        if Config.DEBUG:
            print(f"New Definition for {key}: \n{definition}")

for vertex in graph.vertices:
    print(vertex)

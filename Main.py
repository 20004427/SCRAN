import APIs
import Config
import HelperFunctions
import networkx as nx
import matplotlib.pyplot as pt
import numpy as np
from pattern.text.en import lexeme

word_list = []
graph = nx.Graph()
lexeme_dictionary = {}

if Config.USE_TEST_DATA:
    # Test data - data from the mid-year review
    word_list = ["Bullwhip", "Stockouts", "Warehousing", "Overstocking", "Panic Buying",
                 "Pallets", "Packing", "Supplier Reliability", "Raw Materials", "Containers",
                 "Shipping", "Singapore", "Air Freight", "Los Angeles", "Shanghai", "Auckland",
                 "Available Equipment & Parts", "Cost", "Available credit", "Cybersecurity",
                 "Labour", "Absenteeism", "Attrition", "Staff Burnout", "Salary wars", "Strikes"]
    word_list = ["Pallets", "Packing", "Supplier Reliability"]
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
        HelperFunctions.print_debug("Word list:")
        for i in word_list[:10]:
            HelperFunctions.print_debug(f"\t {i}")
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
    # Lowering so that we don't have duplicate nodes i.e. Tax and tax
    key = key.lower()
    # Creating a node for each word
    graph.add_node(key)
    # Scraping google, the first array item is the number of results
    scrape_output = APIs.scrape_google(key)
    scrape_results = scrape_output[1:]
    number_of_search_results = scrape_output[0]
    if number_of_search_results is not None:
        Config.words_to_graph.append(key)
        Config.values_to_graph.append(number_of_search_results)
    # Using the scrape results to find related keywords
    linking_keywords = HelperFunctions.extract_keywords_from_scrape(scrape_results, lexeme_dictionary, key)
    for word in linking_keywords:
        graph.add_node(word)
        graph.add_edge(key, word)
        if Config.GOOGLE_SCRAPE_DO_RECURSION:
            HelperFunctions.recursively_scrape_word(word, lexeme_dictionary, graph)
    if Config.DEBUG:
        HelperFunctions.print_debug(f"The keywords relating to {key} are {linking_keywords}")

HelperFunctions.cleanup_graph(graph)
# Output
pos = nx.spring_layout(graph)
nx.draw(graph, with_labels=True, pos=pos)
pt.savefig("output.png")
pt.show()
HelperFunctions.export_to_pajek(graph, [key.lower() for key in lexeme_dictionary])


Config.values_to_graph.sort()
if Config.DEBUG:
    HelperFunctions.print_debug(f"Values to graph: {Config.values_to_graph}")
# Normalizing the values
max_value = max(Config.values_to_graph)
min_value = min(Config.values_to_graph)
values_to_graph = [(i - min_value) / (max_value - min_value) for i in Config.values_to_graph]

# Graphing the number of search results
# Bar graph - for visualization purposes
pt.bar(Config.words_to_graph, values_to_graph, color='r', alpha=0.25)
# Numeric only exponential graph.
# Each word is given a number between 0 and len(words)
# Since the data is already sorted, the x value corresponds to the index in the
# words array, that is Config.values_to_graph
numeric_x = list(range(0, len(Config.words_to_graph)))
pt.plot(numeric_x, values_to_graph)
pt.show()

# now fitting the data to an exponential curve
# removing all zeros from the values to graph (preventing a divide by zero error)
# These values are replaced with the smallest none-zero value
smallest_none_zero = min(list(filter(lambda x: x > 0, values_to_graph)))
non_zero_values_y = np.array([i if i != 0 else smallest_none_zero for i in values_to_graph])
# Now fitting the data to a "smooth" exponential curve
fit = np.polyfit(np.array(numeric_x), np.log(non_zero_values_y), 1)
if Config.DEBUG:
    HelperFunctions.print_debug(fit)


def f(x_):
    """
    Function to map x to y.
    Uses an exponential fit.
    Form: a + b*e^x

    :param x_: (Numpy Array) an array of x values.
    :return: (Numpy Array) an array of y values.
    """
    return fit[1] + fit[0] * np.exp(x_)


x = np.linspace(0, len(Config.words_to_graph), 100)
y = f(x)
point_bottom_right = (len(Config.words_to_graph), 0)
# Need to find the shortest distance from the bottom
# right corner of the graph (which is (len(Config.words_to_graph), 0))
# to the exponential curve
# Data needs to be normalized

x_max = max(x)
x_min = min(x)
x_normalized = (x-x_min) / (x_max - x_min)

y_min = min(y)
y_max = max(y)
y_normalized = (y - y_min) / (y_max - y_min)


# The following functions are required for
# finding the shortest distance from the point to the curve

min_x, min_y, min_distance, glob_min_index = HelperFunctions.min_distance(x_normalized, y_normalized, (1, 0))
if Config.DEBUG:
    HelperFunctions.print_debug(f"minimum indexes: {min_x} {min_y} {glob_min_index}")
    HelperFunctions.print_debug(f"distance: {min_distance}")

# Un-normalizing
min_x = min_x * (x_max - x_min) + x_min
min_y = min_y * (y_max - y_min) + y_min

pt.plot(min_x, min_y, 'ro')
pt.plot(point_bottom_right[0], point_bottom_right[1], "ro")
pt.plot([point_bottom_right[0], min_x],
        [point_bottom_right[1], min_y],
        'r-')
pt.plot(x, y)

pt.show()



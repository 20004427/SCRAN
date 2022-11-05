import pandas
import keybert
import APIs
import Config
import numpy as np
from pattern.text.en import lexeme


def read_keywords(path, sheet_name):
    """Function to read a list of words from an excel file.
    Returns a Pandas object.

    :param path: (String) Path to the excel file, this can be relative or absolute
    :param sheet_name: (String)
    :return: (Pandas data_frame) matrix of words
    """
    data_frame = pandas.read_excel(path, sheet_name=sheet_name, header=None)
    return data_frame


def print_identifier_error(name, error, link="unknown"):
    """
    The traceback package will print in red text.
    These aren't fatal errors, so I didn't want them to be red.
    Instead, defining my own traceback prints.

    :param name: (string) name of the identifier. i.e. Link
    :param error: (Error | object) Error being caught
    :param link: (String) Optional. Link of the site
    :return: (NONE)
    """
    # The traceback package will print in red text.
    # These aren't fatal errors, so I didn't want them to be red.
    # Instead, defining my own traceback prints.
    if Config.DEBUG:
        print_error(f"{get_traceback_location(error)} {error.__str__()}")
    print_warning(f"Identifier {name} is invalid for the website {link}.")


def print_traceback_location(exception):
    """
    A method to print traceback location.
    Would use the traceback package. However, I wanted to print none fatal errors,
    And the traceback package always prints exceptions in red text. Which makes the exceptions look like
    they are fatal.

    :param exception:
    :return: none
    """
    traceback = exception.__traceback__
    while traceback:
        print(f"{traceback.tb_frame.f_code.co_filename}: {traceback.tb_lineno}")
        traceback = traceback.tb_next


def print_debug(string):
    """
    Simple function to print coloured text.
    Makes it easier to see debug print statements.

    :param string:
    :return: (NONE)
    """
    print(f"{Config.DEBUG_TEXT_COLOR}[DEBUG] {string} {Config.PRINT_TEXT_ENDC}")


def print_error(string):
    """
    Simple function to print coloured text.
    Makes it easier to see error print statements.

    :param string:
    :return: (NONE)
    """
    print(f"{Config.ERROR_TEXT_COLOR}[ERROR] {string} {Config.PRINT_TEXT_ENDC}")


def print_warning(string):
    """
    Simple function to print coloured text.
    Makes it easier to see warning print statements.

    :param string:
    :return: (NONE)
    """
    print(f"{Config.WARNING_TEXT_COLOR}[WARNING] {string} {Config.PRINT_TEXT_ENDC}")


def get_traceback_location(exception):
    """
    A method to get traceback location.
    Would use the traceback package. However, I wanted to print none fatal errors,
    And the traceback package always prints exceptions in red text. Which makes the exceptions look like
    they are fatal.

    :param exception:
    :return: (String)
    """
    traceback = exception.__traceback__
    ret = ""
    while traceback:
        ret += f"{traceback.tb_frame.f_code.co_filename}: {traceback.tb_lineno}\n"
        traceback = traceback.tb_next
    return ret


def extract_keywords_from_scrape(scrape_list, lexeme_dictionary, parent_keyword, no_keywords=3):
    """
    Takes the scrape results and extracts the keywords from it.
    Returns a list of the n most commonly occurring keywords from the different
    site descriptions. Note: it will not count keywords that occur 0 times.

    :param parent_keyword: (String) the keyword for the current iteration.
        So that it isn't included in the returned keywords
    :param no_keywords: (int) The number of keywords to return
    :param scrape_list: a list of scrape results in the form [{'link': ... , 'title': ..., 'text': ...}]
    :param lexeme_dictionary: the list of inputted keywords and their corresponding inflections
    :return: (list| string) list of keywords
    """
    keyword_counts = {}
    kb = keybert.KeyBERT()
    for site in scrape_list:
        blurb = site['text'].replace("...", "")
        if Config.DEBUG:
            print_debug(blurb)
        # This gets the keywords.
        # Ignoring any keywords in the blacklist
        keywords = [i[0] for i in kb.extract_keywords(blurb) if i[0].lower() not in Config.BLACKLIST_KEYWORDS]
        # for each of the keywords, running the lexeme and taking the first inflection.
        # Also lowering them - so that we don't get duplicates
        keywords = [lexeme(i)[0].lower() for i in keywords]
        # now adding the keywords to keyword counts
        for keyword in set(keywords):
            if keyword not in keyword_counts:
                keyword_counts[keyword] = keywords.count(keyword)
            else:
                keyword_counts[keyword] += keywords.count(keyword)
        print(f"For {parent_keyword}, the learning algorithm got: {keywords}")
    # filtering and sorting the keywords
    keyword_counts = dict(filter(lambda x: x[1] > 0, keyword_counts.items()))
    try:
        sorted(keyword_counts, key=lambda x: x[1], reverse=True)
    except Exception as e:
        print_traceback_location(e)

    # Filtering out numeric values
    ret_keywords = []
    for word in keyword_counts:
        try:
            float(word)
        except ValueError:
            ret_keywords.append(word)

    if len(ret_keywords) <= no_keywords:
        return ret_keywords
    return ret_keywords[:no_keywords]


def export_to_pajek(graph, original_nodes=[]):
    """
    Exports the graph for use in pajek

    :param graph: (Graph) a undirected Graph
    :param original_nodes: (Array)
    :return: (NONE)
    """
    file = open("output.NET", "w+")
    # Adding the vertices
    file.write(f"*vertices {len(graph.nodes)}\n")
    vertex_ids = {}
    for vertex in graph.nodes:
        vertex_id = list(graph.nodes).index(vertex) + 1
        # Pajek indexing starts from 1 not 0
        string_to_write = f"{vertex_id} \"{vertex}\" "
        if vertex in original_nodes:
            string_to_write += f"ic {Config.PAJEK_ORIGINAL_NODE_COLOR}\n"
        else:
            string_to_write += f"ic {Config.PAJEK_OTHER_NODE_COLOR}\n"
        file.write(string_to_write)
        vertex_ids[vertex] = vertex_id
    file.write("*Edges\n")
    # You don't have to declare the vertices,
    # Pajek will automatically add them via edges
    for vertex, vertex_2 in graph.edges:
        file.write(f"{vertex_ids[vertex]} {vertex_ids[vertex_2]}\n")
    file.close()


def cleanup_graph(graph):
    """
    Function to cleanup the graph.

    :param graph: (networkx)
    :return: None
    """
    # because we are using a lexeme, it is very unlikely we will
    # have a node contained in more than one neighbor
    # This is a TODO: allow for this possibility
    #               See issue 9: https://github.com/20004427/SCRAN/issues/9

    # creating a copy of the nodes, so that we can loop through them
    # doing it this way so that it's a deep copy
    current_nodes = [i for i in graph.nodes]

    for node in current_nodes:
        new_node = ""
        node_neighbors = [i for i in graph.neighbors(node)]
        for neighbor in node_neighbors:
            if node in neighbor:
                new_node = neighbor
        # removing a node from networkx, will remove all Edges
        # it doesn't clean the up graph.
        # so re-adding the edges here.
        if new_node != "":
            node_neighbors.remove(new_node)
            for neighbor in node_neighbors:
                graph.add_edge(new_node, neighbor)
            graph.remove_node(node)


def recursively_scrape_word(word, lexeme_dictionary, graph, n=0):
    """
    Function to recursively scrape google for linking keywords given an input word
    to start from. There is no need for this to return anything but the boolean value.
    Since a graph object is used to store the nodes and edges.

    :param word:
    :param lexeme_dictionary:
    :param graph:
    :param n: (int) current recursion depth
    :return: (Boolean) True: The word is above the minimum search result count limit.
                       False: The word is below, or equal to, the minimum search result count limit.
    """
    word = word.lower()
    if n > Config.GOOGLE_SCRAPE_RECURSION_DEPTH_LIMIT:
        return False
    graph.add_node(word)
    scrape_output = APIs.scrape_google(word)
    scrape_results = scrape_output[1:]
    number_of_search_results = scrape_output[0]
    Config.words_to_graph.append(word)
    Config.values_to_graph.append(number_of_search_results)
    linking_keywords = extract_keywords_from_scrape(scrape_results, lexeme_dictionary, word)
    for w in linking_keywords:
        if recursively_scrape_word(w, lexeme_dictionary, graph, n+1):
            graph.add_edge(word, w)
    if Config.DEBUG:
        print(f"The keywords relating to {word} are {linking_keywords}")
    return True


def extract_from_soup(soup, input_, find_all=False):
    """
    HelperFunction - removes duplicate code from APIs

    :param soup: (BeautifulSoup)
    :param input_: (Array| String) ["html element", "class or id", "identifier_name"]
    :param find_all: (Boolean)
    :return: array of html elements
    """
    if find_all:
        if len(input_) == 1:
            return soup.select(input_[0])
        elif input_[1] is None:
            return soup.find_all(input_[0])
        elif input_[1] == "id":
            return soup.find_all(input_[0], id=input_[2])
        else:
            return soup.find_all(input_[0], class_=input_[2])
    else:
        if len(input_) == 1:
            return soup.select_one(input_[0])
        elif input_[1] is None:
            return soup.find(input_[0])
        elif input_[1] == "id":
            return soup.find(input_[0], id=input_[2])
        else:
            return soup.find(input_[0], class_=input_[2])


def distance(x0, y0, x1, y1):
    """
    Computes the distance between two points

    :param x0: (double)
    :param y0: (double)
    :param x1: (double)
    :param y1: (double)
    :return: (double) distance between the two points
    """
    x_distance = x0 - x1
    y_distance = y0 - y1
    return np.sqrt(x_distance**2 + y_distance**2)


def min_distance(x, y, point):
    """
    computes the shortest distance between a curve and a point.

    :param x: (np.linespace) x domain
    :param y: (np.array) f(x)
    :param point: [x, y]
    :return:
    """
    distances = [distance(x[i], y[i], point[0], point[1]) for i in range(len(x))]
    print(f"number of distances: {len(distances)}")
    min_index = distances.index(min(distances))
    return x[min_index], y[min_index], distances, min_index

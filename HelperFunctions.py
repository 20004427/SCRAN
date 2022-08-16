import pandas
import keybert
import Config
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
    Currently just using the inputted  keywords.
    TODO: Add learning algorithm to extract keywords,
        see issue #7 : https://github.com/20004427/SCRAN/issues/7
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
        print(blurb)
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
        print(f"the learning algorithm got: {keywords}")
    # filtering and sorting the keywords
    keyword_counts = dict(filter(lambda x: x[1] > 0, keyword_counts.items()))
    sorted(keyword_counts, key=lambda x: x[1], reverse=True)
    ret_keywords = [i for i in keyword_counts]
    if len(ret_keywords) <= no_keywords:
        return ret_keywords
    return ret_keywords[:no_keywords]


def export_to_pajek(graph):
    """
    Exports the graph for use in pajek

    :param graph: (Graph) a undirected Graph
    :return: (NONE)
    """
    file = open("output.NET", "w+")
    # Adding the vertices
    file.write(f"*vertices {len(graph.nodes)}\n")
    vertex_ids = {}
    for vertex in graph.nodes:
        vertex_id = list(graph.nodes).index(vertex) + 1
        # Pajek indexing starts from 1 not 0
        file.write(f"{vertex_id} \"{vertex}\"\n")
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

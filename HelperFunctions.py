import pandas
from pattern.text.en import lexeme
import keybert


def read_keywords(path, sheet_name, column_headers=None):
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
        keywords = [i[0] for i in kb.extract_keywords(blurb)]
        # for each of the keywords, running the lexeme and taking the first inflection.
        keywords = [lexeme(i)[0] for i in keywords]
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
    file.write(f"*vertices {len(graph.vertices)}\n")
    for vertice in graph.vertices:
        # Pajek indexing starts from 1 not 0
        file.write(f"{list(graph.vertices.keys()).index(vertice) + 1} \"{vertice}\"\n")
    file.write("*Edges\n")
    # You don't have to declare the vertices,
    # Pajek will automatically add them via edges
    for vertice, vertice_2 in graph.visual:
        file.write(f"{list(graph.vertices.keys()).index(vertice) + 1} {list(graph.vertices.keys()).index(vertice_2) + 1}\n")
    file.close()


import pandas


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


def extract_keywords_from_scrape(scrape_list, keywords, no_keywords=3):
    """
    Currently just using the inputted  keywords.
    TODO: Add learning algorithm to extract keywords,
        see issue #7 : https://github.com/20004427/SCRAN/issues/7
    Takes the scrape results and extracts the keywords from it.
    Returns a list of the n most commonly occurring keywords from the different
    site descriptions. Note: it will not count keywords that occur 0 times.

    :param no_keywords: (int) The number of keywords to return
    :param scrape_list: a list of scrape results in the form [{'link': ... , 'title': ..., 'text': ...}]
    :param keywords: the list of inputted keywords
    :return: (list| string) list of keywords
    """
    keyword_counts = {i: 0 for i in keywords}
    for site in scrape_list:
        blurb = site['text']
        for keyword in keywords:
            keyword_counts[keyword] += blurb.count(keyword)
    # filtering and sorting the keywords
    keyword_counts = dict(filter(lambda x: x[1] > 0, keyword_counts.items()))
    sorted(keyword_counts, key=lambda x: x[1], reverse=True)
    ret_keywords = keyword_counts.keys()
    if len(ret_keywords) <= no_keywords:
        return ret_keywords
    return ret_keywords[:no_keywords]


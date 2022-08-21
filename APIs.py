import requests
import urllib
from requests_html import HTMLSession

import Config
import HelperFunctions


# __________ GOOGLE __________


def scrape_google(word):
    """
    Function to scrape google results.
    Looks at the top 10 sites, and looks for keywords.
    Returns a list of keywords.
    Note that the input does not need to contain 'supply chain',
    This function adds 'Supply chain' to the start of the query.
    This isn't technically an API, but thought that it should probably be here.
    TODO: Move this function to a different location?
        See issue #5: https://github.com/20004427/SCRAN/issues/5

    :param word: (String) Ideally a word, but can be a phrase
    :return: (Array| String) List of keywords relating to the input
    """
    stats_text = ""
    number_of_search_results = None
    query = urllib.parse.quote_plus("Supply chain " + word)
    response = get_source(f"https://www.google.co.nz/search?q={query}")

    try:
        stats_text = response.html.find(Config.GOOGLE_SCRAPE_IDENTIFIER_STATS, first=True).text
    except AttributeError as e:
        HelperFunctions.print_identifier_error("stats", e)
    # Extracting the no of results from the stats_text
    # We know it should always be the 2nd string in the list when split.
    # raw, the stats_text is:
    #   About 940,000 results
    #   (0.22 seconds)
    if stats_text != "":
        number_of_search_results = int("".join(stats_text.split()[1].split(",")))
    if Config.DEBUG:
        print(f"number of search results for {word}: {number_of_search_results}")

    # TODO: see issue #6 https://github.com/20004427/SCRAN/issues/6
    results = list(response.html.find(Config.GOOGLE_SCRAPE_IDENTIFIER_SECTION))

    ret = []
    for result in results:
        link = ""
        text = ""
        title = ""
        try:
            link = result.find(Config.GOOGLE_SCRAPE_IDENTIFIER_LINK, first=True).attrs['href']
        except AttributeError as e:
            HelperFunctions.print_identifier_error("link", e, link)
        # Filtering out any links in the blacklist
        if len([1 for i in Config.GOOGLE_SCRAPE_BLACKLIST if link.startswith(i)]) == 0:
            try:
                title = result.find(Config.GOOGLE_SCRAPE_IDENTIFIER_TITLE, first=True).text
            except AttributeError as e:
                HelperFunctions.print_identifier_error("title", e, link)

            try:
                text = result.find(Config.GOOGLE_SCRAPE_IDENTIFIER_TEXT, first=True).text
            except AttributeError as e:
                HelperFunctions.print_identifier_error("text", e, link)

            item = {'title': title,
                    'link': link,
                    'text': text}
            ret.append(item)

    # restricting the scrape to the first 10 sites
    if len(ret) > Config.GOOGLE_SCRAPE_NO_SITES:
        ret = ret[:Config.GOOGLE_SCRAPE_NO_SITES]
    return ret


def google_scholar_word_popularity(word):
    """Takes a word and finds the number of results for that word in google scholar.
    This is used to:
    a) weight the nodes
    b) check if we should stop the recursion.

    :param word: (String)
    :return: (int) number of results.
    """
    stats_text = ""
    query = urllib.parse.quote_plus("Supply chain " + word)
    response = get_source(f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={query}")
    number_of_google_scholar_results = 0
    try:
        stats_text = response.html.find(Config.GOOGLE_SCHOLAR_IDENTIFIER_STATS)
    except AttributeError as e:
        HelperFunctions.print_identifier_error("stats", e)
    # unlike the google search results, google scholar uses a class instead of an id for the
    # stats. So looping through the divs with that class until one works correctly -
    # this can be presumed to be the correct div.
    for i in stats_text:
        # i is a html element object

        # Extracting the no of results from the stats_text
        # We know it should always be the 2nd string in the list when split.
        # raw, the stats_text is:
        #   About 940,000 results
        #   (0.22 seconds)
        try:
            number_of_search_results = int("".join(i.text.split()[1].split(",")))
            # once the number_of_search_results has been found we can just break the loop
            break
        except ValueError as e:
            if Config.DEBUG:
                HelperFunctions.print_identifier_error("stats", e)

    if Config.DEBUG:
        print(f"number of search results for {word}: {number_of_search_results}")
    return number_of_search_results


def get_source(url):
    """Returns the source code for the provided URL.

    :param url: (String) Url of the page to scrape
    :return: (object | requests_html)
    """
    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except requests.exceptions.RequestException as e:
        if Config.DEBUG:
            print(f"[ERROR] {e.strerror}")
        return -1

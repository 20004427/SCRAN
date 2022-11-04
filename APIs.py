import requests
import urllib
import time
import random

import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import Config
import HelperFunctions


# __________ GOOGLE __________


def scrape_google(word):
    """
    Function to scrape google results.
    Returns the number of search results followed by a list of scrapes.
    Each scrape site is a dictionary
    Note that the input does not need to contain 'supply chain',
    This function adds 'Supply chain' to the start of the query.
    This isn't technically an API, but thought that it should probably be here.
    TODO: Move this function to a different location?
        See issue #5: https://github.com/20004427/SCRAN/issues/5

    :param word: (String) Ideally a word, but can be a phrase
    :return: (Array| String) number of search results for the input word,
        Followed by a list of scrape results.
        i.e. [1000, {'link': "https:// www.thisisanexample.com",
                      'text': "Hey, that's pretty pog",
                     'title': "The art of pogness"}, ...]
    """
    while True:
        repeat = False
        search_engine_name = list(Config.SCRAPE_SEARCH_ENGINES.keys())[Config.google_search_engine]
        # We can do this since the values will be unique
        search_engine = Config.SCRAPE_SEARCH_ENGINES[search_engine_name]
        number_of_search_results = None
        query = urllib.parse.quote_plus(f"\"Supply chain {word}\"")
        response = get_source(search_engine["url"].format(query))
        if response == -1:
            repeat = True
        print(search_engine)
        Config.increment_search_engine()
        wait_time = random.randrange(Config.SCRAPE_MIN_DELAY, Config.SCRAPE_MAX_DELAY)
        time.sleep(wait_time)

        soup = BeautifulSoup(response.page_source, features="html.parser")

        identifier_stats = search_engine["identifier_stats"]
        stats_text = ""
        try:
            if identifier_stats is not None:
                stats_text = HelperFunctions.extract_from_soup(soup, identifier_stats).text
        except AttributeError as e:
            HelperFunctions.print_identifier_error("stats", e)
            # Checking to see if the ip has been blocked
            block_check = search_engine["block_check"]
            if block_check is not None:
                text = HelperFunctions.extract_from_soup(soup, block_check[0])
                if text is not None and block_check[1] in text:
                    HelperFunctions.print_warning(f"Search engine {search_engine_name} "
                                                  "has blocked this ip!")
                    HelperFunctions.print_warning(f"Adding {search_engine_name} to a "
                                                  "blacklist for the remainder of this run.")
                    Config.add_current_search_engine_to_blacklist()
                    repeat = True
        # Extracting the no of results from the stats_text
        if stats_text != "":
            if search_engine_name == "bing":
                # For Bing sometimes, the stats text is in the form "About 999,000,000 results.
                # Other times it is "999,000,000 results. So handling this case
                stats_text_split = stats_text.split()
                if len(stats_text_split) == 3:
                    # "About 999,000,000 results" case
                    number_of_search_results_text = stats_text_split[1]
                else:
                    number_of_search_results_text = stats_text_split[0]
                number_of_search_results = int("".join(number_of_search_results_text.split(",")))
            else:
                number_of_search_results = int("".join(stats_text.split()[1].split(",")))
        if Config.DEBUG:
            HelperFunctions.print_debug(f"number of search results for {word}: {number_of_search_results}")

        # TODO: see issue #6 https://github.com/20004427/SCRAN/issues/6
        identifier_section = search_engine["identifier_section"]
        results = HelperFunctions.extract_from_soup(soup, identifier_section, find_all=True)
        if not repeat:
            break
    ret = [number_of_search_results]
    for result in results:
        link = ""
        text = ""
        title = ""
        try:
            identifier_link = search_engine["identifier_link"]
            # Special exception for dogpile.
            # The structure of dogpile is very different from the other search engines,
            # That there wasn't any easy way of using the generic method
            if search_engine_name == "dogpile":
                link_section = result
            else:
                for i in identifier_link:
                    link_section = HelperFunctions.extract_from_soup(result, i)
            link = link_section.find("a").attrs['href']
        except AttributeError as e:
            HelperFunctions.print_identifier_error("link", e, link)
        # Filtering out any links in the blacklist
        if len([1 for i in Config.GOOGLE_SCRAPE_BLACKLIST if link.startswith(i)]) == 0:
            try:
                identifier_title = search_engine["identifier_title"]
                if identifier_title[1] is None:
                    title = result.find(identifier_title[0]).text
                else:
                    title = HelperFunctions.extract_from_soup(result, identifier_title).text
            except AttributeError as e:
                HelperFunctions.print_identifier_error("title", e, link)

            try:
                identifier_text = search_engine["identifier_text"]
                text = HelperFunctions.extract_from_soup(result, identifier_text).text
            except AttributeError as e:
                HelperFunctions.print_identifier_error("text", e, link)
            if title is not None and \
                    link is not None and \
                    text is not None:
                item = {'title': title,
                        'link': link,
                        'text': text}
                ret.append(item)

    # restricting the scrape to the first 10 sites
    if len(ret) - 1 > Config.GOOGLE_SCRAPE_NO_SITES:
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
    query = urllib.parse.quote_plus("\"Supply chain\" " + word)
    response = get_source(f"https://scholar.google.com/scholar?q={query}")
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
            number_of_google_scholar_results = int("".join(i.text.split()[1].split(",")))
            # once the number_of_search_results has been found we can just break the loop
            break
        except ValueError as e:
            if Config.DEBUG:
                HelperFunctions.print_identifier_error("stats", e)

    if Config.DEBUG:
        HelperFunctions.print_debug("number of search results for \"supply chain\" "
                                    f"{word}: {number_of_google_scholar_results}")
    return number_of_google_scholar_results


def get_source(url):
    """Returns the source code for the provided URL.

    :param url: (String) Url of the page to scrape
    :return: (object | requests_html)
    """
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        return driver
    except requests.exceptions.RequestException as e:
        if Config.DEBUG:
            HelperFunctions.print_error(e.strerror)
        return -1
    except selenium.common.exceptions.WebDriverException as e:
        if Config.DEBUG:
            HelperFunctions.print_debug(f"URL {url}")
            HelperFunctions.print_error(e.strerror)
        return -1

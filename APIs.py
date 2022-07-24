import requests
import urllib
import json
from pattern.text.en import lexeme
from io import BytesIO
from requests_html import HTML
from requests_html import HTMLSession

import Config


def get_word_definition(word):
    """
    Function to extract the correct definition from the returned json data.
    calls the 'make_call_to_dictionary' function to get the data

    :param word: (STRING)
    :return: (STRING) definition of the word
    """
    #TODO: A problem here is how to choose the correct definition, as some have multiple definitions.
    # At the moment this just takes the first definition
    # See Issue #3, https://github.com/20004427/SCRAN/issues/3#issue-1300348874
    json_data = make_call_to_dictionary(word)
    if json_data == -1:
        return json_data
    meanings = json_data["meanings"]
    definitions = meanings[0]["definitions"]
    return definitions[0]["definition"]


def make_call_to_dictionary(word):
    """
    Function to make a call to the dictionary api.
    Documentation can be found here: https://dictionaryapi.dev/

    :param word: (STRING) The word to fetch
    :return: (JSON) all the data for the word
    """
    # TODO: time api call, See issue #1, https://github.com/20004427/SCRAN/issues/1

    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    if Config.DEBUG:
        print(response.json())
    try:
        return response.json()[0]
    except KeyError as e:
        print(f"[WARNING] Definition not found for {word}")
        return -1

# __________ GOOGLE __________
# Tutorial/ example: https://practicaldatascience.co.uk/data-science/how-to-scrape-google-search-results-using-python


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
    query = urllib.parse.quote_plus("Supply chain " + word)
    response = get_source(f"https://www.google.co.nz/search?q={query}")
    links = list(response.html.absolute_links)


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
            print(f"[ERROR] {e.strerror()}")
        return -1

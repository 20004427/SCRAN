import requests
import json
from pattern.text.en import lexeme
from io import BytesIO



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

    # Setting up a buffer to handle the response
    response_buffer = BytesIO()
    # Setting up pycurl to get the data/ make request to the dictionary
    curl = pycurl.Curl()

    # Setting the pycurl options
    curl.setopt(curl.SSL_VERIFYPEER, False)
    curl.setopt(curl.URL, f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

    curl.perform()
    curl.close()

    # converting the response data to a json object - so that the data can be read easier
    response = json.loads(response_buffer.getvalue().decode("UTF-8"))
    return response[0]

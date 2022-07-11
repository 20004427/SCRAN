import pycurl, json
from io import BytesIO


def get_word_definition(word):
    """
    Function to make a call to the dictionary api.
    Documentation can be found here: https://dictionaryapi.dev/

    :param word: (STRING) The word to fetch
    :return: (STRING) the word definition
    """
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

    #TODO: it may be worth changing this to a return all data
    # then creating separate sections to handle data extraction

    # converting the response data to a json object - so that the data can be read easier
    response = json.loads(response_buffer.getvalue().decode("UTF-8"))
    return json.dumps(response)

import APIs
import Config

word_list = []

if Config.USE_TEST_DATA:
    word_list = ["Bamboozled", "Risk", "Shipping", "Packaging"]

for word in word_list:
    definition = APIs.get_word_definition(word)
    print(definition)
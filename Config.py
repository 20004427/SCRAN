import HelperFunctions
# __________ Config/ global variables __________
# ____ RUNTIME GLOBALS (NON-CONSTANT)
# This is used by Main, HelperFunctions, and APIs,
# So made it global - so that we don't have to keep passing about and returning it.
global google_search_engine, search_engine_blacklist
google_search_engine = 0

# ____ CONSTANTS ____
DEBUG = True
# Using ANSI color
DEBUG_TEXT_COLOR = "\033[0;36m"  # Cyan
ERROR_TEXT_COLOR = "\033[0;33m"  # Yellow NONE FATAL (so not red)
WARNING_TEXT_COLOR = "\033[0;35m"  # Purple
PRINT_TEXT_ENDC = "\033[00m"
USE_TEST_DATA = True
USE_POPULARITY_ON_INPUT = False
PATH_TO_WORD_LIST = "words.xlsx"
WORD_LIST_SHEET_NAME = "Combined Words"
MINIMUM_WORD_POPULARITY = 10000
# ____ Google scrape ____
# blacklist for google scrape
GOOGLE_SCRAPE_BLACKLIST = ["https://www.youtube.",
                           "https://www.google.",
                           "https://maps.",
                           "https://support."]

# This is the css attribute given to results by google
# This is subject to change, maybe worth investigating a better way to do this?
# TODO: Is there a better way to find the articles in a google search result
#   And extract the text from them? See issue #6 https://github.com/20004427/SCRAN/issues/6

# The different search engines have different html classes/ id's.
# So using a dictionary to store them.
# Note: you don't have to use keys to access items, you can
#       get the values as an iterable
# Stored as {search engine name:
#               {url:, identifier_section:, identifier_title:,
#               identifier_link:, identifier_text:, identifier_stats:}}
# None means that it doesn't exist for that search engine
SCRAPE_SEARCH_ENGINES = {"google": {"url": "https://www.google.co.nz/search?q={}",
                                    "identifier_section": ["div", "class", "tF2Cxc"],
                                    "identifier_title": ["h3", None],
                                    "identifier_link": [["div", "class", "yuRUbf"]],
                                    "identifier_stats": ["div", "id", "result-stats"],
                                    "identifier_text": [".VwiC3b > span"],
                                    "block_check": ["div", "id", "infoDiv"]},
                         "bing": {"url": "https://www.bing.com/search?q={}",
                                  "identifier_section": ["li", "class", "b_algo"],
                                  "identifier_title": ["h2", None],
                                  "identifier_link": [[".b_title > h2"], ["h2", None]],
                                  "identifier_stats": ["span", "class", "sb_count"],
                                  "identifier_text": ["p", "class", "b_lineclamp2"]},
                         "duckduckgo": {"url": "https://duckduckgo.com/?q={}",
                                        "identifier_section": ["article", "class", "yQDlj3B5DI5YO8c8Ulio"],
                                        "identifier_title": ["span", "class", "EKtkFWMYpwzMKOYr0GYm"],
                                        "identifier_link": [["h2", "class", "LnpumSThxEWMIsDdAT17"]],
                                        "identifier_stats": None,
                                        "identifier_text": ["div", "class", "OgdwYG6KE2qthn9XQWFC"]},
                         "yahoo": {"url": "https://nz.search.yahoo.com/search?q={}",
                                   "identifier_section": ["div", "class", "algo-sr"],
                                   "identifier_title": ["h3", "class", "title"],
                                   "identifier_link": [["h3", "class", "title"]],
                                   "identifier_stats": ["span", "class", ".fz-14"],
                                   "identifier_text": ["span", "class", "fc-falcon"],
                                   "block_check": None},
                         "dogpile": {"url": "https://dogpile.com/serp?q={}",
                                     "identifier_section": ["div", "class", "web-bing__result"],
                                     "identifier_title": ["a", "class", "web-bing__title"],
                                     "identifier_link": [["web-bing__title"]],
                                     "identifier_stats": None,
                                     "identifier_text": ["span", "class", "web-bing__description"]}
                         }

# Delay is in seconds
SCRAPE_MIN_DELAY = 0
SCRAPE_MAX_DELAY = 5
GOOGLE_SCRAPE_NO_SITES = 10
GOOGLE_SCRAPE_RECURSION_DEPTH_LIMIT = 1
GOOGLE_SCRAPE_DO_RECURSION = True

# ___ GOOGLE SCHOLAR ___
GOOGLE_SCHOLAR_IDENTIFIER_STATS = ".gs_ab_mdw"


# Blacklist of keywords to ignore
# Note: The program will automatically change everything to lowercase
#       This prevents duplicate nodes.
#       So words in this list need to be lowercase, because this is a constant.
BLACKLIST_KEYWORDS = ["supply",
                      "chain",
                      "supplychain",
                      "supply chain",
                      "chains"]
# ____ Pajek ____
PAJEK_ORIGINAL_NODE_COLOR = "Green"
PAJEK_OTHER_NODE_COLOR = "Purple"

# Global variables
# matplotlib bar graph requires two arrays
# one for the x axis and one for the y axis.
words_to_graph = []
values_to_graph = []

# Blacklist for search engines.
# These are search engines that have blocked this ip.
# These are the indexes of the search engines.
search_engine_blacklist = []


# __________ FUNCTIONS __________
# These functions are here to change variables
# in the config.
def increment_search_engine():
    global google_search_engine, search_engine_blacklist
    flag = True
    while flag:
        if google_search_engine + 1 == len(SCRAPE_SEARCH_ENGINES):
            google_search_engine = 0
        else:
            google_search_engine += 1
        if google_search_engine not in search_engine_blacklist:
            flag = False


def add_current_search_engine_to_blacklist():
    global google_search_engine, search_engine_blacklist
    search_engine_blacklist.append(google_search_engine)

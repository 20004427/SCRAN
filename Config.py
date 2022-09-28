# __________ Config/ global variables __________
# ____ RUNTIME GLOBALS (NON-CONSTANT)
# This is used by Main, HelperFunctions, and APIs,
# So made it global - so that we don't have to keep passing about and returning it.
google_search_engine = 0

# ____ CONSTANTS ____
DEBUG = True
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
                                    "identifier_link": ["div", "class", "yuRUbf"],
                                    "identifier_stats": ["div", "id", "result-stats"],
                                    "identifier_text": ["div", "class", "VwiC3b"]},
                         "bing": {"url": "https://www.bing.com/search?q={}",
                                  "identifier_section": ".b_algo",
                                  "identifier_title": "h2",
                                  "identifier_link": ".b_algoheader a",
                                  "identifier_stats": ".sb_count",
                                  "identifier_text": ".b_lineclamp2"},
                         "duckduckgo": {"url": "https://duckduckgo.com/?q={}",
                                        "identifier_section": ".links_deep",
                                        "identifier_title": "span",
                                        "identifier_link": ".LnpumSThxEWMIsDdAT17 a",
                                        "identifier_stats": None,
                                        "identifier_text": ".OgdwYG6KE2qthn9XQWFC"},
                         "yahoo": {"url": "https://nz.search.yahoo.com/search?q={}",
                                   "identifier_section": ".algo-sr",
                                   "identifier_title": ".ls-05",
                                   "identifier_link": ".ls-05",
                                   "identifier_stats": ".fz-14",
                                   "identifier_text": ".fbox-lc3"},
                         "dogpile": {"url": "https://dogpile.com/serp?q={}",
                                     "identifier_section": ".web-bing__result",
                                     "identifier_title": "a",
                                     "identifier_link": ".web-bing__title",
                                     "identifier_stats": None,
                                     "identifier_text": ".web-bing__description"}
                         }
# Delay is in seconds
SCRAPE_MIN_DELAY = 0
SCRAPE_MAX_DELAY = 5
GOOGLE_SCRAPE_NO_SITES = 10
GOOGLE_SCRAPE_RECURSION_DEPTH_LIMIT = 2
GOOGLE_SCRAPE_DO_RECURSION = False

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

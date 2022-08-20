# __________ Config/ global variables __________
# ____ CONSTANTS ____
DEBUG = True
USE_TEST_DATA = True
PATH_TO_WORD_LIST = "words.xlsx"
WORD_LIST_SHEET_NAME = "Combined Words"
# ____ Google scrape ____
# blacklist for google scrape
GOOGLE_SCRAPE_BLACKLIST = ["https://www.youtube.",
                           "https://www.google.",
                           "https://maps.",
                           "https://support."]
GOOGLE_SCRAPE_NO_SITES = 10
# This is the css attribute given to results by google
# This is subject to change, maybe worth investigating a better way to do this?
# TODO: Is there a better way to find the articles in a google search result
#   And extract the text from them? See issue #6 https://github.com/20004427/SCRAN/issues/6
GOOGLE_SCRAPE_IDENTIFIER_SECTION = ".tF2Cxc"
GOOGLE_SCRAPE_IDENTIFIER_TITLE = "h3"
GOOGLE_SCRAPE_IDENTIFIER_LINK = ".yuRUbf a"
GOOGLE_SCRAPE_IDENTIFIER_TEXT = ".VwiC3b"
GOOGLE_SCRAPE_IDENTIFIER_STATS = "#result-stats"

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

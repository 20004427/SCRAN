# __________ Config/ global variables __________
# NOTE: THESE ARE ALL CONSTANTS!
DEBUG = True
USE_TEST_DATA = False
PATH_TO_WORD_LIST = "words.xlsx"
WORD_LIST_SHEET_NAME = "Combined Words"
# ____ Google scrape _____
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

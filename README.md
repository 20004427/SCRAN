# SCRAN
***
### Input
<b>Takes an excel spreadsheet as input.</b> This files needs to be in the directory root, and called "Words.xlsx" - Although this 
can be configured in the Config.py 
The excel spreadsheet can include inflections (optional). For instance:
<table>
<tr><td>Ship</td><td>Shipping</td><td>shipped</td></tr>
<tr><td>Export</td><td></td><td></td></tr>
<tr><td>Inflation</td><td></td><td></td></tr>
<tr><td>Warehouse</td><td>warehousing</td><td></td></tr>
</table>
<b>NOTE: </b>The program uses a lexeme library - so most inflections are automatically included.
This just allows you to include some more obscure supply chain related inflections.
See the "External Documentation" section for more information about the lexeme library.
<br/><br/>

### Output
The <b>output is stored in output.NET in the project root.</b><br/>
Nodes in the output file are colour coded as follows:
- Purple: None-original nodes 
- Green: The nodes contained in the input file

<b>NOTE:</b> By default, Pajek will not use the colours for nodes and edges contained within the 
Input file. To enable the .net node colours, first load the .net file into pajek. Then draw the network.
Once this is done, in the top bar, click options -> Colors -> Vertices -> As defined in the .net file.
Pajek will now use the colours in the .net file rather than the user defined colours. 
For more info, see: https://blog.katastros.com/a?ID=00500-7af1781a-21ab-42e3-8e79-d36ae54d2487 
***

## Requirements
### Current working with Python3.10
- pybind11
- requests~=2.28.1
- requests_html
- pandas~=1.3.4
- pattern~=3.6
- openpyxl
- networkx~=2.8.5
- matplotlib~=3.5.2
- keybert~=0.6.0
- bs4~=0.0.1
- beautifulsoup4~=4.11.1
- webdriver-manager
- selenium~=4.4.3
- numpy~=1.23.1
- scipy~=1.8.1

***
## External documentation
- Dictionary API: https://dictionaryapi.dev/ 
- Lexeme API: http://digiasset.org/html/pattern-en.html
- Selenium: https://pypi.org/project/selenium/ 


***
## Setup Instructions
1. Install Python 3.10 - found here: https://www.python.org/downloads/release/python-3100/
2. Download this repo. You can do this from this page by clicking on code and either downloading it as a zip, or cloning the repo using git.
3. Open Command prompt or Powershell, and cd to the root of the project. Some helpful commands:
   1. <code>ls</code> - lists all files/ directories in the current directory 
   2. <code>cd</code> - "Change directory", doesn't have to be a single relative path can also be 
        <code>cd C:/example/path</code> or <code>cd example/foo/u/file</code>
        Note: Changing drive i.e. from C to D doesn't always work in the CMD - use powershell instead.
4. From the root of the project install the requirements by running <code>pip install -r requirements.txt</code>\
    If you know how to, use a virtual environment. You can install PyCharm (https://www.jetbrains.com/pycharm/download/#section=windows) which will 
    set up the Virtual environment for you.
5. To run the program, run the following command from the project root: <code>python Main.py</code>
   Note: this currently requires you to have the Words.xlsx file in you project root. This file is <b>NOT INCLUDED</b> with the repo.
   It is just a list of supply chain keywords which is used as a start point for the program. Alternatively, you can go into 
   <code>Main.py</code> and edit the <code>word_list</code> var in the first <code>if</code> statement. This also requires the
   <code>Config.py</code> to be edited. Just change <code>USE_TEST_DATA</code> to true. 

The program uses a Lexeme library which means that word inflections are not required as input. However, this can be overridden by 
including you own inflections in the adjacent columns to the word. The lexeme has most words - but there may be some obscure supply 
chain keywords that it doesn't have. Please note that there must be no empty cells in the xlsx file - as the program will go to the next line 
once it finds an empty cell. And the program will stop when an empty row is found.

***
## Configuration
- <code>DEBUG</code>: enables debugging - basically just adds additional print statements to the output.
- <code>USE_TSET_DATA</code>: If true, the hard coded case will be used. Otherwise, a Words.xlsx file is required. 
- <code>USE_POPULARITY_ON_INPUT</code>: If true, words are only added to the graph if the number of results for the
  word is over the <code>MINIMUM_WORD_POPULARITY</code> 
- <code>PATH_TO_WORD_LIST</code>: The relative or absolute path to the words.xlsx file. 
- <code>WORD_LIST_SHEET_NAME</code>: The sheet containing the words within the words.xlsx file. 
- <code>GOOGLE_SCRAPE_BLACKLIST</code>: sites to ignore during a scrape. 
- <code>GOOGLE_SCRAPE_NO_SITES</code>: The number of sites to return from a scrape. 
- <code>GOOGLE_SCRAPE_RECURSION_DEPTH_LIMIT</code>: The number of recursions to do per word. 
- <code>GOOGLE_SCRAPE_DO_RECURSION</code>: If true, the program will recursively search for each word in the input list. 
- <code>BLACKLIST_KEYWORDS</code>: These words will be ignored/ skipped.
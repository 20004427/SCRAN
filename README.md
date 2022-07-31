# SCRAN
***
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

The <b>output is stored in output.NET in the project root.</b>

***

## Requirements
### Current working with Python3.10
- pybind11
- requests
- requests_html
- pandas~=1.3.4
- pattern
- openpyxl
- networkx
- matplotlib

***
## External documentation
- Dictionary API: https://dictionaryapi.dev/ 
- Lexeme API: http://digiasset.org/html/pattern-en.html

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
   It is just a list of supply chain keywords which is used as a start point for the program. 

The program uses a Lexeme library which means that word inflections are not required as input. However, this can be overridden by 
including you own inflections in the adjacent columns to the word. The lexeme has most words - but there may be some obscure supply 
chain keywords that it doesn't have. Please note that there must be no empty cells in the xlsx file - as the program will go to the next line 
once it finds an empty cell. And the program will stop when an empty row is found.
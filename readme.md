Introduction:
The project is to parse Chase statement pdf file and extract transaction information. The parser parses all the transactions and organize the entry which is transactions happened in Taiwan and output them as table with columns: <br> 
**Transaction date, Transaction name, NTD, USD** <br>
note: all the transactions happened in US are removed in output csv file

################　　statementParser.py   ############### <br>
Library requirments:
- Pandas
- PyPDF2
- configparser

How to use the Parsre: 
0. Before running the program, use config.txt to specify the input/output directory and pdf file name
1. open command line mode
2. execute python statementParser.py

The output csv file will refer to the input pdf name and exports a same name file with .csv extension




[IGNORE below] <br>
################　　tabula_statementParse.py (obsolete version)   ###############
Library requirments:
- Pandas
- tabula-py (https://tabula-py.readthedocs.io/en/latest/getting_started.html)

How to use the Parsre: 
1. open command line mode
2. execute python statementParse.py
3. INPUT the pdf file name (include file extension) 

The output csv file will refer to the input pdf name and exports a same name file with .csv extension

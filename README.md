# HSURV Abstract Book Automation Scripts
This is a collection of scripts that I wrote during Harvard Summer Undergraduate Research Village 2017 in order to automate generating the village Abstract Book in LaTeX. 

The abstract book committee took the following actions sequentially:

* Send a Google Form to the village, which asks for information (name, concentration, PI info, etc.), __title__ and __body__ of the abstract.
    - __Note__: paying attention to the formatting of personal/PI information would have saved time
* Given a spreadsheet of information, title, and abstract body, generate a Google doc for each person that contains his/her abstract. Store the link for Google doc created.
    - Script: `gen_docs.py` (uses `pyDrive`)
* Send emails to each person with the link to his/her Google Doc (done using __Mail Merge in Google Spreadsheets__)
* Give fellows a week to peer edit the abstracts in Google Doc, resolve all changes and comment by some deadline
* Directly access each Google Doc using the links stored, and download the text and title for each Doc. Integrate the text into LaTeX:
    - Scripts: 

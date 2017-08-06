# HSURV Abstract Book Automation Scripts

This is a collection of Python code that I wrote during Harvard Summer Undergraduate Research Village 2017 in order to automate generating the village Abstract Book in LaTeX. 

Clone this repository to use the code.

---

The abstract book committee took the following actions sequentially:

* Send a Google Form to the village, which asks for information (name, concentration, PI info, etc.), __title__ and __body__ of the abstract.
    - __Note__: paying attention to the formatting of personal/PI information would have saved time
* Given a spreadsheet of information, title, and abstract body, generate a Google doc for each person that contains his/her abstract. Store the link for Google doc created.
    - Script: `gen_docs.py` (uses `pyDrive`)
* Send emails to each person with the link to his/her Google Doc (done using __Mail Merge in Google Sheets__)
* Give fellows a week to peer edit the abstracts in Google Doc, resolve all changes and comment by some deadline
* Directly access each Google Doc using the links stored, and download the text and title for each Doc. Integrate the text into LaTeX:
    - Scripts/files: `integrate_tex.py` (helper `text_to_abstract.py`), `main.tex`, `abstracts.tex`
* Generate page proofs and upload page proofs to Google Doc
    - Scripts: `gen_pageproof.py`
* Send email to fellows with link to their page proofs (Mail merge). 

## Notes for Each Script

* Note that these scripts __cannot__ be directly run, and __customization__ is absolutely necessary.
* Please regard these scripts as a collection of Python code. I recommend running in an interactive environment such as __Jupyter notebook__.

### TeX Files

* `main.tex` includes the macro code for the `abstract` environment in LaTeX. It should be the file that you compile, using other TeX files as input (`\input{otherfile.tex}`)
* `abstracts.tex` should be a collection of abstract code in the format defined in `main.tex`. This should ideally be output of the code in `integrate_tex.py`. I used the following `abstract` environment format:

```latex
\begin{abstract}
{title}
{author}
{concentration}
{year}
{PI}
{PI institution}
{mentor 1, institution}
{mentor 2, institution}

% command to index author

main body
\end{abstract}
```

### Python Files

__Again, the Python scripts are only collections of commands/functions and cannot be directly run.__ 

Again, I highly recommend doing this in an interactive environment.

Run `pip install [module name]` to install any dependent modules in Python that you don't have.

* `gen_docs.py` takes in a spreadsheet with author information, title, and body of abstract and generates a list of Google docs with "anyone with link can edit" setting, saving the links to each
    - Gives each abstract submission an ID.
    - Uses `string_funcs.py` to clean up unicode, certain LaTeX reserve keywords, etc.
    - Uses `pyDrive` to access Google Drive (You should understand how Google Drive API authentication works at developers.google.com/console; the module requires `client_secrets.json` authentication file from Google)
    - You should write code to output the list of links and associated emails to send emails using Mail Merge
* `integrate_tex.py` takes in a spreadsheet of author information and the author's Google Doc link. It downloads the title and body of each doc, using `string_funcs.py` to clean up the string, and uses `text_to_abstract.py` to convert to LaTeX code. It should output `abstract.tex` file. 
    - Most likely `main.tex` would fail to compile since `abstract.tex` contains a few LaTeX bugs (since not everyone uses TeX). Those have to be checked manually, unfortunately.
* `gen_pageproof.py` takes in `main.pdf` and `main.idx` (the file that stores author indices) to generate `[ID].pdf`, which contains the abstract of submission `ID`. It uploads PDF files to Google Drive and outputs links for corresponding IDs.
    - The code is haphazardly written on a Saturday night; there should be some major clean up to do.

## Miscellaneous
* The abstract template is due to [this template on overleaf](https://www.overleaf.com/latex/examples/a-basic-conference-abstract-booklet/tkjfcvzgjrnd#.WYZxANPytE4).
* Good luck!




"""
Grab title and text from Google docs and generate code in TeX
The abstract format is

\newenvironment{abstract}[9]{
  \needspace{12\baselineskip}
  \begin{center}
  {{\large\bfseries #1}\par}
  \end{center}

  {\noindent #2 \hfill #3 \par}
  {\noindent #4 \hfill #5 \par}

  \medskip

  {\noindent {#6} \\ {#7}\par}

  \medskip

  {\noindent {#8}\par}
  {\noindent {#9}\par}

  \medskip

}{%
  \bigskip
  \hrule
  \bigskip
}

with usage

Contains function to generate an abstract from the list of fields. The
abstract syntax varies depending on TeX design. We used in 2017
\begin{abstract}
{TITLE}
{AUTHOR}
{CONCENTRATION}
{YEAR}
{PI}
{PI INSTITUTION}
{MENTOR1, INSTITUTION1}
{MENTOR2, INSTITUTION2}

\indexauthor{LAST!FIRST}

ABSTRACT BODY

\end{abstract}

(See text_to_abstract.py)
"""

from pydrive.auth import GoogleAuth # pip install pydrive
from pydrive.drive import GoogleDrive
import pandas as pd
from tqdm import tqdm
from string_funcs import *
from text_to_abstract import *

tqdm.pandas()

# Google Docs API Authentication
# Need `client_secrets.json` (authentication file from Google APIs)
# in directory. See pyDrive documentation
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)


titles = []
contents = []
def get_content(url):
    """
    Scrape google doc for content text and title text. Returns nothing.
    Side effects present.
    """
    idn = url.split('/')[-2]
    fh = drive.CreateFile({'id' : idn})
    content = fh.GetContentString(mimetype='text/plain')
    title = fh['title'].split('___')[-1]
    titles.append(unicode(title))
    contents.append(unicode(content))

# read file with author information and Google doc link
filename = 'abstracts_with_information.csv'
df = pd.read_csv(filename)


# Downloading content and title
temp = df['doc_url'].progress_apply(get_content)
del temp

# adding to spreadsheet
df['body'] = contents
df['title'] = titles


# Converting spreadsheet to TeX

CONC_MAX_LENGTH = 30 # max char length for concentration field

tex_string = ''
last_prog = ''
last_field = ''
prog_dict = {
    'BLISS' : 'Behavioral Laboratory in the Social Sciences (BLISS)',
    'PRISE' : 'Program for Research in Science and Engineering (PRISE)',
    'PCER' : 'Harvard College-Mindich Program in Community-Engaged Research (PCER)',
    'PRIMO' : 'Program for Research in Markets and Organizations (PRIMO)',
    'SHARP' : 'Summer Humanities and Arts Research Program (SHARP)',
    'SURGH' : 'Summer Undergraduate Research in Global Health (SURGH)'
}
for i,row in tqdm(df.iterrows()):
    # Adding chapters and sections to differentiate between
    # programs and research fields
    if row['Program Affiliation'] != last_prog:
        p = prog_dict[row['Program Affiliation']]
        tex_string = tex_string + "\n\\chapter{{{}}}\n".format(p)
        last_prog = row['Program Affiliation']

    if row['Program Affiliation'] == 'PRISE' and row['Research Field'] != last_field:
        tex_string = tex_string \
                     + "\n\\section{{{}}}\n"\
                       .format(row['Research Field'].replace('&','and'))
        last_field = row['Research Field']


    # integrating information of the author
    year = row['Graduation Year']

    try:
        # accommodating 2 PIs
        pi = ' '.join([row['pi_first'], row['pi_last']])
        pi_inst = filter_body(row['pi_inst'])
    except:
        pi = 'UNKNOWN'
        pi_inst = 'UNKNOWN'

    # accommodating 2 PIs
    if not row.isnull()['pi2']:
        pi2 = row['pi2']
        pi2_inst = row['pi2_inst']
        pi = '{} \\\\ {} \n\\smallskip\n'.format(pi,pi_inst)
        pi_inst = '\\noindent {} \\\\ {}'.format(pi2,pi2_inst)


    # concentration, accommodating 2 concentrations
    c = [filter_body(row['conc1'])]
    if not row.isnull()['conc2']:
        c.append(filter_body(row['conc2']))

    # preventing concentration from being too long
    if len(' and '.join(c)) > CONC_MAX_LENGTH: # too long
        if len(c) > 1:
            part1 = c[0]
            part2 = c[1]
        else:
            c = c[0]
            words = c.split(' ')
            part1 = ' '.join(words[:len(words)/2])
            part2 = ' '.join(words[len(words)/2:])
        conc = '{} \\hfill Class of {} \\\\ \\noindent {}'.format(part1, year, part2)
        year = ''
    else:
        conc = ' and '.join(c)


    # Mentors
    mentors = list(pd.Series([row['mentor1'],row['mentor2']]).dropna())
    mentors_insts = list(pd.Series([row['mentor1_inst'],row['mentor2_inst']]).dropna())

    if len(mentors) > len(mentors_insts):
        mentors = []
        mentors_insts = []


    # Author
    try:
        author = ' '.join([row['first'],row['last']])
    except:
        author = row['Full Name']


    # Use text_to_abstract.generate_abstract to generate an abstract
    abstract = generate_abstract(
            title = filter_body(row['title']),
            author = author,
            author_inst = row['College'],
            concentration = conc,
            year = year,
            pi = pi,
            pi_inst = pi_inst,
            mentors = mentors,
            mentors_insts = mentors_insts,
            body = filter_body(row['body'])
    )

    tex_string = tex_string + '\n% {}'.format(row['index']) + '\n{}\n'.format(abstract)

out_filename = 'abstracts.tex'
with open(out_filename, 'w') as f:
    f.write(tex_string)



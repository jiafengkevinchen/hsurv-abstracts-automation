"""
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
"""
WITH_MENTOR = \
'''
\\begin{{abstract}}
{{{0}}}
{{{1}}}
{{{2}}}
{{{3}}}
{{{4}}}
{{{5}}}
{{{6}}}
{{{{\\textit{{Mentor{11}}}\par}} \\noindent
 {7}
}}
{{{8}}}

\indexauthors{{{10}}}

{9}

\end{{abstract}}
'''

WITHOUT_MENTOR = \
'''
\\begin{{abstract}}
{{{0}}}
{{{1}}}
{{{2}}}
{{{3}}}
{{{4}}}
{{{5}}}
{{{6}}}
{{{7}}}
{{{8}}}

\indexauthors{{{10}}}

{9}

\end{{abstract}}
'''


def generate_abstract(title = '',
                      author = '',
                      author_inst = '',
                      concentration = '',
                      year = '',
                      pi = '',
                      pi_inst = '',
                      mentors = [],
                      mentors_insts = [],
                      body = ''):
    first = author.split(' ')[0]
    last = author.split(' ')[-1]
    index_str = '!'.join([last,first])

    if year:
        year = 'Class of {}'.format(year)


    if mentors:
        m1 = ', '.join([mentors[0], mentors_insts[0]])
        if len(mentors) > 1:
            m2 = ', '.join([mentors[1], mentors_insts[1]])
            s = 's'
        else:
            m2 = ''
            s = ''

        return WITH_MENTOR.format(
                title,
                author,
                author_inst,
                concentration,
                year,
                pi,
                pi_inst,
                m1,
                m2,
                body,
                index_str,
                s)
    else:
        return WITHOUT_MENTOR.format(
                title,
                author,
                author_inst,
                concentration,
                year,
                pi,
                pi_inst,
                '',
                '',
                body,
                index_str)

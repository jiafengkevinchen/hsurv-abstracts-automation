"""
String functions to clean up unicode
"""
import re

ucode_replacement_pair = [
    (u'\u2019', "'"),
    (u'\u2018', "'"),
    (u'\ufeff', ''),
    (u'\xe9', "\\'e"),
    (u'\xb5', '$\\mu$'),
    (u'\xf6', '\\"o'),
    (u'\u2014','---'),
    (u'\u201c','``'),
    (u'\u201d',"''"),
    (u'\r','\n'),
    (u'\u2192','$\\to$'),
    (u'\u2013','--'),
    (u'\u03b1','$\\alpha$'),
    (u'\u2265','$\\ge$'),
    (u'\u2026','\\ldots'),
    (u'\xad','-'),
    (u'\u202f',' '),
    (u'\u03b2','$\\beta$'),
    (u'\u02b9',"'"),
    (u'\xe6','ae'),
    (u'\xfc', '\\"u'),
    ('~','$\\sim$'),
    ('\\~','$\\sim$')
]


def replace_unicode(u):
    for uchr,r in ucode_replacement_pair:
        u = u.replace(uchr, r)
    return u


# characters that break tex
# %, $, ~, &, can't handle $
def filter_chars(s):
    re_s = re.sub(r'__+', '', s)
    re_s = re.sub(r'([^\\]|^)([%&])', r'\1\\\2', re_s)
    re_s = re.sub('~',)
    return re_s

callbacks = [replace_unicode, filter_chars]

def filter_body(s):
    for c in callbacks:
        s = c(s)
    return s

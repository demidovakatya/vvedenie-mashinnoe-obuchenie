import os
import pandas as pd

data = 'data'
linkscsv = 'links.csv'

df = pd.read_csv(os.path.join(data, linkscsv), header = None, 
                 names = ['text', 'url', 'tags'])

"""
df.head(2)
                             text                  url        tags
0  Data Structures and Algorit...  https://www.cour...  algorithms
1  MIT 6.046J Introduction to ...  http://ocw.mit.e...  algorithms
"""

tags = df.tags.unique()
"""
tags
array(['algorithms', 'code-editors', 'datasets', 'extra-course-materials',
       'js-libraries', 'latex', 'linalg', 'neural-nets',
       'probability-statistics', 'python', 'r', 'README', 'reddit',
       'spec-recommendations'], dtype=object)
"""

def save_updated_links(df):
    upd = 'updlinks'
    if not os.path.exists(os.path.join(data, upd)):
        os.mkdir(os.path.join(data, upd))
    files = os.listdir(os.path.join(data, upd))
    n = sum([f.startswith('updlinks') for f in files])
    updlinkscsv = os.path.join(data, upd, 'updlinks_{:0>3}.csv'.format(n))
    df.to_csv(updlinkscsv, index = False)
    print('Saved to: %s' % updlinkscsv)

def replace_tags(df):
    save_updated_links(df)                
    replacements = {
                    'code-editors' : 'codeeditors',
                    'extra-course-materials' : 'extramaterials',
                    'js-libraries' : 'javascript',
                    'linalg' : 'linearalgebra',
                    'neural-nets' : 'neuralnets',
                    'README' : 'machinelearning',
                    'reddit' : 'social',
                    'spec-recommendations' : 'extramaterials',
                    }
    df = df.replace({'tags' : replacements})    
    return df


def add_url_base(df):
    save_updated_links(df)                
    df['base'] = [(lambda u: re.sub('https?://|/.*$|www\.', '', u))(u) for u in df.url]
    return df

def add_tag(df, tag, tag_sites):
    save_updated_links(df) 
    for i in df.index:
        try:
            df.base[i]
        except AttributeError:
            df = add_url_base(df)
    if df.base[i] in tag_sites and not tag in df.tags[i].split():
        df.tags[i] += ' {}'.format(tag)
    return df

tags_to_be_added = {
    'mooc' :  [
                'coursera.org', 'datacamp.com', 
                'edx.org', 'ocw.mit.edu', 'stepic.org', 'udacity.com'
              ],
    'social' :  [
                'reddit.com', 'telegram.me', 'vk.com'
                ]               
    }

def add_tags(df, tags_to_be_added):
    tags = list
    for tag, sites in tags_to_be_added.items():
        df = add_tag(df, tag, sites)
    return df

df_ = df.copy()
df = replace_tags(df)
df = add_url_base(df)
df = add_tags(df, tags_to_be_added)

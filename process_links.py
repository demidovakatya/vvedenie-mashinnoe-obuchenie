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
    files = os.listdir(data)
    n = sum([f.startswith('updlinks') for f in files])
    updlinkscsv = os.path.join(data, 'updlinks_{:0>3}.csv'.format(n))
    df.to_csv(updlinkscsv, index = False)
    print('Saved to: %s' % updlinkscsv)

def replace_tags(df):
    replacements = {
                    'code-editors' : 'codeeditors',
                    'extra-course-materials' : 'extramaterials',
                    'js-libraries' : 'javascript',
                    'linalg' : 'linearalgebra',
                    'neural-nets' : 'neuralnets',
                    'README' : 'machinelearning',
                    'spec-recommendations' : 'extramaterials',
                    }
    df = df.replace({'tags' : replacements})    
    save_updated_links(df)                
    return df

df_ = df.copy()
df = replace_tags(df)
save_updated_links(df)

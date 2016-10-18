import os, re
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
                    'probability-statistics' : 'probability statistics',
                    'README' : 'machinelearning',
                    'reddit' : 'social',
                    'spec-recommendations' : 'extramaterials',
                    }
    df = df.replace({'tags' : replacements})    
    return df

def remove_duplicates(df):
    dup_index = df.index[df[['url', 'text']].duplicated(keep = False)]
    duplicates = df.loc[dup_index, :]
    df_ = df.copy()
    df = df.drop(dup_index)

    d = duplicates.merge(duplicates, on = ['text', 'url'], suffixes=('', '_'))
    for i in d.index:
        d.loc[i, 'tags'] = d.loc[i, 'tags'] + ' ' + d.loc[i, 'tags_']
    d.drop(['tags_'], axis = 1, inplace=True)
    d.drop_duplicates(['text', 'url'], inplace=True)
    df = pd.concat([df, d])
    df = df.reset_index()
    return df

def tags_to_list(df):
    tags = df['tags']
    tags_list = [t.split() for t in tags]
    df['tags'] = tags_list
    return df

def add_url_base(df):
    save_updated_links(df)                
    df['base'] = [(lambda u: re.sub('https?://|/.*$|www\.', '', u))(u) for u in df.url]
    return df

def add_tag_for_base(df, tag, tag_sites):
    save_updated_links(df) 
    for i in df.index:
        try:
            df.base[i]
        except AttributeError:
            df = add_url_base(df)
        if df.base[i] in tag_sites:
            df.tags[i].append(tag)
    return df

def add_tag_for_word(df, tag, words):
    for t in df.loc[[len(re.findall(words, t)) > 0 for t in df['text']], 'tags']:
        t.append(tag)
    return df

tags_sites = {
    'mooc' :  [
                'coursera.org', 'datacamp.com', 
                'edx.org', 'ocw.mit.edu', 'stepic.org', 'udacity.com'
              ],
    'social' :  [
                'reddit.com', 'telegram.me', 'vk.com'
                ],
    'video' : [ 'youtube.com']              
    }

tags_words = {
    'statistics' : 'статистик|statistics',
    'probability' : 'вероятнос|probability'
}
def add_tags(df, tags_sites):#, tags_words):
    tags = list
    for tag, sites in tags_sites.items():
        df = add_tag_for_base(df, tag, sites)
    
    # for tag, words in tags_words.items():
    #     df = add_tag_for_word(df, tag, words)
    
    return df


df_ = df.copy()
df = replace_tags(df)
df = remove_duplicates(df)
df = tags_to_list(df)
df = add_url_base(df)
df = add_tags(df, tags_sites)

for t in df.loc[[len(re.findall('статистик|statistics', t)) > 0 for t in df['text']], 'tags']:
    t.append('statistics')

for t in df.loc[[len(re.findall('вероятнос|probability', t)) > 0 for t in df['text']], 'tags']:
    t.append('probability')

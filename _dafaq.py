import os
import re
import json
import pandas as pd

md = 'md'
data = 'data'
if not data in os.listdir():
    os.mkdir(data)
rawlinescsv = 'raw_lines.csv'
rawlinesjson = 'raw_lines.json'


def get_files():
    files = [file for file in os.listdir(md) if file.endswith('md')]
    return files
files = iter(get_files())

tags = ['tag_' + re.sub('\.md', '', f) for f in files]
#df = pd.DataFrame(columns = ['raw', 'link', 'text', 'otherlinks', 'title', 'description'] + tags)
df = pd.DataFrame()


i = 0
while True:
#try:
    file = next(files)
    #except StopIteration:
    #    print('This is the end.')
    #    break
    tag = re.sub('\.md', '', file)
    with open(os.path.join(md, file)) as f:
        lines = [line.strip() for line in f.readlines()]
    for line in lines:
        df.loc[i, 'raw'] = line
        df.loc[i, 'tag_{}'.format(tag)] = 1
        i += 1
        # lines += [line for line in get_lines_from_md(file)]# if
        # line_is_valid(line)]

df = df[df['raw'] != '']
df = df[[not r.startswith(('# ', '##', '**', '[!', '<', '_')) for r in df['raw']]]
df = df[[not (re.sub('(\-)+', '', r) == '') for r in df['raw']]]

def extract_urls(line):
    urls = re.findall('https?://[^\)\s]*', line)
    return urls

def get_first_link(urls):
    try:
        link = urls[0]
    except IndexError:
        link = ''
    return link

df['urls']   = [extract_urls(line) for line in df['raw']]
df['link']   = [get_first_link(urls) for urls in df['urls']]

def get_text(line):
    # remove urls
    text = re.sub('\(https?://[^\)]*\)', '', line)
    ## remove urls in link texts
    #text = re.sub('\[https?://|/?\]', '', text)
    # remove http/https
    text = re.sub('https?://', '', text)
    ## remove www
    #text = re.sub('www\.', '', text)

    # remove brackets
    text = re.sub('\[|\]', '', text)
    # remove punctuation
    text = re.sub('^[\*\+] |[\.;,]$', '', text)
    # remove emoji
    text = re.sub(':[\w_]*: ', '', text)
    # make quotes safe
    text = re.sub('"', '\'', text)
    text = re.sub('\'+', '\'', text)

    # remove extra spaces
    text = re.sub('\s+', ' ', text)
    text = text.strip()

    return text

texts = [get_text(line) for line in df['raw']]
df = pd.concat([df, pd.Series(texts, name = 'text', index = df.index)], axis = 1)

#raw = list(df['raw'])
#for i, line in enumerate(raw):
#    #print(line)
#    text = get_text(line)
#    df['text'].iloc[i] = text

#remove invalid lines
notlist = df[[not r.startswith(('* ', '+ ')) for r in df['raw']]]
nolink = df[[len(urls) == 0 for urls in df['urls']]]

df = df[[r.startswith(('* ', '+ ')) for r in df['raw']]]
df = df[[re.sub('\* \[.+]\(/.+.md\)', '', line) != '' for line in df['raw']]]
df = df[[re.sub('\* .*:', '', line) != '' for line in df['raw']]]



def replace_tags(df):
    replacements = {
                    'tag_code-editors' : 'tag_coding',
                    'tag_extra-course-materials' : 'tag_extra',
                    'tag_js-libraries' : 'tag_js',
                    'tag_neural-nets' : 'tag_neuralnets',
                    'tag_probability-statistics' : 'tag_prob',
                    'tag_README' : 'tag_ml',
                    'tag_reddit' : 'tag_social',
                    'tag_spec-recommendations' : 'tag_extra_',
                    }
    df = df.rename_axis(replacements, axis = 1)
    return df

df = replace_tags(df)

#df = df.drop('tag_extramaterials', axis = 1)
df_ = df.copy()
df['extra'] =  df[['tag_extra', 'tag_extra_']].max(axis = 1)
df = df.drop('tag_extra_', axis = 1)

def add_url_base(df):
    df['base'] = [(lambda u: re.sub('https?://|/.*$|www\.', '', u))(u) for u in df['link']]
    return df

df = add_url_base(df)

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

def add_tag_for_base(df, tag, tag_sites):
    for i in df.index:
        try:
            df.base[i]
        except AttributeError:
            df = add_url_base(df)
        if df.base[i] in tag_sites:
            df.loc[i, 'tag_' + tag] = 1
    return df

def add_tag_pdf(df):
    for i in df.index:
        if df.loc[i, 'link'].endswith('.pdf'):
            df.loc[i, 'tag_pdf'] = 1
    return df

def add_tags(df, tags_sites):
    tags = list
    for tag, sites in tags_sites.items():
        df = add_tag_for_base(df, tag, sites)

    # for tag, words in tags_words.items():
    #     df = add_tag_for_word(df, tag, words)
    df = add_tag_pdf(df)
    return df

#remove duplicates
dup_index = df.index[df['raw'].duplicated(keep = False)]
duplicates = df.loc[dup_index, :]

for i in dup_index:
    occurences = df.index[df.raw == df.loc[i, 'raw']]
    df.loc[i] = df.loc[occurences, :].max(axis = 0)

df.drop_duplicates('raw', inplace = True)

df = df[['link', 'text', 'urls', 'raw' ,
        'tag_r', 'tag_algorithms', 'tag_extra', 'tag_prob', 'tag_ml',
        'tag_datasets', 'tag_neuralnets', 'tag_social', 'tag_latex',
        'tag_code', 'tag_js', 'tag_python', 'tag_linalg', 'tag_video', 'tag_mooc', 'tag_pdf']]
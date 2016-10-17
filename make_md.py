import json, os
from tags import load_tags_from_json
from process_json import load_links_from_json

data = 'data'
src = 'src'

def get_ids(links, tag = 'everything'):
    if tag != 'everything':
        ids = [k for k, v in links['tags'].items() if tag in v]
    else:
        ids = list(links['tags'].keys())
    return ids

def make_md_for_tag(links, tag = 'everything'):
    ids = get_ids(links, tag)
    formatstr = '* {} [link]({})'
    txt = [formatstr.format(links['text'][i] , links['url'][i]) for i in ids]

    md_file = os.path.join(src, tag + '.md')
    with open(md_file, 'w') as f:
        try:
            title = tags[tag]['title']
            description = tags[tag]['description']
        except KeyError:
            title = 'everything'
            description = 'All links.'
        f.write('# {}\n\n'.format(title))
        f.write('{}\n\n'.format(description))
        f.writelines('\n'.join(txt))
        print('Created: {}'.format(md_file))

def make_md(links, tags):
    for tag in list(tags.keys()):
        make_md_for_tag(links, tag)
    # create md file with everything
    make_md_for_tag(links)

links = load_links_from_json()
tags = load_tags_from_json()
make_md(links, tags)

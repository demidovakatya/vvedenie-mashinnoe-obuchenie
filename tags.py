import json, os
#from process_json import load_links_from_json 

data = 'data'
src = 'src'

def load_tags_from_json(jsonfile = 'tags.json'):
    with open(os.path.join(src, jsonfile), 'r') as f:
        tags = json.loads(f.read())
    return tags

def save_tags_to_json(tags_dict, jsonfile = 'tags.json'):
    with open(os.path.join(src, jsonfile), 'w') as f:
        json.dump(tags, f)

def get_unique_tags(links):
    all_tags = [t for tag in list(links['tags'].values()) for t in tag]
    unique_tags = list(set(all_tags))
    return unique_tags

def update_tags_dict(tag_list, tags = {}):
    #tags = {}
    for i, tag in enumerate(tag_list):
        tags[tag] = {
                        'name' : tag, 'id' : i,
                        'title' : tag.title(), 
                        'description' : '{}.'.format(tag.title())
                    }
    return tags

def add_titles(tags):
    titles = {
                'statistics' : 'Statistics',
                'mooc' : 'Mooc',
                'python' : 'Python',
                'linearalgebra' : 'Linear Algebra',
                'r' : 'R',
                'extramaterials' : 'Extra Materials',
                'machinelearning' : 'Machine Learning',
                'codeeditors' : 'Code Editors',
                'video' : 'Video',
                'probability' : 'Probability',
                'algorithms' : 'Algorithms',
                'javascript' : 'Javascript',
                'social' : 'Social',
                'datasets' : 'Datasets',
                'latex' : 'Latex',
                'neuralnets' : 'Neural Nets'
             }
    for t in list(tags.keys()):
        tags[t]['title'] = titles[t]
    return tags

def add_descriptions(tags):
    descriptions = {
                'statistics' : 'Statistics.',
                'mooc' : 'MOOCs.',
                'python' : 'Python.',
                'linearalgebra' : 'Linear algebea.',
                'r' : 'R.',
                'extramaterials' : 'Extra materials.',
                'machinelearning' : 'Machine learning.',
                'codeeditors' : 'Code editors.',
                'video' : 'Video.',
                'probability' : 'Probability.',
                'algorithms' : 'Algorithms.',
                'javascript' : 'Javascript.',
                'social' : 'Social.',
                'datasets' : 'Datasets.',
                'latex' : 'Latex.',
                'neuralnets' : 'Neural nets.'
             }
    for t in list(tags.keys()):
        tags[t]['description'] = descriptions[t]
    return tags

def load_links_from_json(jsonfile = 'sample.json'):
    with open(os.path.join(src, jsonfile)) as f:
        links = json.loads(f.read())
    return links
links = load_links_from_json()

try:
    tags = load_tags_from_json()
except FileNotFoundError:
    tags = {}

#tags = update_tags_dict(get_unique_tags(links))
#tags = add_descriptions(tags)
#tags = add_titles(tags)

unique_tags = get_unique_tags(links)
new_tags = [tag for tag in unique_tags if tag not in list(tags.keys())]
tags = update_tags_dict(new_tags, tags)

save_tags_to_json(tags)

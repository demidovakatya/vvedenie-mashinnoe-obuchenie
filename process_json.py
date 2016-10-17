import json, os
from tags import load_tags_from_json

data = 'data'
src = 'src'

def save_df_to_json(df, jsonfile = 'sample.json'):
    if not os.path.exists(src):
        os.mkdir(src)
    df.to_json(os.path.join(src, jsonfile))

def load_links_from_json(jsonfile = 'sample.json'):
    with open(os.path.join(src, jsonfile)) as f:
        links = json.loads(f.read())
    return links


save_df_to_json(df)

links = load_links_from_json()
tags = load_tags_from_json()

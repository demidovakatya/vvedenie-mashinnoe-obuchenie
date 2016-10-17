import os, re

def get_files():
    files = [file for file in os.listdir('./src') if file.endswith('md')]
    return files

def get_lines(file):
    with open(os.path.join('src', file)) as f:
        lines = [line.strip() for line in f.readlines()]
    return lines

def line_is_valid(line):
    is_valid = (line != '') and not (line.startswith('#'))
    try:
        s, e = re.search('https?://[^)]*', line).span()
    except AttributeError:
        is_valid = False # has no link
    return is_valid

def get_link_from_line(line):
    s, e = re.search('https?://[^)]*', line).span()
    link = line[s:e]
    return link

def get_text_from_line(line):
    # remove urls
    text = re.sub('\(https?://[^\)]*\)', '', line)
    # remove punctuation
    text = re.sub('^[\*\+] |\[|\]|[\.;,]$', '', text)
    text = re.sub(':[\w_]*:', '', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub('"', '\'', text)
    text = text.strip()
    return text

files = get_files()

data = 'data'
if not data in os.listdir():
    os.mkdir(data)

all_lines = []
with open(os.path.join(data, 'links.csv'), 'w') as f:
    f.flush()
for file in files:
    tags = re.sub('\.md', '', file)
    # if tags == 'README':
    #     tags = 'machinelearning'
    # if tags == 'spec-recommendations':
    #     tags = 'specialization'

    lines = [line for line in get_lines(file) if line_is_valid(line)]
    all_lines += lines

    links = []
    for line in lines:
        item = (get_text_from_line(line), 
                get_link_from_line(line), 
                tags)
        links.append(item)
        with open(os.path.join(data, 'links.csv'), 'a') as f:
            f.write('"%s","%s","%s"\n' % item)

with open(os.path.join(data, 'lines.csv'), 'w') as f:
    f.write('\n'.join(all_lines))

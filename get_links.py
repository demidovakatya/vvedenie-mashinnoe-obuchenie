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
    text = re.sub('^\* |\[|\]|\(https?://[^\)]*\)', '', line)
    return text

files = get_files()

lines = []
for file in files:
    lines += [line for line in get_lines(file) if line_is_valid(line)]

with open('./lines.csv', 'w') as f:
    for line in lines:
        f.write(line + ';\n')

links = []
for line in lines:
    item = (get_link_from_line(line), get_text_from_line(line))
    links.append(item)
    with open('./links.csv', 'w') as f:
        f.write('' + item[0] + '\t' + item[1] + '\n')



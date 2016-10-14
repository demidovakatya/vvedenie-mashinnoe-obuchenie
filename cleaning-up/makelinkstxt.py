import os
import re

def get_files():
    if os.path.abspath(os.curdir).endswith('/cleaning-up'):
        os.chdir('..')
    files = [file for file in os.listdir('.') if file.endswith('md')]
    return files


def get_lines(files):
    lines = []

    for f in files:
        with open(f) as file:
            for line in file:
                lines.append(line.strip())
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
lines = get_lines(files)

len_lines = len (lines)
print("%s lines in %s files were read" % (len_lines, len(files)))

print("Removing invalid lines...")
lines = [line for line in lines if line_is_valid(line)]
print("%s invalid lines were removed" % (len_lines - len(lines)))
len_lines = len (lines)

with open('cleaning-up/lines.csv', 'w') as file:
    for line in lines:
        file.write(line + ';\n')

links = []
for line in lines:
    item = (get_link_from_line(line), get_text_from_line(line))
    links.append(item)
    with open('cleaning-up/links.csv', 'w') as file:
        for item in links:
            file.write('' + item[0] + '\t' + item[1] + '\n')



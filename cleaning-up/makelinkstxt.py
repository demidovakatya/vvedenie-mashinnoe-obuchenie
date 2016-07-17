import os
import re

os.chdir('..')
files = [file for file in os.listdir() if file.endswith('md')]

lines = []

for f in files:
    with open(f) as file:
        for line in file:
            lines.append(line.strip())

len_lines = len (lines)
print("%s lines in %s files were read" % (len_lines, len(files)))

print("Removing empty lines...")
lines = [line for line in lines if not line == '']
print("%s empty lines were removed" % (len_lines - len(lines)))

links = []
for line in lines:  
    if len(re.findall(r"\(.*\)", line)) != 0:
        text = re.sub(r"\(.*\)|\[|\]|\* |;|\.$|:.*:|\+", "", line).strip()
        link = re.sub(r"\(|\)", "", re.findall(r"\(.*\)", line)[0])
        links.append([text, link])

print("Saving to file...")
with open('links.txt', 'w') as file:
    for item in links:
        file.write('"' + item[0] + '","' + item[1] + '";\n')

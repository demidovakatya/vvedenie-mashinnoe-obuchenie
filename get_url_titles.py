import os
from bs4 import BeautifulSoup
import requests
data = 'data'
urlstxt = 'urls.txt'

def get_urls(file = urlstxt):
    with open(os.path.join(data, file)) as f:
        urls = [line.strip() for line in f.readlines()]
    return urls

urls = iter(get_urls())
urlstitlestxt = 'urlstitles.txt'

urls_left = iter([
'https://yandexdataschool.ru/edu-process/courses'
])
while True:
    try:
        u = next(urls)
    except StopIteration:
        u = next(urls_left)
    print(u)
    this = {'url' : u, 'title' : '', 'desc' : ''}
    if u.lower().endswith('.pdf') or u.lower().endswith('.png'):
        with open(os.path.join(data, urlstitlestxt), 'a') as f:
            f. write(str(this))
            f. write('\n')
        continue
    else:
        try:
            r = requests.get(u, timeout = 5.0)
        except:
            with open(os.path.join(data, urlstitlestxt), 'a') as f:
                f. write(str(this))
                f. write('\n')
            continue
            continue

        soup = BeautifulSoup(r.text)
        
        # metas = soup.find_all(name = 'meta')
        try:
            this['title'] = soup.find(attrs={'property': 'og:title'}).get('content')
        except:
            try:
                this['title'] = soup.find(name = 'title').get('content')
            except:
                pass
        
        try:
            this['desc']  = soup.find(attrs={'property': 'og:description'}).get('content')
        except:
            try:
                this['desc']  = soup.find(name = 'meta', attrs={'name': 'description'}).get('content')
            except:
                pass
        try:   
            this['url'] = soup.find(attrs={'property': 'og:url'}).get('content')
        except:
            pass

        with open(os.path.join(data, urlstitlestxt), 'a') as f:
            f. write(str(this))
            f. write('\n')

# for u in urls:
    # r = requests.get(u)

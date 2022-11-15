import bs4 as bs
import requests
import os
import re

URL = 'https://www.sacred-texts.com/hin/sbe48/index.htm'
BASE_URL = 'https://www.sacred-texts.com/hin/sbe48/'

content = requests.get(URL).content
soup = bs.BeautifulSoup(content, 'html.parser')


def filter(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text)


hr = soup.findAll('hr')[1]
print(hr)
ADHYAYA = ''
PADA = ''
next = hr.find_next_sibling()
while next:
    try:
        if next.name == 'hr':
            break
        if next.name == 'h3':
            if next.text.endswith('Adhyâya') or next.text.endswith('Adyaya'):
                ADHYAYA = next.text
            elif next.text.endswith('Pâda'):
                PADA = next.text
        if next.name == 'a' and len(ADHYAYA) > 0 and len(PADA) > 0:
            print(ADHYAYA, PADA)
            try:
                link = next['href']
            except:
                next = next.find_next_sibling()
                continue
            print(next['href'])
            try:
                c = requests.get(BASE_URL + next['href']).content
            except:
                print('Error')
                next = next.find_next_sibling()
                continue
            # print(c)
            s = bs.BeautifulSoup(c, 'html.parser')

            text = ''
            h = s.find('hr')
            next_sibling = h.find_next_sibling()

            while next_sibling:
                if next_sibling.name == 'hr':
                    break
                current_text = next_sibling.text.strip()
                if len(current_text) > 0:
                    text += filter(current_text).strip() + '\n'
                next_sibling = next_sibling.find_next_sibling()

            titleDirExists = os.path.isdir(os.path.join(ADHYAYA, PADA))
            if not titleDirExists:
                os.makedirs(os.path.join(ADHYAYA, PADA))
            with open(os.path.join(ADHYAYA, PADA, next.text + '.txt'), 'w') as f:
                f.write(text)
    except:
        pass
    next = next.find_next_sibling()


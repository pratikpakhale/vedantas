import bs4 as bs
import requests
import os
import re

URL = 'https://www.sacred-texts.com/hin/sbe38/index.htm'
BASE_URL = 'https://www.sacred-texts.com/hin/sbe38/'

content = requests.get(URL).content
soup = bs.BeautifulSoup(content, 'html.parser')


def filter(text):
    return re.sub(r'[^\x00-\x7F]+', ' ', text)


hr = soup.findAll('hr')[3]
print(hr)
FOLDER = ''
next = hr.find_next_sibling()
while next:
    try:
        if next.name == 'hr':
            break
        if next.name == 'h3':
            FOLDER = next.text
        if next.name == 'a' and len(FOLDER) > 0:
            print(FOLDER)
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
            h = s.findAll('hr')[2]
            next_sibling = h.find_next_sibling()

            while next_sibling:
                if next_sibling.name == 'hr':
                    break
                current_text = next_sibling.text.strip()
                if len(current_text) > 0:
                    text += filter(current_text).strip() + '\n'
                next_sibling = next_sibling.find_next_sibling()

            titleDirExists = os.path.isdir(FOLDER)
            if not titleDirExists:
                os.makedirs(FOLDER)
            with open(os.path.join(FOLDER, next.text + '.txt'), 'w') as f:
                f.write(text)
    except:
        pass
    next = next.find_next_sibling()


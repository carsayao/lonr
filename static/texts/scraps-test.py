import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

URL = "https://carsayao.github.io"
path = urlparse(URL)
title = re.search(r"[a-z].*[full-transcript]", str(path.path))
print("title: ", title)
r = requests.get(URL)
#print("r.content: ", r.content)

soup = BeautifulSoup(r.content, 'html.parser')
raw_transcript = soup.find('div', attrs = {'class':'aboutme'})
print("raw_transcript: ", raw_transcript)

p = raw_transcript.find_all('p')
text = ""
for p in raw_transcript.find_all('p'):
    text += p.get_text()
print(text)
print(p.prettify())


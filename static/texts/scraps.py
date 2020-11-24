import os, re, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


flinks = "scraps-links.txt"

def get_urls():
    url = "https://scrapsfromtheloft.com/stand-up-comedy-scripts/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_html = soup.find('ul', attrs={'class': 'display-posts-listing'})
    fetched_urls = []
    # Extract urls from list
    fetched_urls = [li.find('a').get('href') for li in raw_html.find_all('li')]
    # for li in raw_html.find_all('li'):
    #     fetched_urls.append(li.find('a').get('href'))
    # Read in what's already been written
    with open(flinks) as f:
        done = f.readlines()
    # Only add to file what's not already in there
    new_urls = [f for f in fetched_urls if not any(f in d for d in done)]
    # for f in fetched_urls:
    #     if not any(f in d for d in done):
    #         new_urls.append(f)
    # Also check our blocklist
    with open("scraps-block-links.txt") as f:
        block_urls = f.readlines()
    new_urls = [n for n in new_urls if not any(n in b for b in block_urls)]

    # Write these new links to file
    print(f"{len(new_urls)} new links")
    with open(flinks, 'a') as f:
        f.writelines('\n'.join(new_urls))
        f.write('\n')

def get_transcript(url):
    path = urlparse(url)
    url_path = re.search(r"[a-z].*[full-transcript]", str(path.path)).string.split('/')[1:-1]
    date = '-'.join(url_path[:3])
    title = '-'.join(url_path[3].split('-')[2:])
    name = '-'.join(url_path[3].split('-')[:2])
    fname = f"{name}/{'_'.join([name, date, title])}.txt"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_html = soup.find('div', attrs = {'class':'elementor-widget-theme-post-content'})
    text = ""
    for p in raw_html.find_all('p'):
        text += f"{p.get_text()}\n"
    
    write_transcript(name, date, title, fname, text)

def write_transcript(name, date, title, fname, text):
    if not os.path.exists(name):
        os.makedirs(name)
    if os.path.isfile(fname):
        print(f"[!] {fname} already exists")
    else:
        with open(fname, 'x') as f:
            f.write(text)
        print(f"[✓] {fname} written")


get_urls()

with open(flinks) as f:
    urls = f.readlines()
urls = [i.strip() for i in urls]
for u in urls:
    get_transcript(u)
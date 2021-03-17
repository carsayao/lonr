# Links not in block list or scraps-links.txt will be downloaded and pickled.

import os, re, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd


flinks = "scraps-links.txt"
fpkl = "./transcripts.pkl"

def get_urls():
    """ Get urls, check against what's already been scraped and blocked """
    url = "https://scrapsfromtheloft.com/stand-up-comedy-scripts/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # div of list containing article elements
    raw_html = soup.find('div', attrs={'class': 'elementor-posts-container'})
    # raw_html = soup.find('ul', attrs={'class': 'display-posts-listing'})
    fetched_urls = []
    # Extract urls from list
    fetched_urls = [article.find('a').get('href') for article in raw_html.find_all('article')]
    # fetched_urls = [li.find('a').get('href') for li in raw_html.find_all('li')]

    # Read in what's already been written
    with open(flinks, 'a') as f:
        #import pdb; pdb.set_trace()
        # Check if flinks exists
        if os.stat(flinks).st_size != 0:
            done = f.readlines()
        else:
            done = []
    # Only add to file what's not already in there
    new_urls = [f for f in fetched_urls if not any(f in d for d in done)]
    # print(f"Not in list:")
    # [print(n) for n in new_urls]

    # Also check our blocklist
    with open("scraps-block-links.txt") as f:
        block_urls = f.readlines()
    new_urls = [n for n in new_urls if not any(n in b for b in block_urls)]
    print(f"{len(new_urls)} new links to download")
    [print(n) for n in new_urls]

    # TODO: test
    # new_urls = new_urls[:2]

    # Write these new links to file
    with open(flinks, 'a') as f:
        f.writelines('\n'.join(new_urls)) if os.stat(flinks).st_size == 0 else f.writelines('\n'+'\n'.join(new_urls))

    return new_urls

def get_transcript(url):
    """ Get transcript from url. Parse out name, act, date uploaded. """
    path = urlparse(url)
    url_path = re.search(r"[a-z].*[full-transcript]", str(path.path)).string.split('/')[1:-1]
    date = '-'.join(url_path[:3])
    title = '-'.join(url_path[3].split('-')[2:])
    name = '-'.join(url_path[3].split('-')[:2])
    fname = f"{name}/{'_'.join([name, date, title])}.txt"

    print(name, title)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_html = soup.find('div', attrs = {'class':'elementor-widget-theme-post-content'})

    # TODO: this is some test text
    # text = "content"

    text = ""
    for p in raw_html.find_all('p'):
        text += f"{p.get_text()}\n"
    
    return [name, date, title, fname, text]

def write_transcript(name, fname, text):
    """ """
    if not os.path.exists(name):
        os.makedirs(name)
    if os.path.isfile(fname):
        print(f"[!] {fname} already exists")
    else:
        with open(fname, 'x') as f:
            f.write(text)
        print(f"[✓] {fname} written")

def save(transcripts):
    """ Pickle the data """
    [write_transcript(t[0], t[3], t[4]) for t in transcripts]
    # Put now transcripts to be written into a dataframe
    #df = pd.DataFrame(transcripts,
    #                  columns=['name', 'date', 'title', 'fname', 'text'])
    # If we already have a pickle, concatenate df onto it
    #if os.path.isfile(fpkl):
    #    df = pd.concat([pd.read_pickle(fpkl), df], ignore_index=True, sort=False)
    #df.to_pickle(fpkl)
    #print("New transcripts serialized.")


urls = get_urls()
if len(urls) == 0:
    print("No new transcripts to download.")
    sys.exit()
# Remove both leading and trailing whitespaces
urls = [i.strip() for i in urls]
# Turn into list comprehension of all transcripts
print("Downloading...")
transcripts = [get_transcript(u) for u in urls]
print("Writing new transcripts to disk...")
save(transcripts)

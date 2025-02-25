import queue
import re
from typing import List

import requests
from bs4 import BeautifulSoup

EMAIL_REGEX = r"[A-Za-z]\w*([-\_.]?\w+)*@\w+([-\._]\w+)*"
HASTHAGE_REGEX = r"#."
AT_REGEX = r"@\w*"
TELEPHONE_REGEX = ""

def get_data(url: str) -> List[str]:
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    emails = re.findall(EMAIL_REGEX, response.text)
    hashtags = re.findall(HASTHAGE_REGEX, response.text)
    ats = re.findall(AT_REGEX, response.text)

    title = soup.title.string if soup.title else 'No title found'

    links = []
    for link in soup.find_all('a'):
        target_url = link.get('href')
        if target_url is None:
            continue
        if target_url.startswith('http'):
            links.append(target_url)
    return links, title, emails, hashtags, ats


def crawl(
    start_url: str,
    max_documents: int,
) -> List[str]:

    q = queue.Queue()
    q.put(start_url)
    visited = set()

    saved_info = []

    while (not q.empty()) and (len(visited) < max_documents):
        url = q.get()
        if url in visited:
            continue
        visited.add(url)

        print(f'Now visiting: {url}')
        links, title, emails, hashtags, ats = get_data(url)
        saved_info.append((title, url, emails, hashtags, ats))
        for link in links:
            if link not in visited:
                q.put(link)
    return visited, saved_info

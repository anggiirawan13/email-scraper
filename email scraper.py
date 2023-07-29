from collections import deque
from bs4 import BeautifulSoup

import re
import requests
import urllib.parse

userURL = str(input('[+] Enter URL : '))

if not userURL.startswith('https'):
    userURL = f'https://{userURL}'

urls = deque([userURL])
scrapedURLS = set()
emails = set()
count = 0
limit = int(input('[+] Enter limit search : '))

try:
    while True:
        count += 1
        if count > limit:
            break

        url = urls.popleft() if len(urls) > 0 else ''
        scrapedURLS.add(url)
        parts = urllib.parse.urlsplit(url)
        baseURL = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        print(f'{count} Process\t: {url}')

        try:
            resp = requests.get(url)
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        newEmails = set(re.findall(r'[\w\d\.\-+_]+@\w+\.+[\w\.]+', resp.text, re.I))
        emails.update(newEmails)

        soup = BeautifulSoup(resp.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = baseURL + link
            elif not link.startswith('http'):
                link = path + link
            
            if not link in urls and not link in scrapedURLS:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Close!')

print('\nDone!')
print(f'\n{len(emails)} emails found!\n==================================================')

for mail in emails:
    print('  ' + mail)

print('\n')

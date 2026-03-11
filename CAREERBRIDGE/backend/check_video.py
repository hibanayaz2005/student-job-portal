import urllib.request
import re

videos = [
    'LHBE6Q9XlzI',
    'rfscVS0vtbw',
    'kqtD5dpn9C8',
    'r-uOLxNrNk8',
    'ZyhVh-qRZPA',
    'M7lc1UVf-VE'
]

for vid in videos:
    url = f'https://www.youtube.com/embed/{vid}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        m = re.search(r'"status":"([^"]+)"', html)
        m2 = re.search(r'"reason":"([^"]+)"', html)
        status = m.group(1) if m else 'UNKNOWN'
        reason = m2.group(1) if m2 else 'No reason'
        print(f'{vid}: {status} - {reason}')
    except Exception as e:
        print(f'{vid}: {e}')

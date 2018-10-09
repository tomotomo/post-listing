
#!/usr/bin/env python3
#coding: utf-8

import sys
import argparse
import urllib.request
import urllib.parse
import json
import csv
import time

'''
# Usage

```
python3 zd2csv.py -u https://isaax.zendesk.com -l ja -o isaax-camp..csv
```

'''

def request(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        sys.exit(e.reason)
    except urllib.error.URLError as e:
        sys.exit(e.reason)

ap = argparse.ArgumentParser()
ap.add_argument('-u','--url', required=True, help='https://isaax.zendesk.com')
ap.add_argument('-l','--language', required=True, help='en-us, ja')
ap.add_argument('-o','--output', help='File name. Example: xshell-blog.csv')

args = vars(ap.parse_args())
filename = args['output']
if filename == None:
    filename = args['url'].replace('http://', '').replace('https://', '').replace('/', '_')
filename = filename+'_'+args['language']+'.csv'

print('Request...')

response = request(args['url']+'/api/v2/help_center/'+args['language']+'/articles.json')

data = json.loads(response.read().decode('utf8'))
# print(pages['count'])
print('Find {} pages ;)'.format(data['count']))

print('Write...')

with open(filename, 'w') as f:
    fp = csv.writer(f)
    fp.writerow(['id','title','link'])

    while True:
        for post in data['articles']:
            print('id:{}'.format(post['id']))
            row = [ post['id'], post['title'], post['html_url'] ]
            fp.writerow(row)

        if data['next_page'] == None:
            break
        
        time.sleep(1)
        res = request(data['next_page'])
        data = json.loads(res.read().decode('utf8'))

print('Success. {}'.format(filename))

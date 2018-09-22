#!/usr/bin/env python3
#coding: utf-8

import sys
import argparse
import urllib.request
import urllib.parse
import json
import csv
import time

def request(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        sys.exit(e.reason)
    except urllib.error.URLError as e:
        sys.exit(e.reason)

ap = argparse.ArgumentParser()
ap.add_argument('-u','--url', required=True, help='https://xshell.io')
ap.add_argument('-o','--output', help='File name. Example: xshell-blog.csv')
                
args = vars(ap.parse_args())
args = vars(ap.parse_args())
filename = args['output']
if filename == None:
    filename = args['url'].replace('http://', '').replace('https://', '').replace('/', '_')
filename = filename+'.csv'

print('Request...')
url = args['url']+'/wp-json/wp/v2/posts?page={}'

response = request(args['url']+'/wp-json/wp/v2/posts')

pages = int(response.headers.get('X-WP-TotalPages'))
print('Find {} pages ;)'.format(pages))

print('Write...')

with open(filename, 'w') as f:
    fp = csv.writer(f)
    fp.writerow(['slug','id','status','title','link'])
    for i in range(pages):
        time.sleep(1)
        res = request(url.format(i+1))
        posts = json.loads(res.read().decode('utf8'))

        for post in posts:
            print('id:{} {}'.format(post['id'], post['slug']))
            row = [ post['slug'], post['id'], post['status'],
                post['title']['rendered'], post['link'] ]
            fp.writerow(row)

print('Success. {}'.format(filename))

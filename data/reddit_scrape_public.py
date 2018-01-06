import urllib2
import json
import time
import numpy as np
from pandas import Series, DataFrame
import pandas as pd

# by /u/<PutYourUserNameHere>)

hdr = {'User-Agent': 'osx:r/relationships.multiple.results:v1.0 (by /u/<PutYourUserNameHere>)'}
url = 'https://www.reddit.com/r/relationships/top/.json?sort=top&t=all&limit=100'
req = urllib2.Request(url, headers=hdr)
text_data = urllib2.urlopen(req).read()
data = json.loads(text_data)
data_all = data.values()[1]['children']

print len(data_all)

while (len(data_all) <= 900):
    time.sleep(2)
    last = data_all[-1]['data']['name']
    print last
    url = 'https://www.reddit.com/r/relationships/top/.json?sort=top&t=all&limit=100&after=%s' % last
    req = urllib2.Request(url, headers=hdr)
    text_data = urllib2.urlopen(req).read()
    data = json.loads(text_data) 
    data_all += data.values()[1]['children']
    print len(data_all)

print len(data_all)

article_title = []
article_flairs = []
article_date = []
article_comments = []
article_score = []

for i in range(0, len(data_all)):
    article_title.append(data_all[i]['data']['title'])
    article_flairs.append(data_all[i]['data']['link_flair_text'])
    article_date.append(data_all[i]['data']['created_utc'])
    article_comments.append(data_all[i]['data']['num_comments'])
    article_score.append(data_all[i]['data']['score'])

rel_df = DataFrame({'Date': article_date,
                    'Title': article_title,
                    'Flair': article_flairs,
                    'Comments': article_comments,
                    'Score': article_score})
rel_df = rel_df[['Date', 'Title', 'Flair', 'Comments', 'Score']]

print rel_df[:5]

rel_df.to_csv('out.csv', encoding='utf-8')
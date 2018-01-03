import csv
import glob
from datetime import datetime

import json_lines
from dateutil.parser import parse
from textblob import TextBlob

filename = 'tweets*.csv'
sentiments = open('results.csv', 'wb')
path = "tweets1*"

for filename in glob.glob(path):
    with open(filename, 'rb') as f:
        for item in json_lines.reader(f):
            testimonial = TextBlob(item['text'])
            date = parse(item['created_at'].encode('utf-8'))
            sentiments.write(str(date.date()) + ' ' + str(date.time()) + ',' + str(testimonial.sentiment.polarity) + '\n')

sortedData = csv.reader(open('results.csv','r'))
sortedData = sorted(sortedData, key = lambda row: datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"))

writer = csv.writer(open('resultsSorted.csv', 'w'))
writer.writerows(sortedData)
import glob
import json_lines
from dateutil.parser import parse
from textblob import TextBlob
import re

path = "FlumeData.*"

for filename in glob.glob(path):
    resultName = 'sentiments-' + filename + '.csv'
    sentiments = open(resultName, 'wb')
    with open(filename, 'rb') as f:
        for item in json_lines.reader(f):
            tweet = item['text']
            if re.search('eur', tweet, re.IGNORECASE):
                testimonial = TextBlob(tweet)
                date = parse(item['created_at'].encode('utf-8'))
                sentiments.write(
                    str(date.date()) + ' ' + str(date.time()) + ',' + str(testimonial.sentiment.polarity) + ',' + str(
                        testimonial.sentiment.subjectivity) + '\n')

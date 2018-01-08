import csv
import glob
from datetime import datetime
import pandas as pd
import json_lines
from dateutil.parser import parse
from textblob import TextBlob

path = "FlumeData.*"

for filename in glob.glob(path):
    resultName = 'result-' + filename + '.csv'
    sentiments = open(resultName, 'wb')
    with open(filename, 'rb') as f:
        for item in json_lines.reader(f):
            testimonial = TextBlob(item['text'])
            # if testimonial.sentiment.polarity != 0:  # do I need this?
            date = parse(item['created_at'].encode('utf-8'))
            sentiments.write(
                str(date.date()) + ' ' + str(date.time()) + ',' + str(testimonial.sentiment.polarity) + '\n')
        sortedData = csv.reader(open(resultName, 'r'))
        sortedData = sorted(sortedData, key=lambda row: datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"))
        df = pd.DataFrame(sortedData, columns=['date', 'sentiment'])
        df.to_csv('dataframe.csv')
        df = pd.read_csv('dataframe.csv', parse_dates=['date'], index_col='date')
        agg = df.resample('30S').mean()
        agg.to_csv('resampled-' + resultName)
        print resultName + 'done'

import csv
import glob
import json_lines
import pandas as pd
from dateutil.parser import parse
from textblob import TextBlob

path = "FlumeData.*"

for filename in glob.glob(path):
    resultName = 'sentiments-' + filename + '.csv'
    sentiments = open(resultName, 'wb')
    with open(filename, 'rb') as f:
        for item in json_lines.reader(f):
            testimonial = TextBlob(item['text'])
            date = parse(item['created_at'].encode('utf-8'))
            sentiments.write(
                str(date.date()) + ' ' + str(date.time()) + ',' + str(testimonial.sentiment.polarity) + '\n')
        sortedData = csv.reader(open(resultName, 'r'))
        sortedData = sorted(sortedData)
        df = pd.DataFrame(sortedData, columns=['date', 'sentiment'])
        df.to_csv('dataframe-' + filename + '.csv')
        try:
            df = pd.read_csv('dataframe-' + filename + '.csv', dayfirst=True, parse_dates=['date'],
                             index_col='date', skiprows=[1])
            agg = df.resample('30Min').mean()
            agg.to_csv('resampled-' + resultName + '.csv')
            print resultName + 'done'
        except TypeError:
            print resultName + ' TypeError'
        except ValueError:
            print resultName + ' ValueError'

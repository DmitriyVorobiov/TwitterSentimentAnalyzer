import csv
import glob
import pandas as pd
import numpy as np

path = "sentiments*"

for filename in glob.glob(path):
    with open(filename, 'rb') as f:
        sortedData = csv.reader(open(filename, 'r'))
        sortedData = sorted(sortedData)
        df = pd.DataFrame(sortedData, columns=['date', 'sentiment', 'subjectivity'])
        df.to_csv('dataframe-' + filename + '.csv')
        try:
            df = pd.read_csv('dataframe-' + filename + '.csv', dayfirst=True, parse_dates=['date'],
                             index_col='date', skiprows=[1])
            agg = df.resample('30Min').agg({'mx': np.mean, 'dx': np.std})
            agg.drop(agg.columns[[0, 3]], axis=1, inplace=True)
            agg.to_csv('resampled-' + filename + '.csv')
            print filename + 'done'
        except TypeError:
            print filename + ' TypeError'
        except ValueError:
            print filename + ' ValueError'

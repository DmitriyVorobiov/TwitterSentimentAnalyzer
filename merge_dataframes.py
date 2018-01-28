import re
import csv
import glob
import pandas as pd
import numpy as np

sortedData = csv.reader(open('result_eur.csv', 'r'))
sortedData = sorted(sortedData)
sortedDatac = csv.reader(open('EURUSD30.csv', 'r'))
sortedDatac = sorted(sortedDatac)

df = pd.DataFrame(sortedData, columns=['date', 'usd_sent_mean', 'usd_subj_mean', 'usd_sent_std', 'usd_subj_std'])
dfc = pd.DataFrame(sortedDatac, columns=['date', 'open', 'high', 'low', 'close', 'vol'])

df.set_index('date').join(dfc.set_index('date'))

df.to_csv('merged.csv')

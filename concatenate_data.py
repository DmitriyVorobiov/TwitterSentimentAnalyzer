import csv
import glob
import re

path = "resampled-*"

result = open('result.csv', 'wb')
for filename in glob.glob(path):
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            if not re.search('mx', str(line), re.IGNORECASE):
                if not re.search('sentiment', str(line), re.IGNORECASE):
                    if not re.search('date', str(line), re.IGNORECASE):
                        result.write(','.join(line) + '\n')

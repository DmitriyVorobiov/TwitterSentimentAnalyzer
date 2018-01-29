import csv
import pandas as pd

sortedDataEur = csv.reader(open('result_eur.csv', 'r'))
sortedDataEur = sorted(sortedDataEur)
sortedDataCurrency = csv.reader(open('EURUSD30.csv', 'r'))
sortedDataCurrency = sorted(sortedDataCurrency)
sortedDataUsd = csv.reader(open('result_usd.csv', 'r'))
sortedDataUsd = sorted(sortedDataUsd)
sortedDataAurum = csv.reader(open('XAUUSD30.csv', 'r'))
sortedDataAurum = sorted(sortedDataAurum)

# dfEur = pd.DataFrame(sortedDataEur, columns=['date', 'eur_sent_mean', 'eur_subj_mean', 'eur_sent_std', 'eur_subj_std'])
# dfUsd = pd.DataFrame(sortedDataUsd, columns=['date', 'usd_sent_mean', 'usd_subj_mean', 'usd_sent_std', 'usd_subj_std'])
#
# df = dfEur.set_index('date').join(dfUsd.set_index('date'))
#
# df.to_csv('merged.csv')


# sortedDataEurUsd = csv.reader(open('merged.csv', 'r'))
# sortedDataEurUsd = sorted(sortedDataEurUsd)
#
# dfEurUsd = pd.DataFrame(sortedDataEurUsd, columns=['date', 'eur_sent_mean', 'eur_subj_mean', 'eur_sent_std', 'eur_subj_std', 'usd_sent_mean', 'usd_subj_mean', 'usd_sent_std', 'usd_subj_std', 'eurusd_open', 'eurusd_high', 'eurusd_low', 'eurusd_close', 'eurusd_vol'])
# dfCurrency = pd.DataFrame(sortedDataCurrency, columns=['date', 'open', 'high', 'low', 'close', 'vol'])
#
# df = dfEurUsd.set_index('date').join(dfCurrency.set_index('date'))


sortedDataEurUsdCurrency = csv.reader(open('merged.csv', 'r'))
sortedDataEurUsdCurrency = sorted(sortedDataEurUsdCurrency)

dfEurUsdCurency = pd.DataFrame(sortedDataEurUsdCurrency, columns=['date', 'eur_sent_mean', 'eur_subj_mean', 'eur_sent_std', 'eur_subj_std', 'usd_sent_mean', 'usd_subj_mean', 'usd_sent_std', 'usd_subj_std', 'eurusd_open', 'eurusd_high', 'eurusd_low', 'eurusd_close', 'eurusd_vol'])
dfCurrencyAur = pd.DataFrame(sortedDataAurum, columns=['date', 'aur_open', 'aur_high', 'aur_low', 'aur_close', 'aur_vol'])

df = dfEurUsdCurency.set_index('date').join(dfCurrencyAur.set_index('date'))

df.to_csv('merged.csv')
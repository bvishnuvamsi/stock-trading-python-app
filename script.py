import requests
import os
import csv
from dotenv import load_dotenv
load_dotenv()
import time


POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
#print(POLYGON_API_KEY)

LIMIT = 1000

URL = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'


response = requests.get(URL)
#print(response.json())

tickers = []

data = response.json()
#print(data.keys())

#print(data['next_url'])

for ticker in data['results']:
    tickers.append(ticker)
print(len(tickers))

while 'next_url' in data:
    print('requesting next page', data['next_url'])
    time.sleep(15)
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()
    #print(data)
    print(len(tickers))
    for ticker in data['results']:
        tickers.append(ticker)

print(len(tickers))

fields = [
    'ticker',
    'name',
    'market',
    'locale',
    'primary_exchange',
    'type',
    'active',
    'currency_name',
    'cik',
    'composite_figi',
    'share_class_figi',
]

ouput_csv = 'tickers.csv'

with open(ouput_csv , mode = 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', restval='')
    writer.writeheader()
    for row in tickers:
        writer.writerow(row)

print(f"Wrote {len(tickers)} rows to {ouput_csv}")
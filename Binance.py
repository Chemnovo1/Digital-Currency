import requests
import time
import pandas as pd

BASE_ENDPOINT = r'https://api.binance.com'


def get_kline(symbol, interval, start_time=None, end_time=None, limit=1000):
    url = BASE_ENDPOINT + '/api/v1/klines'
    payload={
        'symbol': symbol,
        'interval': interval
    }
    if start_time:
        payload['start_time'] = start_time
    if end_time:
        payload['end_time'] = end_time
    if limit:
        payload['limit'] = limit
    response = requests.get(url, payload)
    print('Getted data from', response.url)
    return response.json()


if __name__ == '__main__':
    # for data in get_kline('BTCUSDT', '1d'):
        # print(data)
    ls = get_kline('XRPUSDT', '1h')
    for data in ls:
        timearray = time.localtime(data[0] / 1000)
        data[0] = time.strftime('%Y-%m-%d %H:%M:%S',timearray)
        timearray = time.localtime(data[6] / 1000)
        data[6] = time.strftime('%Y-%m-%d %H:%M:%S', timearray)
    df = pd.DataFrame(ls)
    df.columns = ['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume',\
                     'Number of trades','Taker buy base asset volume','Taker buy quote asset volume',\
                     'Ignore']
    df.to_csv('D:\\xrpusdt hour.csv', sep=',', header=True, index=True)


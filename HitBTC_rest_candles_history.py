# -*- coding: utf-8 -*-

import requests
import time
import json
import pandas as pd


def candles():
    # 函数可以获取K线图数据，详见https://api.hitbtc.com/?python#candles
    # Available values: '1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M'
    url = r'https://api.hitbtc.com/api/2/public/candles/{}'.format(symbol)
    params = {'limit': 1000, 'period': 'H1'}
    # limit为单次获取信息数量（最大值1000），默认值为100
    # 时间周期可选择：M1 (1 minute), M3, M5, M15, M30, H1, H4, D1, D7, 1M (1 month)，默认值是 M30 (30 minutes)。
    response = requests.get(url, params)
    print('Getted data from', response.url)     # 打印获取数据的具体地址
    return response.json()

if __name__ == '__main__':
    symbol = 'zecusd'
    # 交易币对，格式小写如zecusd，这里特别注意：HitBTC网没有法币交易，只有它用usd代表泰达币usdt，所以这里不是美元的意思
    ls = candles()
    df = pd.DataFrame(ls, columns=['timestamp', 'open', 'close', 'max', 'min', 'volume', 'volumeQuote'])
    # HitBTC是一家英国网站，返回的时间不是时间戳，而直接是格林威治时间的正常格式，这里需要注意一下
    print(df)        # 如需要直接写入csv文件，就把下面语句的#去掉
    # df.to_csv('D:\\HitBTC_{}_hour_history.csv'.format(symbol), sep=',', header=True, index=None)
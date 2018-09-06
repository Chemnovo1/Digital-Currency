import requests
import json
import time
import pandas as pd

def candles(end):
    # 函数可以获取K线图数据，详见https://docs.bitfinex.com/v2/reference#rest-public-candles
    url = r'https://api.bitfinex.com/v2/candles/trade:1h:tBTCUSD/hist'
    # url中可设置获取的交易对币、时间周期。币对格式例：tBTCUSDT
    # 可选择的时间间隔有：'1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M'
    params = {'limit': 1000, 'end': end}
    # limit表示单次获取数据量，最大限值是1000；start、end为起始结束时间戳，单位为ms
    response = requests.get(url, params)
    print('Getted data from', response.url)     # 打印获取数据的具体地址
    return response.json()

if __name__ == '__main__':
    ls = candles(None)      # ls跟ls2是一样的，都是为了获取数据，分开设是为了用ls设置列标题，后面用ls2做循环
    ls2 = candles(None)
    for data in ls:
        timearray = time.localtime(data[0] / 1000)
        data[0] = time.strftime('%Y-%m-%d %H:%M:%S', timearray)
    df = pd.DataFrame(ls)
    df.columns = ['Open time', 'Open', 'Close', 'High', 'Low', 'Volume']
    print(df)       # 如需要直接写入csv文件，就把下面语句的#去掉
    # df.to_csv('D:\\Bitfinex_btcusd_day_history.csv', sep=',', header=True, index=None)
    while(1):
        try:
            timestamp = ls2[999][0] - 86400000
            # 这个公式要特别注意！按天减去86400000，按小时减去3600000；另外，ls2后面第一个[]中数值=limit-1
            ls2 = candles(timestamp)
            df2 = pd.DataFrame(ls2)
            for i in range(1000):       # range()中的值=limit
                df2.loc[i, 0] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(df2.loc[i, 0] / 1000))
            print(df2)       # 如需要直接写入csv文件，就把下面语句的#去掉
            # df2.to_csv('D:\\Bitfinex_btcusd_day_history.csv', mode='a', sep=',', header=None, index=None)
        except:
            break
    print('程序结束')    # 更新的时候参数start统一设为上次末尾时间点
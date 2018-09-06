# -*- coding: utf-8 -*-

import requests
import time
import json
import pandas as pd


def candles(since):
    # 函数可以获取K线图数据，详见https://www.zb.cn/i/developer
    url = r'http://api.zb.cn/data/v1/kline'
    params = {'market': symbol, 'type': period, 'since': since, 'size': limit}
    # limit为单词获取数据条数，最大限值是1000，默认也为1000条
    response = requests.get(url, params)
    print('Getted data from', response.url)     # 打印获取数据的具体地址
    return response.json()

if __name__ == '__main__':
    # 在函数外设定好参数，交易币对格式为zb_usdt
    symbol = 'zb_usdt'
    # 时间周期可选：1min 3min 5min 15min 30min 1day 3day 1week 1hour 2hour 4hour 6hour 12hour，格式就是前面这样
    period = '1hour'
    limit = 1000
    dic = candles(1199116800000)      # since参数不让取0，since最小值我建议从1199116800000（2008-01-01）取就可以，单位ms
    timestamp = dic['data'][-1][0]
    for ls in dic['data']:
        ls[0] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ls[0] / 1000))
    df = pd.DataFrame(dic['data'])
    df.columns = ['Timestamp', 'Opening Price', 'High Price', 'Low Price', 'Closing Price', 'Volume']
    print(df)       # 如需要直接写入csv文件，就把下面语句的#去掉
    # df.to_csv('D:\\ZB_{}_hour_history.csv'.format(symbol), sep=',', header=True, index=None)
    while(1):
        try:
            dic = candles(timestamp+3600000)
            timestamp = dic['data'][-1][0]
            for ls in dic['data']:
                    ls[0] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ls[0] / 1000))
            df = pd.DataFrame(dic['data'])
            print(df)       # 如需要直接写入csv文件，就把下面语句的#去掉
            # df.to_csv('D:\\ZB_{}_hour_history.csv'.format(symbol), mode='a', sep=',', header=None, index=None)
        except:
            break
    print('程序结束')    # ZB网返回的数据可能不出现正进行的时间周期，比如我11点半获数据，最后一条采集的数据就是10-11点的

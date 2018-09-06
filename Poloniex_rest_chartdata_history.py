import requests
import json
import time
import pandas as pd

def chartdata():
    # 函数可以获取K线图数据，详见https://www.poloniex.com/support/api/
    url = r'https://poloniex.com/public'          # 改：时间间隔、交易对
    params = {'command': 'returnChartData', 'currencyPair': 'BTC_XRP', 'start': 0, 'end': 9999999999, 'period': 1800}
    # 没有超过单次获取数据最大限额量，所以可以一次性全部获取下来；交易币对要写成BTC_LTC的形式，均大写中间加下划线
    # 可选时间周期均以s为单位，可选值为300, 900, 1800, 7200, 14400, 86400，所以爬不了1小时（没有3600）
    response = requests.get(url, params)
    print('Getted data from', response.url)     # 打印获取数据的具体地址
    return response.json()

if __name__ == '__main__':
    ls = chartdata()
    for dic in ls:
        dic['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dic['date']))
    df = pd.DataFrame(ls, columns=['date', 'high', 'low', 'open', 'close', 'volume', 'quoteVolume', 'weightedAverage'])
    print(df)       # 如需要直接写入csv文件，就把下面语句的#去掉
    # df.to_csv('D:\\Poloniex_xrpbtc_halfhour_history.csv', sep=',', header=True, index=None)

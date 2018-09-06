# -*- coding: utf-8 -*-

from websocket import create_connection
import time
import json
import pandas as pd

def get_kline():
    # 函数可以获取K线图数据，详见https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md
    symbol = 'btcusdt'      # 交易币对在这里改，格式大写，例：BTCUSDT
    interval = '1m'     # 数据的时间周期，可以设置的参数有：1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M
    # 可以设置的时间单位有：m -> minutes; h -> hours; d -> days; w -> weeks; M -> months
    url = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(symbol, interval)
    # 这是Binance的websocket API的基础地址，不用动

    while(1):
        # 连接网络
        while (1):
            try:
                ws = create_connection(url)
                break
            except:
                print('connect ws error,retry...')
                time.sleep(5)
        # 解析数据
        while (1):
            try:
                content = ws.recv()
                dic = json.loads(content)
                if dic['k']['x'] == True:       # 这里判断获取的K线是否是该时间段的末尾，True代表是结尾，所以获取
                    dic['k']['t'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dic['k']['t']/1000))
                    dic['k']['T'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int((dic['k']['T']/1000))))
                    # 获取每条数据时间戳，起始为000结尾，结束为999结尾，所以后面一条的处理加上了int函数
                    df = pd.DataFrame(dic['k'], index=['1'])
                    print(df)       # 如需要直接写入csv文件，就把下面语句的#去掉
                    # df.to_csv('D:\\Binance_btcusdt_min_update.csv', mode='a', header=None, index=None)
                else:
                    continue
            except:
                break

if __name__ == '__main__':
    # 设置数据列标题
    dic = {'1': 'Kline start time', '2': 'Kline close time', '3': 'Symbol', '4': 'Interval', '5': 'First trade ID',
           '6': 'Last trade ID', '7': 'Open price', '8': 'Close price', '9': 'High price', '10': 'Low price',
           '11': 'Base asset volume', '12': 'Number of trades', '13': 'Is this kline closed',
           '14': 'Quote asset volume',
           '15': 'Taker buy base asset volume', '16': 'Taker buy quote asset volume', '17': 'Ignore'}
    df = pd.DataFrame(dic, index=['1'])     # index是为了构建DataFrame设置的，没有作用
    print(df)       # 如需要直接写入csv文件，就把下面语句的#去掉
    # df.to_csv('D:\\Binance_btcusdt_min_update.csv', header=None, index=None)
    get_kline()

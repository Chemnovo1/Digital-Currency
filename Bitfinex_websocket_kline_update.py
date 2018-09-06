# -*- coding: utf-8 -*-

from websocket import create_connection
import time
import json
import pandas as pd

def get_kline():
    # 函数可以获取K线图数据，详见https://docs.bitfinex.com/v2/reference#ws-public-candle
    url = "wss://api.bitfinex.com/ws/2"
    while(1):
        # 连接网络
        while (1):
            try:
                ws = create_connection(url)
                break
            except:
                print('connect ws error,retry...')
                time.sleep(5)

        ws.send('{ "event": "subscribe",  "channel": "candles",  "key": "trade:1m:tBTCUSD" }')
        # 解析数据，交易对和时间周期形式如：trade:1m:tBTCUSD
        # 可选时间周期有：1m(one minute),5m,15m,30m,1h(one hour),3h,6h,12h,1D(one day)7D,14D,1M(one month)
        while (1):
            try:
                content = ws.recv()
                data = json.loads(content)
                print(data)
                if type(data) == dict:
                    continue
                else:
                    print(data)
            except:
                break

if __name__ == '__main__':
    get_kline()

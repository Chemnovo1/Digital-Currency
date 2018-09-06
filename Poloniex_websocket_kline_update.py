# -*- coding: utf-8 -*-

from websocket import create_connection
import time
import json
import pandas as pd

def get_kline():
    # 函数可以获取K线图数据，详见https://www.poloniex.com/support/api/
    url = "wss://api2.poloniex.com"
    ws = create_connection(url)
    ws.send('{"command": "subscribe", "channel": "USDT_BTC"}')
    while(1):
        content = ws.recv()
        dic = json.loads(content)
        print(dic)

if __name__ == '__main__':
    get_kline()
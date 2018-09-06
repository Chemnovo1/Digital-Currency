# -*- coding: utf-8 -*-

from websocket import create_connection
import gzip
import time
import json
import pandas as pd

if __name__ == '__main__':
    # 函数可以获取K线图数据，详见https://github.com/huobiapi/API_Docs/wiki/WS_api_reference
    while(1):
        # 此部分为连接API网址，连接失败会等5秒钟再连
        while(1):
            try:
                ws = create_connection("wss://api.huobi.pro/ws")
                break
            except:
                print('connect ws error,retry...')
                time.sleep(5)

        # 订阅KLine数据，用到"sub"指令，后面的"id"不用管
        tradeStr = """{"sub": "market.btcusdt.kline.1min","id": "id10"}"""      # 在这里改交易对和时间周期
        # 交易对形式小写如：btcusdt；可选时间周期有：1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year

        ws.send(tradeStr)
        while(1):
            try:
                compressData = ws.recv()
                result = gzip.decompress(compressData).decode('utf-8')
                dic = json.loads(result)
                if result[:7] == '{"ping"':
                    ts = result[8:21]
                    pong = '{"pong":' + ts + '}'
                    ws.send(pong)
                    ws.send(tradeStr)
                    time.sleep(2)
                else:
                    print(dic)
            except:
                break
import requests
import time
import pandas as pd

BASE_ENDPOINT = r'https://api.binance.com'  # 这是Binance的restful API的基础地址，不用动

def get_kline(symbol, interval, startTime=None, endTime=None, limit=1000):
    # 函数可以获取K线图数据，详见https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
    url = BASE_ENDPOINT + '/api/v1/klines'
    payload={
        'symbol': symbol,           # 交易币对，格式为 BTCUSDT
        'interval': interval,       # 数据的时间周期，可选值有1m、3m、5m、15m、30m、1h、2h、4h、6h、8h、12h、1d、3d、1w、1M
        # m -> minutes; h -> hours; d -> days; w -> weeks; M -> months
        'startTime': startTime,     # 起始时间，时间戳（单位ms）
        'endTime': endTime,         # 结束时间，时间戳（单位ms）
        'limit': limit              # 单次获取信息数量（最大值1000）
    }
    response = requests.get(url, payload)
    print('Getted data from', response.url)     # 打印获取数据的具体地址
    return response.json()


if __name__ == '__main__':
    ls = get_kline('XRPUSDT', '1h')     # 使用函数获取数据，后面的参数可以设置
    for data in ls:     # 将从网站下载的时间戳统一换成日期时间格式
        timearray = time.localtime(data[0] / 1000)
        data[0] = time.strftime('%Y-%m-%d %H:%M:%S', timearray)
        timearray = time.localtime(data[6] / 1000)
        data[6] = time.strftime('%Y-%m-%d %H:%M:%S', timearray)
    df = pd.DataFrame(ls)
    df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',\
                     'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume',\
                     'Ignore']
    print(df)       # 如需要直接写入csv文件，就把下面语句的#去掉
    # df.to_csv('D:\\Binance_xrpusdt_day_history.csv', mode='a', sep=',', header=True, index=None)


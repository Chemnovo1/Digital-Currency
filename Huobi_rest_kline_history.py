import json
import urllib
import urllib.parse
import urllib.request
import requests
import pandas as pd
import time

MARKET_URL = "https://api.huobi.pro"        # 基本地址不用变
def get_kline(symbol, period, size):
    """
    :param symbol
    :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size: 可选值： [1,2000]
    :return:
    """
    # 函数可以获取K线图数据，详见https://github.com/huobiapi/API_Docs/wiki/REST_api_reference#get-markethistorykline-获取K线数据
    params = {'symbol': symbol,
              'period': period,
              'size': size}
    # 三个参数可以设置：交易对格式小写，例：btcusdt；时间周期可选值：1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
    # size为单次获取数据条数，取值范围[1,2000]，默认值为150

    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)

def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    response = requests.get(url, postdata, headers=headers, timeout=5)
    try:

        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" % (response.text, e))
        return

if __name__ == '__main__':
    start = get_kline('ltcusdt', '60min', 2000)
    for i in range(2000):       # range()中的数=size
        start['data'][i]['id'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start['data'][i]['id']))
    df = pd.DataFrame(start['data'])
    df = df.reindex(columns=['id', 'open', 'close', 'high', 'low', 'amount', 'vol', 'count'])
    print(df)       # 如需要直接写入csv文件，就把下面语句的#去掉
    # df.to_csv('D:\\Huobi_{}_hour_history.csv'.format(symbol), sep=',', header=True, index=None')
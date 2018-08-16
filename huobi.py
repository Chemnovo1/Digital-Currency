import json
import urllib
import urllib.parse
import urllib.request
import requests
import pandas as pd
import time

# 获取KLine
MARKET_URL = "https://api.huobi.pro"
def get_kline(symbol, period, size):
    """
    :param symbol
    :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size: 可选值： [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

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
    start = get_kline('xrpusdt','60min',500)
    t = time.time()
    df = pd.DataFrame(start['data'][0],index = [time.strftime('%Y-%m-%d %H:%M', time.gmtime(t))])
    for i in range(1,500):
        t = t - 3600.0
        df2 = pd.DataFrame(start['data'][i], index=[time.strftime('%Y-%m-%d %H:%M',time.gmtime(t))])
        df = df.append(df2,sort=True)
    print(df)
    # df.to_csv('D:\\xrpusdt 小时.csv', sep=',', header=True, index=True)
import requests
import csv
from bs4 import BeautifulSoup


def get_history_data(since, until, curr_id, interval_sec='Daily'):
    payload = dict(
        curr_id=curr_id,
        smlID='25609848',
        header=None,
        st_date=since,
        end_date=until,
        interval_sec=interval_sec,
        sort_col='date',
        sort_ord='DESC',
        action='historical_data'
    )
    ajax_url = r'https://cn.investing.com/instruments/HistoricalDataAjax'
    ua = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
         r'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': ua,
    }
    return requests.post(ajax_url, headers=headers, data=payload).text


def html_to_csv(html):
    soup = BeautifulSoup(html, 'lxml')
    headers = [dom.get_text() for dom in soup.table.thead.tr.find_all('th')]
    rows = [headers]
    row = []
    for val in soup.find_all('td'):
        row.append(val.get_text())
        if len(row) == len(headers):
            rows.append(row)
            row = []
    with open('xlmusd.csv', 'w', encoding='gbk', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerows(rows)


html_to_csv((get_history_data('2010/01/01', '2018/08/12', '1061451')))

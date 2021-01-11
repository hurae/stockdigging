# Base package for Crawler
import functools
import json
import re
import time
import status_code
import tushare as ts
import pandas as pd
from digging_utils import *
from bs4 import BeautifulSoup as bf
from threading import Thread
import requests

# address of database manager
db_addr = 'http://db.local/'


# todo: complete saver function
# Universal DB saver
def save(df: pd.DataFrame, op_code: int):
    """
    index_info:
    ["ts_code","name","market","publisher","category","base_date","base_point","list_date"]
    ["000001.SH","上证指数","SSE","中证公司","综合指数","19901219",100.0,"19910715"]

    stock_info:
    ["ts_code","symbol","name","area","industry","market","list_date"]
    ["688788.SH","688788","科思科技","深圳","通信设备","科创板","20201022"]

    index_daily:
    stock_daily:
    ["ts_code","trade_date","open","high","low","close","pre_close","change","pct_chg","vol","amount"]
    ["600187.SH","20210106",2.4,2.4,2.34,2.35,2.41,-0.06,-2.4896,122540.51,28972.52]

    final_msg:
    {'operate_code': 8, 'data': '[["000001.SH","20210106",3550.8767,3530.9072,3556.8022,3513.1262,3528.6767,22.2,0.6291,370230926.0,521799529.8000000119],["000001.SH","20210105",3528.6767,3492.1912,3528.6767,3484.7151,3502.9584,25.7183,0.7342,407995934.0,568019462.2000000477],["000001.SH","20210104",3502.9584,3474.6793,3511.6554,3457.2061,3473.0693,29.8891,0.8606,380790800.0,523367700.8000000119]]'}    """

    json_string = df.to_json(orient='values', force_ascii=False)
    route = "/set/info"
    final_msg = {
        "operate_code": op_code,
        "data": json_string
    }
    final_msg_poster(final_msg, route)
    Thread(target=final_msg_poster, args=(final_msg, route)).start()
    print(op_code, json_string[:120] + "........")
    print(json.dumps(final_msg)[:150] + ".........")
    print(df)
    print("------------------------------------------------------")


# post with error detection and unlimited retry
def final_msg_poster(params, route):
    # todo: error handler
    while True:
        r = requests.post(url=db_addr + route, json=params, timeout=(3, 5))
        json_obj = json.loads(r.text)
        if r.status_code == 200 and json_obj['error_code'] == 0 and json_obj['data'][0] is str:
            break
        else:
            print(json_obj['error_message'])
            time.sleep(2)
    return json_obj


# wrapper of tushare sdk, adapted for our needs
class Tushare:
    pro_1 = ts.pro_api('85c250f231ccbe95aa63350b365d892161ecf18810ff7b93e35fc1f4')
    pro_2 = ts.pro_api('6d2175719e5b5d27c8b7f3ae83402bbf806979bcd53ec6500808c31a')
    pro_list = [pro_1, pro_2]
    op_code = status_code.OpCode()
    error_code = status_code.ErrorCode()

    # cal means calendar
    cal = {}

    def __init__(self):
        pd.set_option('display.max_columns', 100)
        pd.set_option('display.max_rows', 10)
        pd.set_option('display.width', 200)
        self.get_trade_cal()

    def get_trade_cal(self):
        df = self.pro_2.trade_cal(start_date=get_year(), end_date=get_today(), fields=["cal_date", "is_open"])
        for x in df.values.tolist():
            self.cal[x[0]] = True if x[1] == 1 else False

        return self.cal

    # get all basic info and save it or return only tscode dataframe
    def get_basic_info(self, is_index: bool = True, only_tscode: bool = False):
        fields = ['ts_code'] if only_tscode else []
        if is_index:
            df = self.pro_2.index_basic(fields=fields)
            code = self.op_code.SET_INDEX_INFO
        else:
            df = self.pro_1.stock_basic(fields=fields)
            code = self.op_code.SET_STOCK_INFO

        if not only_tscode:
            save(df, op_code=code)
        else:
            return df

    # get today's index number or stock price
    def get_price_today(self, ts_code: str, is_index: bool):
        today = get_today()
        if self.cal[today]:
            self.get_price_daily(ts_code, today, today, is_index)
            self.get_price_daily(ts_code, today, today, is_index)
        else:
            print(f'Today({today}) is not open.')

    # get the last year's index number history or stock price history
    def get_price_year(self, ts_code: str, is_index: bool):
        year_ago = get_year()
        today = get_today()
        self.get_price_daily(ts_code, year_ago, today, is_index)
        self.get_price_daily(ts_code, year_ago, today, is_index)

    # base api wrapper of tushare for index number and stock price
    def get_price_daily(self, ts_code: str, start_date: str, end_date: str, is_index: bool):
        if is_index:
            df = self.pro_2.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            code = self.op_code.SET_INDEX_DAILY
        else:
            # todo: replace with pro_api
            df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
            code = self.op_code.SET_STOCK_DAILY
        save(df, op_code=code)


# base class for basic crawler operation
class CrawlerBase:
    session = requests.session()
    only_today = True

    def __init__(self, headers, cookies):
        self.img_re = re.compile(r'\[(\w+)\]')
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)
        self._daily = Daily

    # proxy for class Daily
    def __getattr__(self, item):
        if item == 'get_tscode_list':
            return functools.partial(getattr(self._daily, item), self=self._daily)

    # main entrance of Xueqiu crawler
    def set_base(self, only_today):
        self.only_today = only_today

    # set http header
    def set_header(self, headers):
        self.session.headers.update(headers)

    # get response and decode it
    def get_url_content(self, url, headers, params=None):
        if params is None:
            # r = self.session.get(url, headers=headers, timeout=(3, 5))
            f = functools.partial(self.session.get, url, headers=headers, timeout=(3, 5))
        elif isinstance(params, dict):
            # r = self.session.post(url, data=params, headers=headers, timeout=(3, 5))
            f = functools.partial(self.session.post, url, data=params, headers=headers, timeout=(3, 5))
        else:
            raise TypeError
        # todo: error handler
        RETRY_LIMIT = 10
        while True:
            if RETRY_LIMIT < 0:
                break
            r = f()
            if r.status_code == 200:
                return r.text
            else:
                RETRY_LIMIT -= 1
                time.sleep(2)

    # get decoded response and parse it as json
    def get_parsed_json_response(self, url, headers, params=None):
        decoded_text = self.get_url_content(url, headers, params)
        if decoded_text is None:
            return {}
        return json.loads(decoded_text)

    # parse the document and extract the wanted element
    def get_target_element(self, selector, html_text):
        html_parsed = bf(html_text, "lxml")
        return html_parsed.findall(selector)

    # extract all label a, and return an iterator which yield a tuple (text, href) of one label each time
    def extract_label_a(self, html_text):
        a_list = self.get_target_element('a', html_text)
        return map(lambda x: (x.text, x.attrs['href']), a_list)

    # extract all label p, and return an iterator which yield inner text of one label each time
    def extract_label_p(self, html_text):
        p_list = self.get_target_element('p', html_text)
        # find all str inside of a label p, and connect them with symbol ","
        return map(lambda p_item: ','.join(filter(lambda content_item: isinstance(content_item, str),
                                                  p_item.contents)
                                           ),
                   p_list)

    # extract all label img, and return an iterator which yield one alt attrs of one label each time
    def extract_label_img(self, html_text):
        img_list = self.get_target_element('img', html_text)
        return map(lambda x: self.img_re.findall(r'\[(\w+)\]', x.attrs['alt'])[0] if 'alt' in x.attrs else '',
                   img_list)

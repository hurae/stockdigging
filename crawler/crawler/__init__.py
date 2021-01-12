# Base package for Crawler
import functools
import json
import random
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
    {'operate_code': 8, 'data': '[["000001.SH","20210106",3550.8767,3530.9072,3556.8022,3513.1262,3528.6767,22.2,0.6291,370230926.0,521799529.8000000119],["000001.SH","20210105",3528.6767,3492.1912,3528.6767,3484.7151,3502.9584,25.7183,0.7342,407995934.0,568019462.2000000477],["000001.SH","20210104",3502.9584,3474.6793,3511.6554,3457.2061,3473.0693,29.8891,0.8606,380790800.0,523367700.8000000119]]'}
    """

    if df.empty:
        print("Trying to saving empty, skipped.")
        return

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
    # todo: response parse
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
    pro_api = {
        True: pro_1,
        False: pro_2
    }
    api_flag = True
    api = pro_api[api_flag]
    all_api_used = 0

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
        if only_tscode:
            df_stock = self.pro_1.stock_basic(fields=['ts_code'])
            df_index = self.pro_2.index_basic(fields=['ts_code'])
            df = pd.merge(df_index, df_stock, how='outer', on='ts_code')
            return df

        # is_index is only valid when only_tscode == False
        if is_index:
            df = self.pro_2.index_basic()
            code = self.op_code.SET_INDEX_INFO
        else:
            df = self.pro_1.stock_basic()
            code = self.op_code.SET_STOCK_INFO

        save(df, op_code=code)

    # get today's index number or stock price
    def get_price_today(self, ts_code: str, is_index: bool):
        today = get_today()
        if self.cal[today]:
            self.get_price_daily(ts_code, today, today, is_index)
        else:
            print(f'Today({today}) is not open.')

    # get the last year's index number history or stock price history
    def get_price_year(self, ts_code: str, is_index: bool):
        year_ago = get_year()
        today = get_today()
        self.get_price_daily(ts_code, year_ago, today, is_index)

    # base api wrapper of tushare for index number and stock price
    def get_price_daily(self, ts_code: str, start_date: str, end_date: str, is_index: bool):
        adj = None
        if is_index:
            # 500 times/min
            # df = ts.pro_bar(ts_code=ts_code, asset='E', adj=None, start_date=start_date, end_date=end_date)
            code = self.op_code.SET_INDEX_DAILY
            asset = 'I'
        else:
            # 50 times/min
            # df = ts.pro_bar(ts_code=ts_code, asset='I', adj='qfq', start_date=start_date, end_date=end_date)
            code = self.op_code.SET_STOCK_DAILY
            asset = 'E'
            adj = 'qfq'

        try:
            print(f"ts_code={ts_code}, api={self.api_flag}, {self.api}, asset={asset}, adj={adj},"
                  f" start_date={start_date}, end_date={end_date}")
            df = ts.pro_bar(ts_code=ts_code, api=self.api, asset=asset, adj=adj,
                            start_date=start_date, end_date=end_date)
            save(df, op_code=code)
        except Exception as e:
            print(e)
            if self.all_api_used >= 1:
                self.all_api_used = -1
                time.sleep(55)
            self.api_flag = not self.api_flag
            self.api = self.pro_api[self.api_flag]
            self.all_api_used += 1

            print("api token cut, retry...")
            print(f"ts_code={ts_code}, api={self.api_flag}, asset={asset}, adj={adj},"
                  f" start_date={start_date}, end_date={end_date}")
            df = ts.pro_bar(ts_code=ts_code, api=self.api, asset=asset, adj=adj,
                            start_date=start_date, end_date=end_date)
            save(df, op_code=code)


# universal finance data getter
class Daily:
    tu = Tushare()

    def __init__(self):
        pass

    # get index's ts_code list or stock's ts_code list from Tushare
    def get_tscode_list(self) -> map:
        print("getting tscode list...")
        df = self.tu.get_basic_info(only_tscode=True)
        return map(lambda x: x[0], df.values.tolist())

    # get basic info of both index and stock
    def get_basic_info(self):
        print("request for basic info...")
        self.tu.get_basic_info(is_index=False)
        self.tu.get_basic_info(is_index=True)

    # iterate the index list or stock list to get the data of specific index or stock
    def get_price(self, only_today=True):
        order = 0
        f = self.tu.get_price_today if only_today else self.tu.get_price_year
        for is_index in [True, False]:
            for code in self.get_tscode_list(is_index):
                order += 1
                print(f"order: {order}, request for price of {code}...")
                f(code, is_index)


# base class for basic crawler operation
class CrawlerBase:
    session = requests.session()
    only_today = True
    img_re = re.compile(r'\[(\w+)\]')

    def __init__(self, headers, cookies):
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
            partial_request = functools.partial(self.session.get, url, headers=headers, timeout=(3, 5))
        elif params is dict:
            # r = self.session.post(url, data=params, headers=headers, timeout=(3, 5))
            partial_request = functools.partial(self.session.post, url, data=params, headers=headers, timeout=(3, 5))
        else:
            raise TypeError
        # todo: error handler
        RETRY_LIMIT = 10
        while RETRY_LIMIT > 0:
            r = partial_request()
            if r.status_code == 200:
                return r.text
            elif r.status_code == 404 or r.status_code == 302:
                print(f'Failed with status_code {r.status_code}, url = {url}, probably this stock not exist')
                return None
            elif r.status_code != 200:
                print(f'Failed with status_code {r.status_code}, url = {url}, retrying...')
                RETRY_LIMIT -= 1
                time.sleep(random.randint(0, 3))

        print(f"Failed within 10 times retry, url = {url}")
        return None

    # get decoded response and parse it as json
    def get_parsed_json_response(self, url, headers, params=None):
        decoded_text = self.get_url_content(url, headers, params)
        if decoded_text is None:
            return None
        return json.loads(decoded_text)

    # parse the document and extract the wanted element
    def get_target_element(self, selector: str, html_text: str):
        html_parsed = bf(html_text, "lxml")
        return html_parsed.find_all(selector)

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
        return map(lambda x: self.img_re.findall(r'\[(\w+)\]', x.attrs['alt'])[0] if 'alt' in x.attrs else '', img_list)

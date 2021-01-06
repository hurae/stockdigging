import json
import pandas as pd
import tushare as ts
import datetime
import status_code


# get the date string of today
def get_today():
    return datetime.date.today().strftime('%Y%m%d')


# get the date string of the day which is 365 days ago
def get_year():
    last_year_date = datetime.date.today() - datetime.timedelta(days=365)
    return last_year_date.strftime('%Y%m%d')


# todo: complete saver function
# Universal DB saver
def save(df: pd.DataFrame, op_code: int):
    # if df != None:
    json_string = df.to_json(orient='split', force_ascii=False)
    print(op_code, json_string)


# wrapper of tushare sdk, adapted for our needs
class Tushare:
    pro_stock = ts.pro_api('85c250f231ccbe95aa63350b365d892161ecf18810ff7b93e35fc1f4')
    pro_index = ts.pro_api('6d2175719e5b5d27c8b7f3ae83402bbf806979bcd53ec6500808c31a')
    op_code = status_code.OpCode()
    error_code = status_code.ErrorCode()

    def __init__(self):
        pd.set_option('display.max_columns', 100)
        pd.set_option('display.max_rows', 1000)
        pd.set_option('display.width', 500)

    # get all basic index info and save it
    def get_basic_info(self, is_index: bool):
        if is_index:
            df = self.pro_index.index_basic()
            code = self.op_code.SET_INDEX_INFO
        else:
            df = self.pro_stock.stock_basic(exchange='', list_status='L',
                                            fields='ts_code,name,symbol,list_date,area,industry')
            code = self.op_code.SET_STOCK_INFO
        save(df, op_code=code)

    # get today's index number or stock price
    def get_price_today(self, ts_code: str, is_index: bool):
        today = get_today()
        self.get_price_daily(ts_code, today, today, is_index)
        self.get_price_daily(ts_code, today, today, is_index)

    # get the last year's index number history or stock price history
    def get_price_year(self, ts_code: str, is_index: bool):
        year_ago = get_year()
        today = get_today()
        self.get_price_daily(ts_code, year_ago, today, is_index)
        self.get_price_daily(ts_code, year_ago, today, is_index)

    # todo: complete ts_code getter
    # get index list or stock list from database
    def get_list_from_db(self, is_index: bool):
        if is_index:
            return []
        else:
            return []

    # base api wrapper of tushare for index number and stock price
    def get_price_daily(self, ts_code: str, start_date: str, end_date: str, is_index: bool):
        if is_index:
            df = self.pro_index.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            code = self.op_code.SET_INDEX_DAILY
        else:
            df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
            code = self.op_code.SET_STOCK_DAILY
        save(df, op_code=code)

    # iterate the index list or stock list to get the data of specific index or stock
    def trace_list(self, is_index: bool, only_today=True):
        deal_list = self.get_list_from_db(is_index)
        for ele in deal_list:
            if only_today:
                self.get_price_today(ele, is_index)
            else:
                self.get_price_year(ele, is_index)


# universal finance data getter
class Daily:
    tu = Tushare()

    def __init__(self):
        pass

    # get basic info of both index and stock
    def get_basic_info(self):
        # return error
        pass

    # get today's price of both index and stock
    def get_index_stock_today(self):
        # return error
        pass

    # get price of both index and stock of the last 12 month
    def get_index_stock_history(self):
        # return error
        pass


# base class for basic crawler operation
class CrawlerBase:
    base_url = ""
    header = {}  # 字典

    def __init__(self):
        pass

    # set http header
    def set_header(self, header):
        pass

    # get response and decode it
    def get_url_content(self, url):
        pass

    # parse the document and extract the wanted element
    def get_target_element(self, selector, content):
        # return str
        pass


# Crawler for Guba
class Guba(CrawlerBase):
    guba_home = ""

    def __init__(self):
        super().__init__()
        pass

    # main entrance for Guba crawler
    def start(self, date):
        # return bool
        pass

    # get the number of how mana people have read it
    def get_popular_num(self, page_content):
        pass

    # return a comments list which contains every article's comment of all stocks
    def get_all_comment(self, page_content):
        pass

    # get all comment of the specific article
    def get_comment_by_article(self, page_content):
        pass

    # get all comments of the specific article
    def get_comment_by_stock(self, stock_code):
        # return str
        pass

    # get next page's post list
    def get_next_page(self, page_content):
        # return str
        pass

    # return the next post of the post list
    def get_next_article(self, page_content):
        # return str
        pass


# Crawler for Xueqiu
class Xueqiu(CrawlerBase):
    xueqiu_home = ""

    def __init__(self):
        super().__init__()
        pass

    # main entrance of Xueqiu crawler
    def start(self, date):
        # return bool
        pass

    # get the number of how mana people have read it
    def get_popular_num(self, page_content):
        pass

    # return a comments list which contains every article's comment of all stocks
    def get_all_comment(self, page_content):
        pass

    # get all comment of the specific article
    def get_comment_by_article(self, page_content):
        pass

    # get all comments of the specific article
    def get_comment_by_stock(self, stock_code):
        # return str
        pass

    # get next page's post list
    def get_next_page(self, page_content):
        # return str
        pass

    # return the next post of the post list
    def get_next_article(self, page_content):
        # return str
        pass


# universal comment getter
class Comment:
    guba = Guba()
    xueqiu = Xueqiu()

    def __init__(self):
        pass

    # get all comment today from both Guba and Xueqiu
    def get_comment_today(self):
        # return error
        pass

    # get all comment last 12 month from both Guba and Xueqiu
    def get_comment_history(self):
        # return str
        pass


# scheduler for all crawlers
class Scheduler:
    config = {}

    def __init__(self):
        self.set_task()

    # read config file and initialize it
    def set_task(self):
        with open("config.yml") as config_file:
            self.config = json.loads(config_file.read())

    # main entrance of Scheduler, start from here
    def start(self):
        pass


if __name__ == '__main__':
    # tu.get_stock_year('000001.SZ')
    scheduler = Scheduler()
    try:
        scheduler.start()
    except Exception as e:
        print(e)
    finally:
        print("done")

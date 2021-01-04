import tushare as ts
from dateutil.relativedelta import relativedelta
import datetime


def get_today():#获取当天日期
    print(datetime.date.strftime(datetime.date.today(), '%Y%m%d'))
    return datetime.date.strftime(datetime.date.today(), '%Y%m%d')

def get_year():#获取一年前的日期
    last_year_date = datetime.date.today() - relativedelta(months=12)
    print(datetime.date.strftime(last_year_date, '%Y%m%d'))
    return datetime.date.strftime(last_year_date, '%Y%m%d')

def save(df):  # pandas转化为json
    #if df != None:
    json_string = df.to_json(orient='split', force_ascii=False)
    print(json_string)

class Tushare:
    pro_stock = ts.pro_api('85c250f231ccbe95aa63350b365d892161ecf18810ff7b93e35fc1f4')
    pro_index = ts.pro_api('85c250f231ccbe95aa63350b365d892161ecf18810ff7b93e35fc1f4')

    def __init__(self):
        pass

    def get_index_info(self):  # 获取指数信息
        pass

    def get_stock_info(self):#获取股票信息
        df = self.pro_stock.stock_basic(exchange='', list_status='L', fields='ts_code,name,symbol,list_date,area,industry')
        save(df)

    def get_index_today(self, ts_code):  # 获取一天指数信息
        pass

    def get_stock_today(self, ts_code):#获取一天股价信息
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=get_today(), end_date=get_today())
        save(df)

    def get_index_year(self, ts_code):  # 获取一年间指数信息
        pass

    def get_stock_year(self, ts_code):#获取一年间股价信息
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=get_year(), end_date=get_today())
        save(df)

    def get_list_from_db(self, isIndex):
        pass

    def get_index_daily(self, ts_code, start_date, end_date):
        pass

    def get_stock_daily(self, ts_code, start_date, end_date):
        pass

    def trace_list(self, isIndex):
        pass

class Daily:
    tu = Tushare()

    def __init__(self):
        pass

    def get_basic_info(self):
        #return error
        pass

    def get_index_stock_today(self):
        # return error
        pass

    def get_index_stock_history(self):
        # return error
        pass

class Crawler_base:
    base_url = ""
    header = {}#字典

    def __init__(self):
        pass

    def set_header(self, header):
        pass

    def get_url_content(sel, url):
        pass

    def get_target_element(self, selector, content):
        # return str
        pass

class Guba:
    guba_home = ""

    def __init__(self):
        pass

    def start(self, date):
        # return bool
        pass

    def get_popular_num(self, page_content):
        pass

    def get_all_comment(self, page_comment):
        pass

    def get_comment_by_article(self, page_comment):
        pass

    def get_comment_by_stock(self, str):
        # return str
        pass

    def get_next_page(self, page_content):
        # return str
        pass

    def get_next_article(self, page_content):
        # return str
        pass


class Xueqiu:
    xueqiu_home = ""

    def __init__(self):
        pass

    def start(self, date):
        # return bool
        pass

    def get_popular_num(self, page_content):
        pass

    def get_all_comment(self, page_comment):
        pass

    def get_comment_by_article(self, page_comment):
        pass

    def get_comment_by_stock(self, str):
        # return str
        pass

    def get_next_page(self, page_content):
        # return str
        pass

    def get_next_article(self, page_content):
        # return str
        pass

class Comment:
    guba = Guba()
    xueqiu = Xueqiu()

    def __init__(self):
        pass

    def get_comment_today(self):
        # return error
        pass

    def get_comment_history(self):
        # return str
        pass

class Scheduler:
    config = {}

    def __init__(self):
        pass

    def set_task(self, map):
        # return bool
        pass

    def start(self):
        pass



if __name__ == '__main__':
    tu = Tushare()
    #tu.get_stock_info()
    #tu.get_stock_today('000001.SZ')
    tu.get_stock_year('000001.SZ')

    print("done")
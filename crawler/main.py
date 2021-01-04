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

class Tushare:
    pro_stock = ts.pro_api('85c250f231ccbe95aa63350b365d892161ecf18810ff7b93e35fc1f4')

    def __init__(self):
        pass

    def save_stock(self, df):#pandas转化为json
        if df != None:
            json_string = df.to_json(orient='split', force_ascii=False)
            print(json_string)

    def get_stock_info(self):#获取股票信息
        df = self.pro_stock.stock_basic(exchange='', list_status='L', fields='ts_code,name,symbol,list_date,area,industry')
        self.save_stock(df)

    def get_stock_today(self, ts_code):#获取一天股价信息
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=get_today(), end_date=get_today())
        self.save_stock(df)

    def get_stock_year(self, ts_code):#获取一年间股价信息
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=get_year(), end_date=get_today())
        self.save_stock(df)


if __name__ == '__main__':
    tu = Tushare()
    #tu.get_stock_info()
    tu.get_stock_today('000001.SZ')
    #tu.get_stock_year('000001.SZ')

    print("done")
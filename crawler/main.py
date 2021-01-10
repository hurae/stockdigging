import sys
import time
import pandas as pd
import tushare as ts
import yaml
import schedule

from digging_utils import *
from crawler import *
import status_code

# address of database manager
db_addr = 'http://db.local/'


# todo: complete saver function
# Universal DB saver
def save(df: pd.DataFrame, op_code: int):
    """
    index_info:
    {"ts_code":"000001.SH","name":"上证指数","market":"SSE","publisher":"中证公司","category":"综合指数","base_date":"19901219","base_point":100.0,"list_date":"19910715"}

    stock_info:
    {"ts_code":"689009.SH","symbol":"689009","name":"九号公司-UWD","area":"北京","industry":"专用机械","market":"CDR","list_date":"20201029"}

    index_daily:
    {"ts_code":"000001.SH","trade_date":"20210106","close":3550.8767,"open":3530.9072,"high":3556.8022,"low":3513.1262,"pre_close":3528.6767,"change":22.2,"pct_chg":0.6291,"vol":370230926.0,"amount":521799529.8000000119}

    stock_daily:
    {"ts_code":"600187.SH","trade_date":"20210106","open":2.4,"high":2.4,"low":2.34,"close":2.35,"pre_close":2.41,"change":-0.06,"pct_chg":-2.4896,"vol":122540.51,"amount":28972.52}

    final_msg:
    {'operate_code': 9, 'data': '[{"ts_code":"600187.SH","trade_date":"20210106","open":2.4,"high":2.4,"low":2.34,"close":2.35,"pre_close":2.41,"change":-0.06,"pct_chg":-2.4896,"vol":122540.51,"amount":28972.52},{"ts_code":"600187.SH","trade_date":"20210105","open":2.46,"high":2.46,"low":2.39,"close":2.41,"pre_close":2.47,"change":-0.06,"pct_chg":-2.4291,"vol":199402.05,"amount":48193.974},{"ts_code":"600187.SH","trade_date":"20210104","open":2.48,"high":2.5,"low":2.44,"close":2.47,"pre_close":2.5,"change":-0.03,"pct_chg":-1.2,"vol":168340.77,"amount":41672.599}]'}
    """

    json_string = df.to_json(orient='records', force_ascii=False)
    route = "/set/info"
    final_msg = {
        "operate_code": op_code,
        "data": json_string
    }
    universal_post(final_msg, route)
    print(op_code, json_string[:120] + ".......")
    print(final_msg)
    print(df)
    print("------------------------------------------------------")


# post with error detection and unlimited retry
def universal_post(params, route):
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
    pro_stock = ts.pro_api('85c250f231ccbe95aa63350b365d892161ecf18810ff7b93e35fc1f4')
    pro_index = ts.pro_api('6d2175719e5b5d27c8b7f3ae83402bbf806979bcd53ec6500808c31a')
    op_code = status_code.OpCode()
    error_code = status_code.ErrorCode()

    def __init__(self):
        pd.set_option('display.max_columns', 100)
        pd.set_option('display.max_rows', 10)
        pd.set_option('display.width', 200)

    # get all basic info and save it or return only tscode dataframe
    def get_basic_info(self, is_index: bool, only_tscode: bool = False):
        fields = ['ts_code'] if only_tscode else []
        if is_index:
            df = self.pro_index.index_basic(fields=fields)
            code = self.op_code.SET_INDEX_INFO
        else:
            df = self.pro_stock.stock_basic(fields=fields)
            code = self.op_code.SET_STOCK_INFO

        if not only_tscode:
            save(df, op_code=code)
        else:
            return df

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

    # base api wrapper of tushare for index number and stock price
    def get_price_daily(self, ts_code: str, start_date: str, end_date: str, is_index: bool):
        if is_index:
            df = self.pro_index.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            code = self.op_code.SET_INDEX_DAILY
        else:
            # todo: replace with pro_api
            df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
            code = self.op_code.SET_STOCK_DAILY
        save(df, op_code=code)


# universal finance data getter
class Daily:
    tu = Tushare()

    def __init__(self):
        pass

    # get index's ts_code list or stock's ts_code list from Tushare
    def get_tscode_list(self, is_index: bool) -> map:
        df = self.tu.get_basic_info(is_index, only_tscode=True)
        return map(lambda x: x[0], json.loads(df.to_json(orient='values')))

    # get basic info of both index and stock
    def get_basic_info(self):
        self.tu.get_basic_info(is_index=False)
        self.tu.get_basic_info(is_index=True)

    # iterate the index list or stock list to get the data of specific index or stock
    def get_price(self, only_today=True):
        f = self.tu.get_price_today if only_today else self.tu.get_price_year
        for is_index in [True, False]:
            for code in self.get_tscode_list(is_index):
                f(code, is_index)


# Crawler for Guba
class Guba(CrawlerBase):
    guba_home = ""

    def __init__(self, headers, cookies):
        super().__init__(headers, cookies)
        pass

    # main entrance for Guba crawler
    def start(self, only_today):
        self.set_base(only_today)
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

    def __init__(self, headers, cookies):
        super().__init__(headers, cookies)

    # main entrance of Xueqiu crawler
    def start(self, only_today):
        self.set_base(only_today)
        return self.get_all_comment()

    # return a comments "dict" which contains every article's comment of "all stocks"
    def get_all_comment(self):
        stock_list = []
        all_comments_dict = {}
        for ele in stock_list:
            popular_num_sum, comment_reply_list = self.get_comment_by_stock(ele)
            all_comments_dict[ele] = (popular_num_sum, comment_reply_list)

        return all_comments_dict

    # get all comments of the specific stock
    def get_comment_by_stock(self, stock_code: str):
        comment_reply_list = []
        popular_num_sum = 0

        stop_status = self.trace_all_pages(stock_code, comment_reply_list, popular_num_sum)
        print(stop_status)

        return popular_num_sum, comment_reply_list

    # deal with all pages
    def trace_all_pages(self, stock_code: str, comment_reply_list: list, popular_num_sum: int):
        # scan all 100 pages of comments, the max page is 100
        for i in range(100):
            parsed_response = self.get_comment_page(stock_code, page=i + 1)
            comment_list = self.extract_comment_list(parsed_response)
            # stop if this stock has less than 100 pages
            if not comment_list:
                return f"All {0} page(s) done".format(i)

            # scan all comments and their replies in this page
            for comment_item in comment_list:
                # get comment date
                comment_time = self.extract_comment_time(comment_item)
                if comment_time < (get_today() if self.only_today else get_year()):
                    return f"Stopped at {0}, while today is {1}".format(comment_time, get_today())

                # get comment text
                comment_text = self.extract_comment_text(comment_item)
                comment_reply_list.append((comment_time, comment_text))

                # get popular number
                popular_num_sum += self.extract_popular_number_of_one_comment(comment_list)

                # scan all replies of current comments
                comment_id = self.extract_comment_id(comment_item)
                reply_count = self.extract_reply_count(comment_item)
                for ele in self.get_reply_list(self.get_reply_content(comment_id, reply_count)):
                    comment_reply_list.append(ele)
        return "all pages done"

    # get the wanted page of comments of given stock
    def get_comment_page(self, stock_code: str, page: int):
        url = "https://xueqiu.com:443/query/v1/symbol/search/status?u=7164308215&uuid=1346768825525350400&count=100" \
              f"&comment=0&symbol={stock_code}&hl=0&source=all&sort=&" \
              f"page={page}&q=&type=11&session_token=null&access_token" \
              "=e220ad18f2449eca248b5aa5ba3b6464ffddef72".format(stock_code=stock_code, page=page)
        comment_headers = {"Accept": "*/*",
                           "Referer": f"https://xueqiu.com/S/{stock_code}".format(stock_code=stock_code),
                           "X-Requested-With": "XMLHttpRequest"}

        parsed_response = self.get_parsed_json_response(url, headers=comment_headers)
        return parsed_response

    # get reply list
    def get_reply_list(self, parsed_response: dict) -> list:
        reply_list = []
        for ele in parsed_response['comments']:
            reply_list.append(ele['text'])
        return reply_list

    # get all replies of the given comment
    def get_reply_content(self, comment_id, comment_count):
        url = f"https://xueqiu.com:443/statuses/comments.json?id={comment_id}&count={comment_count}&page=1&reply" \
              f"=true&asc=false&type=status&split=true".format(comment_id=comment_id, comment_count=comment_count)
        reply_headers = {"Accept": "application/json, text/plain, */*"}
        parsed_response = self.get_parsed_json_response(url, headers=reply_headers)
        return parsed_response

    # return a list which contains all comment items
    def extract_comment_list(self, parsed_response: dict) -> list:
        return parsed_response['list']

    # return the exact text of the given comment
    def extract_comment_text(self, comment_item):
        text = comment_item['text']
        a_text = ','.join(map(lambda x: x[0], self.extract_label_a(text)))
        p_text = ','.join(self.extract_label_p(text))
        img_text = ','.join(self.extract_label_img(text))

        return p_text + a_text + img_text

    # add view_count, reply_count and retweet_count of one page as the popular number
    def extract_popular_number_of_one_comment(self, comment_item):
        count_sum = 0
        view_count = comment_item['view_count']
        reply_count = comment_item['reply_count']
        retweet_count = comment_item['retweet_count']
        count_sum += view_count + 2 * (reply_count + retweet_count)

        return count_sum

    # get comment id for given one comment, in order to request for replies of the comment
    def extract_comment_id(self, comment_item):
        return comment_item['id']

    # get the time when the comment is created
    def extract_comment_time(self, comment_item):
        return get_date_from_timestamp(comment_item['created_at'])

    # get reply count of the given comment
    def extract_reply_count(self, comment_item):
        return comment_item['reply_count']


# universal comment getter
class Comment:
    headers_public_xueqiu = {"Connection": "Keep-Alive", "DNT": "1",
                             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                           " Chrome/87.0.4280.88 Safari/537.36",
                             "elastic-apm-traceparent": "00-2827a5c12a251b88ec5bd9cd382c3fbb-8ee8601f0fdbc257-00",
                             "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
                             "Accept-Encoding": "gzip, deflate",
                             "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
    cookies_public_xueqiu = {"device_id": "bb106f8825a4917c70219db041af129a", "s": "d4129ojzw7",
                             "xq_is_login": "1", "u": "7164308215", "bid": "840c28f1e2bc907727de3c615d5b6730_kjcsi86q",
                             "is_overseas": "0"}

    # set public http headers and coolies
    guba = Guba({}, {})
    xueqiu = Xueqiu(headers_public_xueqiu, cookies_public_xueqiu)

    def __init__(self):
        pass

    # get all comment of today or last last 365 days from both Guba and Xueqiu
    def get_comment(self, only_today):
        self.xueqiu.start(only_today)
        # todo: complete guba's starter
        self.guba.start(only_today)


# scheduler for all crawlers
class Scheduler:
    """
        config Example:
        default:
          today_now: TRUE
          history_now: FALSE
          task_time:
            - "15:10"
            - "22:00"
    """

    config = {}
    daily = Daily()
    comment = Comment()

    class ConfigException(Exception):
        pass

    class TestDone(Exception):
        pass

    def __init__(self, arguments):
        self.set_task(arguments)

    # read config file and initialize it
    def set_task(self, arguments):
        with open("config.yaml") as config_file:
            self.config = yaml.safe_load(config_file)
        if 'default' not in self.config:
            raise self.ConfigException("default configuration not found!")
        self.config = self.config[arguments] if arguments in self.config else self.config['default']

        global db_addr
        db_addr = self.config['db_addr']

    # main entrance of Scheduler, start from here
    def start(self):
        if self.config['history_now']:
            self.job(False)
        if self.config['today_now']:
            self.job(True)
        for ele in self.config['task_time']:
            schedule.every(1).day.at(ele).do(job_func=self.job())

        while True:
            schedule.run_pending()
            time.sleep(60)

    def job(self, only_today: bool = None):
        if only_today is None:
            for only in [False, True]:
                self.daily.get_basic_info()
                self.daily.get_price(only)
                self.comment.get_comment(only)
        else:
            self.daily.get_basic_info()
            self.daily.get_price(only_today)
            self.comment.get_comment(only_today)
            raise self.TestDone


if __name__ == '__main__':
    sys_arguments = sys.argv[1] if len(sys.argv) >= 2 else None
    if sys_arguments is None:
        print('Configuration not set, trying to use default configuration...')
    scheduler = Scheduler(sys_arguments)
    try:
        scheduler.start()
    except Exception as e:
        print(e)
    finally:
        print("END at {0}".format(get_time()))

    # pass
    # tu = Tushare()
    # tu.get_basic_info(is_index=True)
    # # tu.get_basic_info(is_index=False)
    # # tu.get_price_daily('600187.SH', start_date='20210101', end_date='20210106', is_index=False)
    # tu.get_price_daily('000001.SH', start_date='20210101', end_date='20210106', is_index=True)

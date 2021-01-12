import sys
import yaml
import schedule
from crawler import *


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
        stock_list = map(lambda x: x.split('.')[1] + x.split('.')[0], self.get_tscode_list())
        all_comments_dict = {}
        for ele in stock_list:
            print(f'Crawling comment of {ele} of Xueqiu...')
            popular_num_sum, comment_reply_list = self.get_comment_by_stock(ele)
            all_comments_dict[ele] = (popular_num_sum, comment_reply_list)

        return all_comments_dict

    # get all comments of the specific stock
    def get_comment_by_stock(self, stock_code: str):
        comment_reply_list = []

        stop_status, popular_num_sum = self.trace_all_pages(stock_code, comment_reply_list)
        print(stop_status)

        return popular_num_sum, comment_reply_list

    # deal with all pages
    def trace_all_pages(self, stock_code: str, comment_reply_list: list):
        popular_num_sum = 0
        # scan all 100 pages of comments, the max page is 100
        for i in range(100):
            parsed_response = self.get_comment_page(stock_code, page=i + 1)
            if parsed_response is None:
                return f"Comment trace failed for stock {stock_code}"
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

        # parsed_response is None if request failed
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
        for ele in comment_item:
            view_count = ele['view_count']
            reply_count = ele['reply_count']
            retweet_count = ele['retweet_count']
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
        print(f"Scheduler started at {get_time()}.")

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
        print("doing job...")
        if only_today is None:
            for only in [False, True]:
                self.daily.get_basic_info()
                self.daily.get_price(only)
                self.comment.get_comment(only)
        else:
            self.comment.get_comment(only_today)
            self.daily.get_basic_info()
            self.daily.get_price(only_today)
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
        print(f"END at {get_time()}")

    # pass
    # tu = Tushare()
    # tu.get_basic_info(is_index=True)
    # tu.get_basic_info(is_index=False)
    # tu.get_price_daily('600187.SH', start_date='20210101', end_date='20210106', is_index=False)
    # tu.get_price_daily('000001.SH', start_date='20210101', end_date='20210106', is_index=True)

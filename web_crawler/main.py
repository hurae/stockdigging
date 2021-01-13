import sys
from time import sleep
import traceback
import yaml
import schedule
from crawler import *
from lxml import etree

from crawler import save


class Guba(CrawlerBase):
    guba_home = ""

    def __init__(self, headers, cookies):
        super().__init__(headers, cookies)

    # main entrance for Guba web_crawler
    def start(self, only_today):
        self.set_base(only_today)
        return self.get_all_comment()

    # return a comments list which contains every article's comment of all stocks
    def get_all_comment(self):
        def f(x):
            print(f'(ts_code, is_index): {x}')
            stock_code = x[0][:6]
            exchange = x[0][-2:]
            is_index = x[1]
            if is_index:
                code = 'zs' + exchange.lower() + stock_code
            else:
                code = stock_code
            return code, x[0]

        index_list = map(f, filter(lambda x: x[1], self.get_tscode_list()))
        stock_list = map(f, filter(lambda x: not x[1], self.get_tscode_list()))
        all_index_comments_dict = {}
        all_stock_comments_dict = {}
        # popular_num_sum, article_comment_list = self.get_comment_by_stock("zssh000001")
        # all_comments_dict["zssh000001"] = (popular_num_sum, article_comment_list)
        count = 0

        count = self.iter_list(all_index_comments_dict, count, index_list)
        self.iter_list(all_stock_comments_dict, count, stock_list)

        return all_index_comments_dict, all_stock_comments_dict

    def iter_list(self, comments_dict, count, code_list):
        for url_code, tscode in code_list:
            print("stock_code:", url_code)
            popular_num_sum, article_comment_list = self.get_comment_by_stock(url_code)
            comments_dict[tscode] = (int(popular_num_sum), article_comment_list)
            count += 1
            print("*****count:" + str(count) + "," + url_code + "," + "popular_num_sum:" + str(
                popular_num_sum) + ",article_comment_list" + str(article_comment_list))
        return count

    # get the number of how many people have read it
    def get_popular_num(self, read_num, comment_num):
        return (int(read_num) + int(comment_num)) * 2

    # get the element by xpath
    def get_target_element(self, selector, html_text):
        html_parsed = etree.HTML(html_text)
        return html_parsed.xpath(selector)

    # get all comments of the specific article
    def get_comment_by_stock(self, stock_code):
        print("get_comment_by_stock")
        popular_num = 0
        page = 1
        article_comment_list = []
        if len(stock_code) > 6:
            start_url = "http://guba.eastmoney.com/list," + str(stock_code) + ",99,f_1.html"
        else:
            start_url = "http://guba.eastmoney.com/list," + str(stock_code) + ",1,f_1.html"
        print("start_url:", start_url)
        popular_num = self.get_comment_by_page(stock_code, start_url, popular_num, article_comment_list, page)
        print("popular_num in get_comment_by_stock:", popular_num)
        return popular_num, article_comment_list

    # control whether crawl the specific article by article_date and comment_count
    def get_comment_by_page(self, stock_code, article_list_url, popular_num, article_comment_list, page):
        print("get_comment_by_page")
        page_header = {
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        self.session.cookies.update({})
        html_text = self.get_url_content(article_list_url, page_header)
        if html_text != None:
            if "最近一年无帖子！" not in html_text:
                print("here")
                li_list = self.get_target_element('//*[@id="articlelistnew"]/div[@class!="dheader odd"]', html_text)
                for index in range(len(li_list) - 2):
                    url_item = {}
                    url_item["read_num"] = self.get_target_element(
                        '//*[@id="articlelistnew"]/div[@class!="dheader odd"]//span[@class="l1 a1"]/text()', html_text)[
                        index + 1].strip()
                    print("read_num:", url_item["read_num"])
                    url_item["comment_num"] = self.get_target_element(
                        '//*[@id="articlelistnew"]/div[@class!="dheader odd"]//span[@class="l2 a2"]/text()', html_text)[
                        index + 1].strip()
                    print("comment_num:", url_item["comment_num"])
                    url_item["url"] = self.get_target_element(
                        '//*[@id="articlelistnew"]/div[@class!="dheader odd"]//span[@class="l3 a3"]/a/@href',
                        html_text)[index]
                    print("url:", url_item["url"])
                    if 'cjpl' in url_item["url"]:
                        sleep(120)
                        self.get_comment_by_stock(stock_code)
                    else:
                        article_code = re.findall(r'\d,(\d+).html', url_item["url"])[0]
                        print("article_code:", article_code)
                        article_date = self.get_article_date(stock_code, article_code)
                        article_date = article_date.replace('-', '')
                        print("article_date:", article_date)
                        print(f"comment_time: {article_date}, the_day: {status_code.get_value('the_day')}")
                        if article_date > status_code.get_value('the_day'):
                            continue
                        if article_date < status_code.get_value('the_day'):
                            return popular_num
                        # if article_date >= (get_today_format() if self.only_today else get_year_format()):
                        if article_date == status_code.get_value('the_day'):
                            popular_num += self.get_popular_num(url_item["read_num"], url_item["comment_num"])
                            print("popular_num in get_comment_by_page:", popular_num)
                            if int(url_item["comment_num"]) > 0:
                                self.get_comment_by_article(stock_code, article_code, url_item["comment_num"],
                                                            article_comment_list)

                popular_num = self.get_next_page(stock_code, popular_num, article_comment_list, page)

        return popular_num

    # get next page's post list
    def get_next_page(self, stock_code, popular_num, article_comment_list, page):
        print("get_next_page")
        page += 1
        if len(stock_code) > 6:
            next_page_url = "http://guba.eastmoney.com/list," + str(stock_code) + ",99,f_" + str(page) + ".html"
        else:
            next_page_url = "http://guba.eastmoney.com/list," + str(stock_code) + ",1,f_" + str(page) + ".html"
        print(next_page_url)
        popular_num = self.get_comment_by_page(stock_code, next_page_url, popular_num, article_comment_list, page)
        print("popular_num in get_next_page", popular_num)
        return popular_num

    # get all comment of the specific article
    def get_comment_by_article(self, stock_code, article_code, comment_num, article_comment_list):
        print("get_comment_by_article")
        article_headers = {'Host': 'guba.eastmoney.com',
                           'Accept': 'application/json, text/javascript, */*; q=0.01',
                           'X-Requested-With': 'XMLHttpRequest',
                           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                           'Origin': 'http://guba.eastmoney.com',
                           'Referer': "http://guba.eastmoney.com/news,{stock_code},{article_code}_1.html".format(
                               stock_code=stock_code, article_code=article_code),
                           }
        comment_data = {
            'param': 'postid={article_code}&sort=1&sorttype=1&p=1&ps={reply_count}'.format(article_code=article_code,
                                                                                           reply_count=comment_num),
            'path': 'reply/api/Reply/ArticleNewReplyList',
            'env': '2'}
        comment_url = "http://guba.eastmoney.com/interface/GetData.aspx"
        comment_dict = self.get_parsed_json_response(comment_url, article_headers, comment_data)
        if comment_dict["re"] is not None:
            for i in range(len(comment_dict["re"])):
                print((comment_dict["re"][i]["reply_time"][:10].replace('-',''), comment_dict["re"][i]["reply_text"]))
                article_comment_list.append((comment_dict["re"][i]["reply_time"][:10].replace('-',''), comment_dict["re"][i]["reply_text"]))
                if len(comment_dict["re"][i]["child_replys"]) <= comment_dict["re"][i]["reply_count"]:
                    reply_id = comment_dict["re"][i]["reply_id"]
                    child_comment_data = {
                        'param': 'postid={article_code}&replyid={replyid}&sort=1&sorttype=1&ps={reply_count}&p=1'.format(
                            article_code=article_code, replyid=reply_id,
                            reply_count=comment_dict["re"][i]["reply_count"]),
                        'path': 'reply/api/Reply/ArticleReplyDetail',
                        'env': '2'}
                    child_comment_dict = self.get_parsed_json_response(comment_url, article_headers, child_comment_data)
                    if child_comment_dict is not None and "re" in child_comment_dict \
                            and "child_replys" in child_comment_dict['re'] \
                            and child_comment_dict["re"]["child_replys"] is not None:
                        for j in range(len(child_comment_dict["re"]["child_replys"])):
                            reply_time = child_comment_dict["re"]["child_replys"][j]["reply_time"][:10].replace('-','')
                            reply_text = child_comment_dict["re"]["child_replys"][j]["reply_text"]
                            print((reply_time, reply_text))
                            article_comment_list.append((reply_time, reply_text))

    # get the date of the article has been writen
    def get_article_date(self, stock_code, article_code):
        self.session.cookies.update({})
        print("get_article_date")
        page_header = {
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        article_url = "http://guba.eastmoney.com/news,{stock_code},{article_code}.html".format(stock_code=stock_code,
                                                                                               article_code=article_code)
        print("article_url:", article_url)
        html_text = self.get_url_content(article_url, page_header)
        article_date = self.get_target_element('//*[@id="zwconttb"]/div[2]/text()', html_text)
        return re.findall(r'(\d{4}-\d{2}-\d{2})', article_date[0])[0]


# Crawler for Xueqiu
class Xueqiu(CrawlerBase):
    xueqiu_home = ""

    def __init__(self, headers, cookies):
        super().__init__(headers, cookies)

    # main entrance of Xueqiu web_crawler
    def start(self, only_today):
        self.set_base(only_today)
        return self.get_all_comment()

    # return a comments "dict" which contains every article's comment of "all stocks"
    def get_all_comment(self):
        index_list = map(lambda x: (x[0].split('.')[1] + x[0].split('.')[0], x[0]),
                         filter(lambda x: x[1], self.get_tscode_list())
                         )
        stock_list = map(lambda x: (x[0].split('.')[1] + x[0].split('.')[0], x[0]),
                         filter(lambda x: not x[1], self.get_tscode_list())
                         )
        all_index_comments_dict = {}
        all_stock_comments_dict = {}

        self.iter_list(all_index_comments_dict, index_list)
        self.iter_list(all_stock_comments_dict, stock_list)

        return all_index_comments_dict, all_stock_comments_dict

    def iter_list(self, comments_dict, code_list):
        for url_code, tscode in code_list:
            print(f'Crawling comment of {url_code} of Xueqiu...')
            popular_num_sum, comment_reply_list = self.get_comment_by_stock(url_code)
            comments_dict[tscode] = (popular_num_sum, comment_reply_list)

    # get all comments of the specific stock
    def get_comment_by_stock(self, stock_code: str):
        comment_reply_list = []

        stop_status, popular_num_sum = self.trace_all_pages(stock_code, comment_reply_list)
        print(stop_status)

        return popular_num_sum, comment_reply_list

    # deal with all pages
    def trace_all_pages(self, stock_code: str, comment_reply_list: list):
        popular_num_sum = 0
        check_headers = {"Connection": "close", "DNT": "1", "Upgrade-Insecure-Requests": "1",
                         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                         "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                         "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
                         "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}

        # scan all 100 pages of comments, the max page is 100
        for i in range(100):
            if self.get_url_content("https://xueqiu.com/S/" + stock_code, headers=check_headers) is None:
                return f'{stock_code} not exist', popular_num_sum
            parsed_response = self.get_comment_page(stock_code, page=i + 1)
            if parsed_response is None:
                return f"Comment trace failed for stock {stock_code}", popular_num_sum
            comment_list = self.extract_comment_list(parsed_response)

            # stop if this stock has less than 100 pages
            if not comment_list:
                if 'code' in parsed_response and 'message' in parsed_response:
                    print(f'code: {parsed_response["code"]}, message: {parsed_response["message"]}')
                return f"All {i + 1} page(s) done", popular_num_sum

            # scan all comments and their replies in this page
            for comment_item in comment_list:
                # get comment date
                comment_time = self.extract_comment_time(comment_item)
                print(f"comment_time: {comment_time}, the_day: {status_code.get_value('the_day')}")
                if comment_time > status_code.get_value('the_day'):
                    continue
                if comment_time < status_code.get_value('the_day'):
                    return f"Stopped at {comment_time}, while today is {get_today()}", popular_num_sum
                # if comment_time < (get_today() if self.only_today else get_year()):
                #     return f"Stopped at {comment_time}, while today is {get_today()}", popular_num_sum

                # get comment text
                comment_text = self.extract_comment_text(comment_item)
                print(f"stock_code: {stock_code}, page: {i + 1}, comment_time: {comment_time},"
                      f" comment_text: {comment_text}")
                comment_reply_list.append((comment_time, comment_text))

                # get popular number
                popular_num_sum += self.extract_popular_number_of_one_page(comment_list)

                # scan all replies of current comments
                comment_id = self.extract_comment_id(comment_item)
                reply_count = self.extract_reply_count(comment_item)
                reply_json_content = self.get_reply_content(comment_id, reply_count)
                if reply_json_content is None:
                    print(f"    reply: none")
                    continue
                for i, ele in enumerate(self.get_reply_list(reply_json_content, comment_time)):
                    print(f"    reply{i}: {ele}")
                    comment_reply_list.append(ele)
        return "all pages done", popular_num_sum

    # get the wanted page of comments of given stock
    def get_comment_page(self, stock_code: str, page: int):
        url = "https://xueqiu.com:443/query/v1/symbol/search/status?u=7164308215&uuid=1346768825525350400&count=100" \
              f"&comment=0&symbol={stock_code}&hl=0&source=all&sort=&" \
              f"page={page}&q=&type=11&session_token=null&access_token" \
              "=e220ad18f2449eca248b5aa5ba3b6464ffddef72"
        comment_headers = {"Accept": "*/*",
                           "Referer": f"https://xueqiu.com/S/{stock_code}",
                           "X-Requested-With": "XMLHttpRequest"}

        # parsed_response is None if request failed
        parsed_response = self.get_parsed_json_response(url, headers=comment_headers)
        return parsed_response

    # get reply list
    def get_reply_list(self, parsed_response: dict, comment_time) -> list:
        reply_list = []
        for ele in parsed_response['comments']:
            reply_list.append((comment_time, self.handle_html_label(ele['text'])))
        return reply_list

    # get all replies of the given comment
    def get_reply_content(self, comment_id, comment_count):
        url = f"https://xueqiu.com:443/statuses/comments.json?id={comment_id}&count={comment_count}&page=1&reply" \
              "=true&asc=false&type=status&split=true"
        reply_headers = {"Accept": "application/json, text/plain, */*"}
        parsed_response = self.get_parsed_json_response(url, headers=reply_headers)
        return parsed_response

    # return a list which contains all comment items
    def extract_comment_list(self, parsed_response: dict) -> list:
        if 'list' in parsed_response:
            return parsed_response['list']
        else:
            return []

    # return the exact text of the given comment
    def extract_comment_text(self, comment_item):
        text = comment_item['text']
        return self.handle_html_label(text)

    def handle_html_label(self, text):
        a_text = ','.join(map(lambda x: x[0], self.extract_label_a(text)))
        p_text = ','.join(self.extract_label_p(text))
        img_text = ','.join(self.extract_label_img(text))
        return p_text + a_text + img_text

    # add view_count, reply_count and retweet_count of one page as the popular number
    def extract_popular_number_of_one_page(self, comment_list):
        count_sum = 0
        for ele in comment_list:
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
    headers_public_guba = {'Connection': 'keep-alive',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                           'Accept-Encoding': 'gzip, deflate',
                           'Accept-Language': 'zh-CN,zh;q=0.9', }
    cookies_public_guba = {"intellpositionL": "1524px",
                           "intellpositionT": "2257px",
                           "em_hq_fls": "old",
                           "emshistory": "%5B%22%E6%8C%87%E6%95%B0%22%2C%22%E4%B8%8A%E8%AF%81%E6%8C%87%E6%95%B0%22%5D",
                           "ct": "dkGEpaUDCnQR8xDurG5EKXZ_riKeTGUCmXAND-yMErD1YEopBD3yWnEEuS-ELPnRjxiUTjI6gBxnlDSeaRYTfNnwLKu1_tyBspAB1h6RXuAkzAV_Md3dj-m01kvN0QWWtLMkRPDEju7UgPBwx7Ihyo1gtSGHUIT-SCsiY7UjrCA",
                           "ut": "FobyicMgeV4XKdbUhrvvY717K1eq9okpAhf16XCAGf4T2GXGsgX7jpCYU7Nc4ElS_Oqu954TBXI182qbr_y5gikcKjQzzpHg54A6kyk_E7Bz4WkwAywicSdzgxKWIIROyVmgESPBfYUB5-BNN9RfynFq6L03BDH9MBOvVj87LU_Emacsm8aP1KWFNqy8vt9Ru1a5atZWeM3WRkpZQYWEQ_OKoTcLTvAAluxrs_w2c-No51WmbNmKOAbu1VMsFXV7p0nwnkVxqe3tn_917ZQePdmITgU3b-J0",
                           "pi": "6108395675653978%3bm6108395675653978%3b%e8%82%a1%e5%8f%8b5Deiam%3beAu54BssgjyVQ1Dl75GzPCbZDeuXCoFJNIhAaE9q5qhwT3DST1tHJHQuty9VQZQweo0gpyXhXbBYPf5tknW3rtk8aUA42IXH%2bdgmFAL1hibQHBhZF%2bLr4B%2fzKW%2fyB3YVWlL8TIBglyqpnFzfr8BWhqmVTf4XUiU0ooCYSlHGQiQbVvJVzn%2ffzfheQgenKyAgBND80%2b2q%3bwPhgCWaV5lPZ0jmAsUqacFl%2fvh%2bvJ%2b8L666Q24Le7YZ94%2bhZ%2fakvvPkIPgpKRKiWRrnUsvAOsmzPRQDw1Kvf8EtpWgeeqS2mhnN7dDTp4el7QqG%2b5%2fP4kCANFyZXax5aZyq54GPktMArCFZkNBTf7w%2frm%2bMMgw%3d%3d",
                           "uidal": "6108395675653978%e8%82%a1%e5%8f%8b5Deiam",
                           "sid": "139501923",
                           "vtpst": "|",
                           "HAList": "a-sz-300925-%u6CD5%u672C%u4FE1%u606F%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570",
                           "st_si": "46963940521169",
                           "st_asi": "delete",
                           "qgqp_b_id": "c69227c5d2df8060e3f511e87cb19377",
                           "st_pvi": "81354694049613",
                           "st_sp": "2020-12-30%2009%3A11%3A35",
                           "st_inirUrl": "https%3A%2F%2Fwww.eastmoney.com%2F",
                           "st_sn": "9",
                           "st_psi": "2021011215450469-117001301474-6947178642"}

    headers_public_xueqiu = {"Connection": "Keep-Alive", "DNT": "1",
                             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                           " Chrome/87.0.4280.88 Safari/537.36",
                             "elastic-apm-traceparent": "00-2827a5c12a251b88ec5bd9cd382c3fbb-8ee8601f0fdbc257-00",
                             "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
                             "Accept-Encoding": "gzip, deflate",
                             "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
    cookies_public_xueqiu = {"device_id": "bb106f8825a4917c70219db041af129a", "s": "d4129ojzw7",
                             "bid": "840c28f1e2bc907727de3c615d5b6730_kjcsi86q",
                             "xq_a_token": "e220ad18f2449eca248b5aa5ba3b6464ffddef72",
                             "xqat": "e220ad18f2449eca248b5aa5ba3b6464ffddef72",
                             "xq_r_token": "2af0b8f80a2b546e026d684d6474e89edee05eb3",
                             "xq_id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjcxNjQzMDgyMTUsImlzcyI6InVjIiwiZXhwIjoxNjEyMDA3NDc0LCJjdG0iOjE2MTA0MzI5NjE0ODUsImNpZCI6ImQ5ZDBuNEFadXAifQ.qOTV_kQPKvQTbTPBxM8JREukeUssWgpTAAVCxOf_ox4fL2TD86yy2lIu5YrcPUh9pI8j_lW_P55GAoiBJ2_-JD6l3csm4FVOkTjlTCWaVQeaQA0-cdRpVFMsVMWtXKCTWzRyhNimKjHfOy-Qqy3IXVtvXiX-A8noDut7MCWmHcEp84PapY7F8dTa22_DHC4yZZwid0doQvX2ML-NC1wuXoZ3ESMZ7gqPa3HCz-0y92zdSxort9HDY4vgbfaHit-CSEtOuLENnM-R2D9jcv-Y0rZCUGJAvxVvYtbrobpcMObX3mB0LrCf5BUuoJeye8oo1Pvwz83rnRTptg7C5ggftA",
                             "xq_is_login": "1", "u": "7164308215", "snbim_minify": "true",
                             "acw_tc": "2760820416104329813686124ef59e426bbc51a641268ba88a0dcd3613f65f",
                             "is_overseas": "0"}

    # set public http headers and coolies
    guba = Guba(headers_public_guba, cookies_public_xueqiu)
    xueqiu = Xueqiu(headers_public_xueqiu, cookies_public_xueqiu)
    op_code = status_code.OpCode()

    def __init__(self):
        pass

    # get all comment of today or last last 365 days from both Guba and Xueqiu
    def get_comment(self, only_today):
        if only_today:
            # get 10 days day by day in today mode
            for i in range(10):
                status_code.set_value('the_day', get_the_day_before(i))
                self.iter(only_today)
        else:
            self.iter(only_today)

        print("Comment Done.")

    def iter(self, only_today):
        guba_index_comments, guba_stock_comments = self.guba.start(only_today)
        xueqiu_index_comments, xueqiu_stock_comments = self.xueqiu.start(only_today)
        print('guba_index', guba_index_comments)
        print('guba_stock', guba_stock_comments)
        print('xuqiu_index', xueqiu_index_comments)
        print('xuqiu_stock', xueqiu_stock_comments)
        save(dict(xueqiu_index_comments, **guba_index_comments), op_code=self.op_code.SET_INDEX_COMMENT)
        save(dict(xueqiu_stock_comments, **guba_stock_comments), op_code=self.op_code.SET_STOCK_COMMENT)


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
        status_code.set_value('db_addr', self.config['db_addr'])
        if 'test' in arguments:
            print('string "test" detected, TEST mode start.')
            status_code.set_value('test', True)

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
        self.daily.get_basic_info()
        if only_today is None:
            for only in [False, True]:
                self.daily.get_price(only)
                self.comment.get_comment(only)
        else:
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
        traceback.print_exc()
    finally:
        print(f"END at {get_time()}")

    # pass
    # tu = Tushare()
    # tu.get_basic_info(is_index=True)
    # tu.get_basic_info(is_index=False)
    # tu.get_price_daily('600187.SH', start_date='20210101', end_date='20210106', is_index=False)
    # tu.get_price_daily('000001.SH', start_date='20210101', end_date='20210106', is_index=True)

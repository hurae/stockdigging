# Base package for Crawler
import json
import re
from bs4 import BeautifulSoup as bf

import requests


# base class for basic crawler operation
class CrawlerBase:
    session = requests.session()
    only_today = True

    def __init__(self, headers, cookies):
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)

    # main entrance of Xueqiu crawler
    def set_base(self, only_today):
        self.only_today = only_today

    # set http header
    def set_header(self, headers):
        self.session.headers.update(headers)

    # get response and decode it
    def get_url_content(self, url, headers):
        res = self.session.get(url, headers=headers, timeout=(3, 5))
        # todo: error handler
        if res.status_code != 200:
            raise IOError
        return res.text

    # get decoded response and parse it as json
    def get_parsed_json_response(self, url, headers):
        decoded_text = self.get_url_content(url, headers)
        return json.loads(decoded_text)

    # parse the document and extract the wanted element
    def get_target_element(self, selector, html_text):
        html_parsed = bf(html_text, "lxml")
        return html_parsed.findall(selector)

    # extract all label a, and return an iterator which yield a tuple (text, href)
    def extract_label_a(self, html_text):
        a_list = self.get_target_element('a', html_text)
        return map(lambda x: (x.text, x.attrs['href']), a_list)

    # extract all label p, and return an iterator which yield all inner text
    def extract_label_p(self, html_text):
        p_list = self.get_target_element('p', html_text)
        # find all str inside of a label p, and connect them with symbol ","
        return map(lambda p_item: ','.join(filter(lambda content_item: isinstance(content_item, str),
                                                  p_item.contents)
                                           ),
                   p_list)

    # extract all label img, and return an iterator which yield all alt attrs
    def extract_label_img(self, html_text):
        img_list = self.get_target_element('img', html_text)
        return map(lambda x: re.findall(r'\[(\w+)\]', x.attrs['alt'])[0], img_list)

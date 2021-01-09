import json
from storage.business.business_op import set_stock_state, set_stock_info

js = {"operate_code": 9, "data": [["600187.SH", "20210105", 2.46, 2.46, 2.39, 2.41],
                                  ["600187.SH", "20210104", 2.48, 2.5, 2.44, 2.47]]}


def json_handle(res):
    for i in res['data']:
        set_stock_state( i[0], i[1], i[2], i[3], i[4], i[5])


json_handle( js )

import paddlehub as hub
import pandas as pd
from statsmodels.formula.api import ols
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import status_code
import json
from urllib import parse

storage_url = 'http://192.168.43.106:8000'
senta = hub.Module(name="senta_lstm")  # load model
begin = 1  # first get comment
op_code = status_code.OpCode()
err_code = status_code.ErrorCode()


# deal with comments
class Processing:

    def __init__(self, data):
        self.comment = data["comment"]

    # calculate public index
    def comment_sentiment(self):
        # classify
        try:
            results = senta.sentiment_classify(texts=self.comment)
            public_index = 0
            for result in results:
                public_index = public_index + result["positive_probs"]
        except:
            public_index = 0
        return public_index


# predict stock or index
class Predict:

    def __init__(self, data):
        data = pd.DataFrame(data, columns=['public_index', 'num', 'today_average', 'tomorrow_average'])
        data.fillna(value={'num':0}, inplace=True)
        data['rate_of_change'] = (data['tomorrow_average'] - data['today_average']) / data['today_average']
        self.data = data[['public_index', 'num', 'rate_of_change']]

    # linear regression models
    def predict(self):
        print(self.data)
        lm = ols('rate_of_change ~ public_index + num', data=self.data).fit()
        return lm.params


# request to storage host for features and set forecast
def train(op3, op4, op5):
    global storage_url
    # get process result:index/stock
    storage3 = parse.urljoin(storage_url, op_code.route(op3))
    storage4 = parse.urljoin(storage_url, op_code.route(op4))
    storage5 = parse.urljoin(storage_url, op_code.route(op5))
    send_3 = {"operate_code": op3}
    response_json = requests.post(storage3, json=send_3).json()
    all_params = pd.DataFrame()
    while response_json["error_code"] == err_code.SUCCESS:
        print(response_json)
        data = response_json["data"]
        pr = Predict(data)
        print(pr)
        params = pr.predict()
        print(params)
        all_params = pd.concat([all_params, params], axis=1, ignore_index=True)
        response_json = requests.post(storage3, json=send_3).json()
    if response_json["error_code"] == err_code.ITERATE_END:
        # get today's public index and hot num
        send_4 = {"operate_code": op4}
        response_json = requests.post(storage4, json=send_4).json()
        if response_json["error_code"] == err_code.SUCCESS:
            index = pd.DataFrame(data=response_json["data"], columns=['today_public_index', 'today_num'])
            all_params = all_params.T
            print(all_params)
            index = pd.concat([all_params, index], axis=1)
            print(index)
            index["forecast"] = index["public_index"] * index["today_public_index"] + index["num"] * index[
                "today_num"] + index["Intercept"]
            # post forecast result to save
            send_5 = {"operate_code": op5, "data": {"prediction": index["forecast"].tolist()}}
            print(send_5)
            response_json = requests.post(storage5, json=send_5).json()
            print(response_json)
            return response_json["error_code"]
    return response_json["error_code"]


# request to storage host for comment and set public index
def get_comment(op1, op2):
    global storage_url
    storage1 = parse.urljoin(storage_url, op_code.route(op1))
    storage2 = parse.urljoin(storage_url, op_code.route(op2))
    send_1 = {"operate_code": op1}
    response = requests.post(storage1, json=send_1).json()
    while response["error_code"] == err_code.SUCCESS:
        print("1")
        data = response["data"]
        p = Processing(data)
        public_index = p.comment_sentiment()
        send_2 = {"operate_code": op2, "data": {"public_index": public_index}}
        response = requests.post(storage2, json=send_2).json()
        print(response)
        if response["error_code"] == err_code.SUCCESS:
            print(response["error_code"])
            response = requests.post(storage1, json=send_1).json()
    return response["error_code"]


def main():
    global begin
    if begin == 0:
        error_code = get_comment(op1=op_code.GET_ALL_COMMENT, op2=op_code.SET_PUBLIC_OPINION)
        if error_code == err_code.ITERATE_END:
            begin = 1
        else:
            return main()
    if begin == 1:
        error_code = get_comment(op1=op_code.GET_TODAY_COMMENT, op2=op_code.SET_PUBLIC_OPINION)
        if error_code == err_code.ITERATE_END:
            error_code = train(op3=op_code.GET_STOCK_FEATURE_HISTORY, op4=op_code.GET_STOCK_FEATURE_TODAY,
                               op5=op_code.SET_INCREASE_RATE)
            if error_code == err_code.SUCCESS:
                error_code = train(op3=op_code.GET_INDEX_FEATURE_HISTORY, op4=op_code.GET_INDEX_FEATURE_TODAY,
                                   op5=op_code.SET_INDEX_PREDICTION)
                if error_code == err_code.SUCCESS:
                    return error_code
                else:
                    return main()
            else:
                return main()
        else:
            return main()


test = 2


if __name__ == '__main__':
    if test == 2:
        # test
        main()
    else:
        scheduler = BlockingScheduler()
        scheduler.add_job(main, 'cron', hour='16', minute='30')
        scheduler.add_job(main, 'cron', hour='22', minute='00')

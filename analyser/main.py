import paddlehub as hub
import pandas as pd
from statsmodels.formula.api import ols
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

storage = '127.0.0.1:111'
senta = hub.Module(name="senta_lstm")  # load model
begin = 0  # first get comment


# deal with comments
class Processing:

    def __init__(self, data):
        self.comment = data["comment"]

    # calculate public index
    def comment_sentiment(self):
        # classify
        results = senta.sentiment_classify(texts=self.comment)
        public_index = 0
        for result in results:
            public_index = public_index + result["positive_probs"]
        return public_index


# predict stock or index
class Predict:

    def __init__(self, data):
        data = pd.DataFrame(data, columns=['public_index', 'num', 'today_average', 'tomorrow_average'])
        data['rate_of_change'] = (data['tomorrow_average'] - data['today_average']) / data['today_average']
        self.data = data['public_index', 'num', 'rate_of_change']

    # linear regression models
    def predict(self):
        lm = ols('rate_of_change ~ public_index + num', data=self.data).fit()
        return lm.params


# request to storage host for features and set forecast
def train(op3, op4, op5):
    # get process result:index/stock
    send_3 = {"operate_code": op3}
    response_json = requests.post(storage, data=send_3).json
    all_params = pd.DataFrame()
    while response_json["error_code"] == 0:
        data = response_json["data"]
        pr = Predict(data)
        params = pr.predict()
        all_params = pd.concat([all_params, params])
        response_json = requests.post(storage, data=send_3).json
    if response_json["error_code"] == 5:
        # get today's public index and hot num
        send_4 = {"operate_code": op4}
        response_json = requests.post(storage, data=send_4).json
        if response_json["error_code"] == 0:
            index = pd.DataFrame(data=response_json["data"], columns=['today_public_index', 'today_num'])
            index = pd.concat([all_params, index], axis=1)
            index["forecast"] = index["public_index"] * index["today_public_index"] + index["num"] * index[
                "today_num"] + index["Intercept"]
            # post forecast result to save
            send_5 = {"operate_code": op5, "data": index["forecast"].tolist()}
            response_json = requests.post(storage, data=send_5).json
            return response_json["error"]
    return response_json["error"]


# request to storage host for comment and set public index
def get_comment(op1, op2):
    send_1 = {"operate_code": op1}
    response = requests.post(storage, data=send_1).json
    while response["error_code"] == 0:
        data = response["data"]
        p = Processing(data)
        public_index = p.comment_sentiment()
        del p
        send_2 = {"operate_code": op2, "data": {"public_index": public_index}}
        response = requests.post(storage, data=send_2).json
        if response["error_code"] == 0:
            response = requests.post(storage, data=send_1).json
    return response["error_code"]


def main():
    global begin
    if begin == 0:
        error_code = get_comment(op1=1, op2=3)
        if error_code == 5:
            begin = 1
        else:
            return main()
    if begin == 1:
        error_code = get_comment(op1=2, op2=3)
        if error_code == 5:
            error_code = train(op3=19, op4=21, op5=5)
            if error_code == 0:
                error_code = train(op3=20, op4=22, op5=4)
                if error_code == 0:
                    return error_code
                else:
                    main()
            else:
                return main()
        else:
            return main()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', hour='16', minute='30')
    scheduler.add_job(main, 'cron', hour='22', minute='00')

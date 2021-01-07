import paddlehub as hub
import pandas as pd
from statsmodels.formula.api import ols
# import socket
# import json

analyser_ip, analyser_port = '127.0.0.1', 112
storage_ip, storage_port = '127.0.0.1', 111

# load model
senta = hub.Module(name="senta_lstm")


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
        data = pd.DataFrame(data, columns=['public_index', 'public_index', 'today_average', 'tomorrow_average'])
        data['rate_of_change'] = (data['tomorrow_average'] - data['today_average']) / data['today_average']
        self.data = data['public_index', 'public_index', 'rate_of_change']

    # linear regression models
    def predict(self):
        lm = ols('rate_of_change ~ public_index + num', data=self.data).fit()
        return lm.params


'''
if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((analyser_ip, analyser_port))
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    print('connected with', addr)

    while True:
        data = conn.recv(1024)
        data = data.decode()
        if not data:
            break
        elif data == '??':
            print('receive:', data)
            send = input('send:')
            conn.sendall(send.encode())
        conn.close()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((storage_ip, storage_port))
        while True:
            trigger = {"operate_code": 1}
            client_socket.sendall(trigger)
            data = client_socket.recv(1024)
            data = data.decode()
            text = json.loads(data)
            print('recieved:', data)
            if trigger.lower() == '1':  # 发送1结束连接
                break
        client_socket.close()
    server_socket.close()
'''

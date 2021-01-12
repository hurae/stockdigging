from typing import List
# from datetime import datetime
# from storage.business.server import json_handle
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import status_code
import business.business_op as op

app = FastAPI()
op_code = status_code.OpCode()
err_code = status_code.ErrorCode()
answer = op.answer  # [(stock,date),,]
length = op.length
flag = 0
answer1 = op.answer1
length1 = op.length1
flag1 = 0
ans2 = op.ans2
length2 = op.length2
flag2 = 0
ans3 = op.ans3
length3 = op.length3
flag3 = 0

response_json = {
    "error_code": err_code.SUCCESS,
    "error_message": err_code.error_msg[err_code.SUCCESS]
}


# only send operation_code
class Code(BaseModel):
    operation_code: int


class Opinion(BaseModel):
    public_index: float


class CodeOpinion(Code):
    data: Opinion


class Increase(BaseModel):
    prediction: List


class CodeIncrease(Code):
    data: Increase


class CodeInfo(Code):
    data: List[List]


class Comment(BaseModel):
    ts_code: str
    content: List
    comment_date: str
    num: int


class CodeComment(Code):
    data: Comment


class Userid(BaseModel):
    user_id: int


class CodeUserid(Code):
    data: Userid


class Userinfo(BaseModel):
    name: str
    signature: str
    favcion: bytes
    password: str
    phone: str
    last_login: str


class CodeUserinfo(Code):
    data: Userinfo


class Pwd(BaseModel):
    user_id: int
    password: str


class CodePwd(Code):
    data: Pwd


class Search(BaseModel):
    Search: str


class CodeSearch(Code):
    data: Search


class Filter(BaseModel):
    market: str = ""
    publisher: str = ""
    category: str = ""
    industry: str = ""
    area: str = ""


class CodeFilter(Code):
    data: Filter


class Stock(BaseModel):
    stock_code: str


class CodeStock(Code):
    data: Stock


class Collection(BaseModel):
    user_id: int
    stock_info_id: int


class CodeCollection(Code):
    data: Collection


@app.post("/")
def post_code(code: Code):
    global response_json
    response = response_json
    global flag, flag1
    global flag2, flag3
    if code.operation_code == op_code.GET_ALL_COMMENT:
        # 1.get_all_comment()
        if flag < length:
            data = op.get_stock_all_comment(flag)
            flag = flag + 1
            response["data"] = {
                "comment": data
            }
            return response
        elif flag1 < length1:
            data = op.get_index_all_comment(flag1)
            flag1 = flag1 + 1
            response["data"] = {
                "comment": data
            }
            return response
        elif flag == length and flag1 == length1:
            response["error_code"] = err_code.ITERATE_END
            response["error_message"] = err_code.error_msg[err_code.ITERATE_END]
            return response
        else:
            response["error_code"] = err_code.INTERNAL_ERROR
            response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
            return response
    elif code.operation_code == op_code.GET_TODAY_COMMENT:
        # 2.get_today_comment()
        if flag2 < length2:
            data = op.get_stock_today_comment(flag2)
            flag2 = flag2 + 1
            response["data"] = {
                "comment": data
            }
            return response
        elif flag3 < length3:
            data = op.get_index_today_comment(flag3)
            flag3 = flag3 + 1
            response["data"] = {
                "comment": data
            }
            return response
        elif flag2 == length2 and flag3 == length3:
            response["error_code"] = err_code.ITERATE_END
            response["error_message"] = err_code.error_msg[err_code.ITERATE_END]
            flag2 = 0
            flag3 = 0
            return response
        else:
            response["error_code"] = err_code.INTERNAL_ERROR
            response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
            return response
    elif code.operation_code == op_code.GET_INDUSTRY_INDEX_PREDICTION:
        # 16.get_industry_index_prediction()
        response["data"] = op.get_industry_index_prediction()
        return response
    elif code.operation_code == op_code.GET_MARKET_INDEX_PREDICTION:
        # 17.get_market_index_prediction()
        response["data"] = op.get_market_index_prediction()
        return response
    elif code.operation_code == op_code.GET_STOCK_PREDICTION:
        # 18.get_stock_prediction()
        response["data"] = op.get_stock_prediction()
        return response
    elif code.operation_code == op_code.GET_INDEX_FEATURE_HISTORY:
        # 19.get_index_feature_history()
        if flag3 < length3:
            data = op.get_index_feature_history(flag3)
            flag3 = flag3 + 1
            response["data"] = data
            return response
        elif flag3 == length3:
            flag3 = 0
            response["error_code"] = err_code.ITERATE_END
            response["error_message"] = err_code.error_msg[err_code.ITERATE_END]
            return response
        else:
            response["error_code"] = err_code.INTERNAL_ERROR
            response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
            return response
    elif code.operation_code == op_code.GET_STOCK_FEATURE_HISTORY:
        # 20.get_stock_feature_history()
        if flag2 < length2:
            data = op.get_stock_feature_history(flag2)
            flag2 = flag2 + 1
            response["data"] = data
            return response
        elif flag2 == length2:
            flag2 = 0
            response["error_code"] = err_code.ITERATE_END
            response["error_message"] = err_code.error_msg[err_code.ITERATE_END]
            return response
        else:
            response["error_code"] = err_code.INTERNAL_ERROR
            response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
            return response
    elif code.operation_code == op_code.GET_INDEX_FEATURE_TODAY:
        # 21.get_index_feature_today()
        data = []
        for i in range(length3):
            data.append(op.get_index_feature_today(i))
        response["data"] = data
        return response
    elif code.operation_code == op_code.GET_STOCK_FEATURE_TODAY:
        # 22.get_stock_feature_today()
        data = []
        for i in range(length2):
            data.append(op.get_stock_feature_today(i))
        response["data"] = data
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/opinion")
def post_code_opinion(code_opinion: CodeOpinion):
    global flag
    global flag1
    global response_json
    response = response_json
    if code_opinion.operation_code == op_code.SET_PUBLIC_OPINION:
        # 3.set_public_opinion()
        public_index = code_opinion.data.public_index
        if flag < length:
            op.set_stock_public_opinion(flag, public_index)
            return response
        elif flag1 < length1:
            op.set_index_public_opinion(flag1, public_index)
            return response
        elif flag == length and flag1 == length1:
            response["error_code"] = err_code.ITERATE_END
            response["error_message"] = err_code.error_msg[err_code.ITERATE_END]
            return response
        else:
            response["error_code"] = err_code.INTERNAL_ERROR
            response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
            return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/increase")
def post_code_prediction(code_increase: CodeIncrease):
    global length2, length3, response_json
    response = response_json
    if code_increase.operation_code == op_code.SET_INCREASE_RATE:
        # 4.set_increase_rate()
        prediction = code_increase.data.prediction
        for i in range(length2):
            op.set_increase_rate(i, prediction[i])
        return response
    elif code_increase.operation_code == op_code.SET_INDEX_PREDICTION:
        # 5.set_index_prediction()
        prediction = code_increase.data.prediction
        for i in range(length3):
            op.set_index_prediction(i, prediction[i])
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/info")
def post_code_info(code_info: CodeInfo):
    global response_json
    response = response_json
    if code_info.operation_code == op_code.SET_INDEX_INFO:
        # 6.set_index_info()
        for r in code_info.data:
            print(r)
            op.set_index_info(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12])
        return response
    elif code_info.operation_code == op_code.SET_STOCK_INFO:
        # 7.set_stock_info()
        for r in code_info.data:
            op.set_stock_info(r[0], r[1], r[2], r[3], r[4], r[5])
        return response
    elif code_info.operation_code == op_code.SET_INDEX_DAILY:
        # 8.set_index_daily()
        for r in code_info.data:
            op.set_index_state(r[0], r[1], r[2], r[3], r[4], r[5])
        return response
    elif code_info.operation_code == op_code.SET_STOCK_DAILY:
        # 9.set_stock_daily()
        for r in code_info.data:
            op.set_stock_state(r[0], r[1], r[2], r[3], r[4], r[5])
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return code_info


@app.post("/comment")
def post_code_comment(code_comment: CodeComment):
    global response_json
    response = response_json
    data = code_comment.data
    if code_comment.operation_code == op_code.SET_STOCK_COMMENT:
        # 10.set_stock_comment()
        op.set_stock_comment(data.ts_code, data.content, data.comment_date, data.num)
        return response
    elif code_comment.operation_code == op_code.SET_INDEX_COMMENT:
        # 11.set_index_comment()
        op.set_index_comment(data.ts_code, data.content, data.comment_date, data.num)
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return code_comment


@app.post("/userid")
def post_code_userid(code_userid: CodeUserid):
    global response_json
    response = response_json
    data = code_userid.data
    if code_userid.operation_code == op_code.GET_USER_INFO:
        # 12.get_user_info()
        user = op.get_user_info(data.user_id)[0]
        response["data"] = {
            "name": user[0],
            "signature": user[1],
            "favcion": user[2],
            "state": user[3],
            "password": user[4],
            "phone": user[5],
            "last_login": user[6]
        }
        return response
    elif code_userid.operation_code == op_code.DELETE_USER_INFO:
        # 15.delete_user_info()
        op.delete_user_info(data.user_id)
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/new")
def post_code_userinfo(code_userinfo: CodeUserinfo):
    global response_json
    response = response_json
    data = code_userinfo.data
    if code_userinfo.operation_code == op_code.SET_USER_INFO:
        # 13.set_user_info()
        op.set_user_info(data.name, data.signature, data.favcion, data.password, data.phone, data.last_login)
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/update")
def post_code_pwd(code_pwd: CodePwd):
    global response_json
    response = response_json
    data = code_pwd.data
    if code_pwd.operation_code == op_code.UPDATE_USER_INFO:
        # 14.update_user_info()
        op.update_user_info(data.user_id, data.password)
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/search")
def post_code_index(code_search: CodeSearch):
    if code_search.operation_code == op_code.SEARCH:
        # 23.search()
        pass
    else:
        # error
        pass
    return code_search


@app.post("/filter")
def post_code_filter(code_filter: CodeFilter):
    global response_json
    response = response_json
    data = code_filter.data
    if code_filter.operation_code == op_code.FILTER:
        # 24.filter()
        response["data"] = op.filter(data.market, data.publisher, data.category, data.industry, data.area)
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/stock")
def post_code_stock(code_stock: CodeStock):
    global response_json
    response = response_json
    data = code_stock.data
    if code_stock.operation_code == op_code.GET_STOCK_INFO:
        # 25.get_stock_info()
        response["data"] = op.get_stock_info(data.stock_code)
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/collection")
def post_code_collection(code_collection: CodeCollection):
    global response_json
    response = response_json
    print(response)
    data = code_collection.data
    if code_collection.operation_code == op_code.SET_COLLECTION:
        # 26.set_collection()
        op.set_collection(data.user_id, data.stock_info_id)
        return response
    elif code_collection.operation_code == op_code.DELETE_COLLECTION:
        # 27.delete_collection()
        op.delete_collection(data.user_id, data.stock_info_id)
        return response
    else:
        # error
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


uvicorn.run(app, host='127.0.0.1', port=8000)

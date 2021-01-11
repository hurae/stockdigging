from typing import List
# from datetime import datetime
# from storage.business.server import json_handle
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import status_code

app = FastAPI()
op_code = status_code.OpCode()
err_code = status_code.ErrorCode()


# only send operation_code
class Code(BaseModel):
    operation_code: int


class Opinion(BaseModel):
    public_index: float


class CodeOpinion(Code):
    data: Opinion


class Increase(BaseModel):
    prediction: float


class CodeIncrease(Code):
    data: Increase


class CodeInfo(Code):
    data: List[List]


class Comment(BaseModel):
    ts_code: int
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
    favcion: str
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
    market: str
    publisher: str
    category: str
    industry: str
    area: str


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
    if code.operation_code == op_code.GET_ALL_COMMENT:
        # 1.get_all_comment()
        pass
    elif code.operation_code == op_code.GET_TODAY_COMMENT:
        # 2.get_today_comment()
        pass
    elif code.operation_code == op_code.GET_INDUSTRY_INDEX_PREDICTION:
        # 16.get_industry_index_prediction()
        pass
    elif code.operation_code == op_code.GET_MARKET_INDEX_PREDICTION:
        # 17.get_market_index_prediction()
        pass
    elif code.operation_code == op_code.GET_STOCK_PREDICTION:
        # 18.get_stock_prediction()
        pass
    elif code.operation_code == op_code.GET_INDEX_FEATURE_HISTORY:
        # 19.get_index_feature_history()
        pass
    elif code.operation_code == op_code.GET_STOCK_FEATURE_HISTORY:
        # 20.get_stock_feature_history()
        pass
    elif code.operation_code == op_code.GET_INDEX_FEATURE_TODAY:
        # 21.get_index_feature_today()
        pass
    elif code.operation_code == op_code.GET_STOCK_FEATURE_TODAY:
        # 22.get_stock_feature_today()
        pass
    else:
        # error
        pass

    return code


@app.post("/opinion")
def post_code_opinion(code_opinion: CodeOpinion):
    if code_opinion.operation_code == op_code.SET_PUBLIC_OPINION:
        # 3.set_public_opinion()
        pass
    else:
        # error
        pass
    return code_opinion


@app.post("/increase")
def post_code_prediction(code_increase: CodeIncrease):
    if code_increase.operation_code == op_code.SET_INCREASE_RATE:
        # 4.set_increase_rate()
        pass
    elif code_increase.operation_code == op_code.SET_INDEX_PREDICTION:
        # 5.set_index_prediction()
        pass
    else:
        # error
        pass
    return code_increase


@app.post("/info")
def post_code_info(code_info: CodeInfo):
    if code_info.operation_code == op_code.SET_INDEX_INFO:
        # 6.set_index_info()
        pass
    elif code_info.operation_code == op_code.SET_STOCK_INFO:
        # 7.set_stock_info()
        pass
    elif code_info.operation_code == op_code.SET_INDEX_DAILY:
        # 8.set_index_daily()
        pass
    elif code_info.operation_code == op_code.SET_STOCK_DAILY:
        # 9.set_stock_daily()
        pass
    else:
        # error
        pass
    return code_info


@app.post("/comment")
def post_code_comment(code_comment: CodeComment):
    if code_comment.operation_code == op_code.SET_STOCK_COMMENT:
        # 10.set_stock_comment()
        pass
    elif code_comment.operation_code == op_code.SET_INDEX_COMMENT:
        # 11.set_index_comment()
        pass
    else:
        # error
        pass
    return code_comment


@app.post("/userid")
def post_code_userid(code_userid: CodeUserid):
    if code_userid.operation_code == op_code.GET_USER_INFO:
        # 12.get_user_info()
        pass
    elif code_userid.operation_code == op_code.DELETE_USER_INFO:
        # 15.delete_user_info()
        pass
    else:
        # error
        pass
    return code_userid


@app.post("/new")
def post_code_userinfo(code_userinfo: CodeUserinfo):
    if code_userinfo.operation_code == op_code.SET_USER_INFO:
        # 13.set_user_info()
        pass
    else:
        # error
        pass
    return code_userinfo


@app.post("/update")
def post_code_pwd(code_pwd: CodePwd):
    if code_pwd.operation_code == op_code.UPDATE_USER_INFO:
        # 14.update_user_info()
        pass
    else:
        # error
        pass
    return code_pwd


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
    if code_filter.operation_code == op_code.FILTER:
        # 24.filter()
        pass
    else:
        # error
        pass
    return code_filter


@app.post("/stock")
def post_code_stock(code_stock: CodeStock):
    if code_stock.operation_code == op_code.GET_STOCK_INFO:
        # 25.get_stock_info()
        pass
    else:
        # error
        pass
    return code_stock


@app.post("/collection")
def post_code_collection(code_collection: CodeCollection):
    if code_collection.operation_code == op_code.SET_COLLECTION:
        # 26.set_collection()
        pass
    elif code_collection.operation_code == op_code.DELETE_COLLECTION:
        # 27.delete_collection()
        pass
    else:
        # error
        pass


uvicorn.run(app, host='127.0.0.1', port=8000)

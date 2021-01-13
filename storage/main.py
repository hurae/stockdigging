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


# response general
def rg():
    return {
        "error_code": err_code.SUCCESS,
        "error_message": err_code.error_msg[err_code.SUCCESS]
    }


# only send operate_code
class Code(BaseModel):
    operate_code: int


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
    search: str


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
async def post_code(code: Code):
    
    global flag, flag1
    global flag2, flag3
    if code.operate_code == op_code.GET_ALL_COMMENT:
        response = rg()
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
    elif code.operate_code == op_code.GET_TODAY_COMMENT:
        response = rg()
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
    elif code.operate_code == op_code.GET_INDUSTRY_INDEX_PREDICTION:
        response = rg()
        # 16.get_industry_index_prediction()
        response["data"] = op.get_industry_index_prediction()
        return response
    elif code.operate_code == op_code.GET_MARKET_INDEX_PREDICTION:
        response = rg()
        # 17.get_market_index_prediction()
        response["data"] = op.get_market_index_prediction()
        return response
    elif code.operate_code == op_code.GET_STOCK_PREDICTION:
        response = rg()
        # 18.get_stock_prediction()
        response["data"] = op.get_stock_prediction()
        return response
    elif code.operate_code == op_code.GET_INDEX_FEATURE_HISTORY:
        response = rg()
        # 19.get_index_feature_history()
        print( flag3 )
        if flag3 < length3:
            data = op.get_index_feature_history(flag3)
            flag3 = flag3 + 1
            response["data"] = data
            print(response)
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
    elif code.operate_code == op_code.GET_STOCK_FEATURE_HISTORY:
        response = rg()
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
    elif code.operate_code == op_code.GET_INDEX_FEATURE_TODAY:
        response = rg()
        # 21.get_index_feature_today()
        data = []
        for i in range(length3):
            data.append(op.get_index_feature_today(i))
        response["data"] = data
        return response
    elif code.operate_code == op_code.GET_STOCK_FEATURE_TODAY:
        response = rg()
        # 22.get_stock_feature_today()
        data = []
        for i in range(length2):
            data.append(op.get_stock_feature_today(i))
        response["data"] = data
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/opinion")
async def post_code_opinion(code_opinion: CodeOpinion):
    global flag
    global flag1
    
    if code_opinion.operate_code == op_code.SET_PUBLIC_OPINION:
        response = rg()
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
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/increase")
async def post_code_prediction(code_increase: CodeIncrease):
    global length2, length3
    if code_increase.operate_code == op_code.SET_INCREASE_RATE:
        response = rg()
        # 4.set_increase_rate()
        prediction = code_increase.data.prediction
        for i in range(length2):
            op.set_increase_rate(i, prediction[i])
        return response
    elif code_increase.operate_code == op_code.SET_INDEX_PREDICTION:
        response = rg()
        # 5.set_index_prediction()
        prediction = code_increase.data.prediction
        for i in range(length3):
            op.set_index_prediction(i, prediction[i])
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/info")
async def post_code_info(code_info: CodeInfo):
    
    if code_info.operate_code == op_code.SET_INDEX_INFO:
        response = rg()
        # 6.set_index_info()
        for r in code_info.data:
            print(r)
            op.set_index_info(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12])
        return response
    elif code_info.operate_code == op_code.SET_STOCK_INFO:
        response = rg()
        # 7.set_stock_info()
        for r in code_info.data:
            op.set_stock_info(r[0], r[1], r[2], r[3], r[4], r[5])
        return response
    elif code_info.operate_code == op_code.SET_INDEX_DAILY:
        response = rg()
        # 8.set_index_daily()
        for r in code_info.data:
            op.set_index_state(r[0], r[1], r[2], r[3], r[4], r[5])
        return response
    elif code_info.operate_code == op_code.SET_STOCK_DAILY:
        response = rg()
        # 9.set_stock_daily()
        for r in code_info.data:
            op.set_stock_state(r[0], r[1], r[2], r[3], r[4], r[5])
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return code_info


@app.post("/comment")
async def post_code_comment(code_comment: CodeComment):
    
    data = code_comment.data
    if code_comment.operate_code == op_code.SET_STOCK_COMMENT:
        response = rg()
        # 10.set_stock_comment()
        op.set_stock_comment(data.ts_code, data.content, data.comment_date, data.num)
        return response
    elif code_comment.operate_code == op_code.SET_INDEX_COMMENT:
        response = rg()
        # 11.set_index_comment()
        op.set_index_comment(data.ts_code, data.content, data.comment_date, data.num)
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return code_comment


@app.post("/userid")
async def post_code_userid(code_userid: CodeUserid):
    
    data = code_userid.data
    if code_userid.operate_code == op_code.GET_USER_INFO:
        response = rg()
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
    elif code_userid.operate_code == op_code.DELETE_USER_INFO:
        response = rg()
        # 15.delete_user_info()
        op.delete_user_info(data.user_id)
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/new")
async def post_code_userinfo(code_userinfo: CodeUserinfo):
    
    data = code_userinfo.data
    if code_userinfo.operate_code == op_code.SET_USER_INFO:
        response = rg()
        # 13.set_user_info()
        op.set_user_info(data.name, data.signature, data.favcion, data.password, data.phone, data.last_login)
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/update")
async def post_code_pwd(code_pwd: CodePwd):
    
    data = code_pwd.data
    if code_pwd.operate_code == op_code.UPDATE_USER_INFO:
        response = rg()
        # 14.update_user_info()
        op.update_user_info(data.user_id, data.password)
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/search")
async def post_code_index(code_search: CodeSearch):
    
    if code_search.operate_code == op_code.SEARCH:
        response = rg()
        # 23.search()
        data = op.search(code_search.data.search)
        response["data"] = data
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/filter")
async def post_code_filter(code_filter: CodeFilter):
    
    data = code_filter.data
    if code_filter.operate_code == op_code.FILTER:
        response = rg()
        # 24.filter()
        response["data"] = op.filter(data.market, data.publisher, data.category, data.industry, data.area)
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/stock")
async def post_code_stock(code_stock: CodeStock):
    
    data = code_stock.data
    if code_stock.operate_code == op_code.GET_STOCK_INFO:
        response = rg()
        # 25.get_stock_info()
        response["data"] = op.get_stock_info(data.stock_code)
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


@app.post("/collection")
async def post_code_collection(code_collection: CodeCollection):
    
    data = code_collection.data
    if code_collection.operate_code == op_code.SET_COLLECTION:
        response = rg()
        # 26.set_collection()
        op.set_collection(data.user_id, data.stock_info_id)
        return response
    elif code_collection.operate_code == op_code.DELETE_COLLECTION:
        response = rg()
        # 27.delete_collection()
        op.delete_collection(data.user_id, data.stock_info_id)
        return response
    else:
        # error
        response = rg()
        response["error_code"] = err_code.INTERNAL_ERROR
        response["error_message"] = err_code.error_msg[err_code.INTERNAL_ERROR]
        return response


uvicorn.run(app, host='0.0.0.0', port=8000)

from sqlalchemy.orm import sessionmaker, relationship

from storage.operation import models
from storage.operation.models import IndexInfo, StockInfo, IndexPoint, StockPrice, StockComment, IndexComment, \
    StockPopular, IndexPopular, StockPopular, User
from digging_utils import get_year_format, get_today_format, get_yesterday
import random, string

# if __name__ == "__main__":
Session = sessionmaker( bind=models.engine )
session = Session()

# 查询股票评论的全局变量
d = {}
query = session.query( StockInfo.ts_code, StockComment.comment_date ).all()
ans = [ele for ele in (map( lambda item: (item[0], item[1].strftime( "%Y-%m-%d" )), query ))]
answer = d.fromkeys( ans )
answer = answer.keys()
answer = list( answer )
length = len( answer )
flag = 0

# 查询指数评论的全局变量(带1)
query1 = session.query( IndexInfo.ts_code, IndexComment.comment_date ).all()
ans1 = [ele for ele in (map( lambda item: (item[0], item[1].strftime( "%Y-%m-%d" )), query1 ))]
answer1 = d.fromkeys( ans1 )
answer1 = answer1.keys()
answer1 = list( answer1 )
length1 = len( answer1 )
flag1 = 0

# 查询股票价格的全局变量——股票tscode
query2 = session.query( StockInfo.ts_code ).all()
ans2 = [ele for ele in (map( lambda item: (item[0]), query2 ))]
length2 = len( ans2 )
flag2 = 0

# 查询指数价格的全局变量——指数tscode
query3 = session.query( IndexInfo.ts_code ).all()
ans3 = [ele for ele in (map( lambda item: (item[0]), query3 ))]
length3 = len( ans3 )
flag3 = 0


# operation 6 插入指数信息
def set_index_info(ts_code, name, fullname, market, publisher, index_type, category, base_date, base_point, list_date,
                   weight_rule, desc, exp_date):
    row_obj = IndexInfo( ts_code=ts_code,
                         name=name,
                         fullname=fullname,
                         market=market,
                         publisher=publisher,
                         index_type=index_type,
                         category=category,
                         base_date=base_date,
                         base_point=base_point,
                         list_date=base_date,
                         weight_rule=weight_rule,
                         desc=desc,
                         exp_date=exp_date )
    session.add( row_obj )
    session.commit()


# set_index_info('123', '测试1', '345', 'y1', '23', '23', '8', '1999-09-10', 0.9, '1999-2-2', 0.9, '9', '2020-2-2')


# operation 7 插入股票信息
def set_stock_info(ts_code, stock_name, stock_code, list_data, area, industry):
    row_obj = StockInfo( ts_code=ts_code,
                         stock_name=stock_name,
                         stock_code=stock_code,
                         list_data=list_data,
                         area=area,
                         industry=industry )
    session.add( row_obj )
    session.commit()


# set_stock_info('123', '测试3', '345', '1999-9-9', '23', '23')


# extract_index_id:通过ts_code查询指数id
def extract_index_id(ts_code):
    res = session.execute( session.query( IndexInfo.id ).filter( IndexInfo.ts_code == ts_code ) ).fetchall()[0][0]
    print( "通过ts_code查询到的指数id：", res )
    return res


# operation 8 插入指数行情
def set_index_state(ts_code, trade_date, close, open, high, low):
    # 1.先调用函数extract_index_id()查询ts_code对应的指数信息表的index_info_id。
    # 2.将此index_info_id对应的其他数据信息插入到指数行情表

    row_obj = IndexPoint( index_info_id=extract_index_id( ts_code ),
                          trade_date=trade_date,
                          close=close,
                          open=open,
                          high=high,
                          low=low,
                          today_ave=(open + close) / 2,
                          )
    session.add( row_obj )
    session.query( IndexPoint ).filter( IndexPoint.index_info_id == extract_index_id( ts_code ),
                                        IndexPoint.trade_date == get_yesterday() ).update(
        {"tom_ave": (open + close) / 2} )

    session.commit()


# set_index_state('zhishu2', '2020-1-1', 1.1, 2.1, 1.0, 1.1)


# extract_stock_id:通过ts_code查询股票id
def extract_stock_id(ts_code):
    res = session.execute( session.query( StockInfo.id ).filter( StockInfo.ts_code == ts_code ) ).fetchall()[0][0]
    # print( "通过ts_code查询到的股票id：", res )
    return res


# operation 9 插入股票行情:股价表
def set_stock_state(ts_code, trade_date, open, high, low, close):
    row_obj = StockPrice( stock_info_id=extract_stock_id( ts_code ),
                          trade_date=trade_date,
                          open=open,
                          high=high,
                          low=low,
                          close=close,
                          today_ave=(open + close) / 2 )
    session.add( row_obj )
    session.query( StockPrice ).filter( StockPrice.stock_info_id == extract_stock_id( ts_code ),
                                        StockPrice.trade_date == get_yesterday() ).update(
        {"tom_ave": (open + close) / 2} )
    session.commit()


# set_stock_state('gupiao1', '2020-1-1', 1.1, 2.1, 1.0, 1.1)


# operation 10 写入股票评论:股票评论表、股票热度表
def set_stock_comment(ts_code, content, comment_date, num):
    row1_obj = StockComment( stock_info_id=extract_stock_id( ts_code ),
                             content=content,
                             comment_date=comment_date )
    session.add( row1_obj )
    row2_obj = StockPopular( stock_info_id=extract_stock_id( ts_code ),
                             num=num,
                             comment_date=comment_date )
    session.add( row2_obj )
    session.commit()


# set_stock_comment('gupiao4', 'great!','2020-1-1',12394)


# operation 11 写入指数评论:指数评论表（内容、时间）、指数热度表（时间、阅读量）
def set_index_comment(ts_code, content, comment_date, num):
    row1_obj = IndexComment( index_info_id=extract_index_id( ts_code ),
                             content=content,
                             comment_date=comment_date )
    session.add( row1_obj )
    row2_obj = IndexPopular( index_info_id=extract_index_id( ts_code ),
                             num=num,
                             comment_date=comment_date )
    session.add( row2_obj )
    session.commit()


# set_index_comment('zhishu3', 'bad!','2020-1-1',1734)

# operation 1 查看历史所有评论
def get_stock_all_comment(flag):
    # 每只股票每日评论
    res = session.execute( session.query( StockComment.content ).filter(
        StockInfo.ts_code == answer[flag][0],
        StockComment.stock_info_id == StockInfo.id,
        get_year_format() < answer[flag][1],
        answer[flag][1] < get_today_format() ) ).fetchall()
    data = [r[0] for r in res]
    print( "第", flag, "条数据：", data )
    return data


# get_stock_all_comment(16)

def get_index_all_comment(flag1):
    # 每个指数每日评论
    res = session.execute( session.query( IndexComment.content ).filter(
        IndexInfo.ts_code == answer1[flag1][0],
        IndexComment.index_info_id == IndexInfo.id,
        get_year_format() < answer1[flag1][1],
        answer1[flag1][1] < get_today_format() ) ).fetchall()
    data = [r[0] for r in res]
    print( "第", flag1, "条数据：", data )
    return data


# get_index_all_comment( 13 )

# operation 2 查看今天所有评论
def get_stock_today_comment(flag2):
    # 每只股票今日评论
    res = session.execute( session.query( StockComment.content ).filter(
        StockInfo.ts_code == ans2[flag2],
        StockComment.stock_info_id == StockInfo.id,
        StockComment.comment_date == get_today_format() ) ).fetchall()
    data = [r[0] for r in res]
    print( "第", flag2, "条数据：", data )
    return data


# get_stock_today_comment(3)

def get_index_today_comment(flag3):
    # 每个指数今日评论
    res = session.execute( session.query( IndexComment.content ).filter(
        IndexInfo.ts_code == ans3[flag3],
        IndexComment.index_info_id == IndexInfo.id,
        IndexComment.comment_date == get_today_format() ) ).fetchall()
    data = [r[0] for r in res]
    print( "第", flag3, "条数据：", data )
    return data


# get_index_today_comment(2)

# 操作码3 写入舆情指数（股票评论热度表）
def set_stock_public_opinion(flag, public_index):
    session.query( StockPopular ).filter(
        StockPopular.stock_info_id == extract_stock_id( answer[flag][0] ),
        answer[flag][1] == StockPopular.comment_date ).update(
        {"public_index": public_index} )
    session.commit()
    print( extract_stock_id( answer[flag][0] ) )
    print( answer[flag][1] )


# set_stock_public_opinion( 16, 3.4 )

def set_index_public_opinion(flag1, public_index):
    session.query( IndexPopular ).filter(
        IndexPopular.index_info_id == extract_index_id( answer1[flag1][0] ),
        answer1[flag1][1] == IndexPopular.comment_date ).update(
        {"public_index": public_index} )
    session.commit()
    print( extract_index_id( answer1[flag1][0] ) )
    print( answer1[flag1][1] )


# set_index_public_opinion( 13, 3.4 )


# 操作码13 建立用户信息
def set_user_info(name, signature, favcion, password, phone, last_login):
    salting = ''.join( random.sample( string.ascii_letters + string.digits, 8 ) )
    row_obj = User( name=name,
                    signature=signature,
                    favcion=favcion,
                    password=password,
                    phone=phone,
                    last_login=last_login,
                    salt=salting,
                    state=0 )

    session.add( row_obj )
    session.commit()


# set_user_info('小明','ming',34,'okkkkkk','1736299','19980809')
# 操作码14 修改用户密码 UPDATE_USER_INFO
def update_user_info(id, password):
    salt = session.execute( session.query( User.salt ).filter( User.id == id ) ).fetchall()[0][0]
    print( salt )
    new_password = password + salt
    session.query( User ).filter( User.id == id ).update( {"password": new_password} )
    session.commit()


# update_user_info(2,'mima')
ans1 = [ele for ele in (map( lambda item: (item[0], item[1].strftime( "%Y-%m-%d" )), query1 ))]


# 操作码12 读取用户信息

def get_user_info(id):
    res = session.execute(
        session.query( User.name, User.signature, User.favcion, User.state, User.password, User.phone,
                       User.last_login ).filter(
            User.id == id ) ).fetchall()
    data = [ele for ele in (
        map( lambda item: (item[0], item[1], item[2], item[3], item[4], item[5], item[6].strftime( "%Y-%m-%d" )),
             res ))]
    print( data )
    return data


# get_user_info(2)

# 操作码15 删除用户
def delete_user_info(id):
    session.query( User ).filter( User.id == id ).update( {"state": 2} )
    session.commit()


# delete_user_info(3)


# 操作码20 获取股票特征四元组(舆情指数，热度，今日平均，明日平均）
def get_stock_feature_history(flag2):
    res = session.execute(
        session.query( StockPopular.num, StockPopular.public_index, StockPrice.today_ave, StockPrice.tom_ave ).filter(
            StockInfo.ts_code == ans2[flag2],
            StockPopular.stock_info_id== StockInfo.id,
            StockPrice.stock_info_id == StockInfo.id,
            # get_year_format() < StockPrice.trade_date,
            # StockPrice.trade_date < get_today_format()
        ) ).fetchall()
    print(res)
    data = [r[0] for r in res]
    print( "第", flag2, "条数据：", data )
    return data

get_stock_feature_history(2)
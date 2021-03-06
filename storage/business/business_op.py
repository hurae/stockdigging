from sqlalchemy.orm import sessionmaker, relationship

from storage.operation import models
from storage.operation.models import IndexInfo, StockInfo, IndexPoint, StockPrice, StockComment, IndexComment, \
    StockPopular, IndexPopular, StockPopular, User, StockForecast, IndexForecast, Collection
from digging_utils import get_year_format, get_today_format, get_yesterday
import random, string, hashlib

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
#print(length3)

def stock_tscode():
    query2 = session.query(StockInfo.ts_code).all()
    ans2 = [ele for ele in (map(lambda item: (item[0]), query2))]
    length2 = len(ans2)
    return ans2, length2


def index_tscode():
    query3 = session.query(IndexInfo.ts_code).all()
    ans3 = [ele for ele in (map(lambda item: (item[0]), query3))]
    length3 = len(ans3)
    return ans3,length3


# extract_stock_id:通过ts_code查询股票id
def extract_stock_id(ts_code):
    res = session.execute( session.query( StockInfo.id ).filter( StockInfo.ts_code == ts_code ) ).fetchall()
    if len( res ) == 0:
        # print( "stock:ts_code不存在！" )
        return 0
    else:
        res = session.execute( session.query( StockInfo.id ).filter( StockInfo.ts_code == ts_code ) ).fetchall()[0][0]
        # print( "通过ts_code查询到的股票id：", res )
        return res


# extract_stock_id( "123" )

# extract_index_id:通过ts_code查询指数id
def extract_index_id(ts_code):
    res = session.execute( session.query( IndexInfo.id ).filter( IndexInfo.ts_code == ts_code ) ).fetchall()
    if len( res ) == 0:
        # print( "index：ts_code不存在！" )
        return 0
    else:
        res = session.execute( session.query( IndexInfo.id ).filter( IndexInfo.ts_code == ts_code ) ).fetchall()[0][0]
        # print( "通过ts_code查询到的股票id：", res )
        return res


# extract_index_id("zhishu1")


# operation 6 插入指数信息
def set_index_info(ts_code, name, fullname, market, publisher, index_type, category, base_date, base_point, list_date,
                   weight_rule, desc, exp_date):
    if extract_index_id( ts_code ) != 0:
        session.query( IndexInfo ).filter( IndexInfo.ts_code == ts_code ).update(
            {"name": name, "fullname": fullname, "market": market, "publisher": publisher, "index_type": index_type,
             "category": category, "base_date": base_date, "base_point": base_point, "list_date": list_date,
             "weight_rule": weight_rule, "desc": desc, "exp_date": exp_date} )
    else:
        row_obj = IndexInfo( ts_code=ts_code,
                             name=name,
                             fullname=fullname,
                             market=market,
                             publisher=publisher,
                             index_type=index_type,
                             category=category,
                             base_date=base_date,
                             base_point=base_point,
                             list_date=list_date,
                             weight_rule=weight_rule,
                             desc=desc,
                             exp_date=exp_date )
        session.add( row_obj )
    session.commit()

# set_index_info('zhishu9', '测试2', '345', 'y2', '23', '23', '8', '1999-09-10', 0.9, '1999-2-2', 0.9, '9', '2020-2-2')


# operation 7 插入股票信息
def set_stock_info(ts_code, stock_code,stock_name,area, industry, list_data):
    if extract_stock_id( ts_code ) != 0:
        session.query( StockInfo ).filter( StockInfo.ts_code == ts_code ).update(
            {"stock_name": stock_name, "stock_code": stock_code, "list_data": list_data, "area": area,
             "industry": industry} )
    else:
        row_obj = StockInfo( ts_code=ts_code,
                             stock_name=stock_name,
                             stock_code=stock_code,
                             list_data=list_data,
                             area=area,
                             industry=industry )
        session.add( row_obj )
    session.commit()


#set_stock_info('12', '测试9', '45', '23', '23','1999-9-9')


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
                                        IndexPoint.trade_date == get_yesterday( trade_date ) ).update(
        {"tom_ave": (open + close) / 2} )

    session.commit()


# set_index_state('zhishu2', '2020-1-1', 1.1, 2.1, 1.0, 1.1)


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
                                        StockPrice.trade_date == get_yesterday( trade_date ) ).update(
        {"tom_ave": (open + close) / 2} )
    session.commit()


# set_stock_state('gupiao1', '2020-1-1', 1.1, 2.1, 1.0, 1.1)


# operation 10 写入股票评论:股票评论表、股票热度表
def set_stock_comment(ts_code, content, comment_date, num):
    for c in content:
        row1_obj = StockComment( stock_info_id=extract_stock_id( ts_code ),
                                 content=c,
                                 comment_date=comment_date )
        session.add( row1_obj )
    row2_obj = StockPopular( stock_info_id=extract_stock_id( ts_code ),
                             num=num,
                             comment_date=comment_date )
    session.add( row2_obj )
    session.commit()


# set_stock_comment('gupiao4', ['great!',],'2020-1-1',12394)


# operation 11 写入指数评论:指数评论表（内容、时间）、指数热度表（时间、阅读量）
def set_index_comment(ts_code, content, comment_date, num):
    for c in content:
        row1_obj = IndexComment( index_info_id=extract_index_id( ts_code ),
                                 content=c,
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


# set_stock_public_opinion( 1, 3.4 )

def set_index_public_opinion(flag1, public_index):
    session.query( IndexPopular ).filter(
        IndexPopular.index_info_id == extract_index_id( answer1[flag1][0] ),
        answer1[flag1][1] == IndexPopular.comment_date ).update(
        {"public_index": public_index} )
    session.commit()


# set_index_public_opinion( 13, 3.4 )


# 操作码13 建立用户信息
def set_user_info(name, signature, favcion, password, phone, last_login):
    salting = ''.join( random.sample( string.ascii_letters + string.digits, 8 ) )
    new_password = password + salting
    new_password = hashlib.sha256( new_password.encode() ).hexdigest()
    ans = session.execute( session.query( User.phone ).filter( User.phone == phone ) ).fetchall()
    if len( ans ) != 0:
        print( "手机号已经注册！" )
    else:
        row_obj = User( name=name,
                        signature=signature,
                        favcion=favcion,
                        password=new_password,
                        phone=phone,
                        last_login=last_login,
                        salt=salting,
                        state=0 )

        session.add( row_obj )
        session.commit()


# et_user_info('小明','ming',34,'okkkkkk','1736299','19980809')

# 操作码14 修改用户密码 UPDATE_USER_INFO
def update_user_info(id, password):
    salt = session.execute( session.query( User.salt ).filter( User.id == id ) ).fetchall()[0][0]
    print( salt )
    new_password = password + salt
    new_password = hashlib.sha256( new_password.encode() ).hexdigest()
    session.query( User ).filter( User.id == id ).update( {"password": new_password} )
    session.commit()


# update_user_info(2,'mima')

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

# 操作码15 删除用户，不直接删除，设为状态2
def delete_user_info(id):
    session.query( User ).filter( User.id == id ).update( {"state": 2} )
    session.commit()


# delete_user_info(3)


# 操作码20 获取股票特征四元组(舆情指数，热度，今日平均，明日平均）
def get_stock_feature_history(flag2):
    res = session.execute(
        session.query( StockPopular.public_index, StockPopular.num, StockPrice.today_ave, StockPrice.tom_ave ).filter(
            StockInfo.ts_code == ans2[flag2],
            StockPopular.stock_info_id == StockInfo.id,
            StockPrice.stock_info_id == StockInfo.id,
            get_year_format() < StockPrice.trade_date,
            StockPrice.trade_date < get_today_format()
        ) ).fetchall()
    data = []
    for r in res:
        data.append( list( r ) )
    print( data )
    return data


# get_stock_feature_history(2)

# 操作码19 获取指数特征四元组(舆情指数，热度，今日平均，明日平均）
def get_index_feature_history(flag3):
    res = session.execute(
        session.query( IndexPopular.public_index, IndexPopular.num, IndexPoint.today_ave, IndexPoint.tom_ave ).filter(
            IndexInfo.ts_code == ans3[flag3],
            IndexPopular.index_info_id == IndexInfo.id,
            IndexPoint.index_info_id == IndexInfo.id,
            get_year_format() < IndexPoint.trade_date,
            IndexPoint.trade_date < get_today_format()
        ) ).fetchall()
    data = []
    for r in res:
        data.append( list( r ) )
    print( data )
    return data


# get_index_feature_history(1)

# 操作码22 获取今日股票二元组（热度，舆情指数） 数据库中一定要有股票的今日数据
def get_stock_feature_today(flag2):
    try:
        res = session.execute(
            session.query( StockPopular.public_index, StockPopular.num ).filter(
                StockInfo.ts_code == ans2[flag2],
                StockPopular.stock_info_id == StockInfo.id,
                StockPopular.comment_date == get_today_format()
            ) ).fetchall()
        data = list( res[0] )
        print( data )
        return data
    except:
        data = [0, 0]
        print( data )
        return data


# get_stock_feature_today( 1 )


# 操作码21 获取今日指数二元组（热度，舆情指数）
def get_index_feature_today(flag3):
    try:
        res = session.execute(
            session.query( IndexPopular.public_index, IndexPopular.num ).filter(
                IndexInfo.ts_code == ans3[flag3],
                IndexPopular.index_info_id == IndexInfo.id,
                IndexPopular.comment_date == get_today_format()
            ) ).fetchall()
        data = list( res[0] )
        print( data )
        return data
    except:
        data = [0, 0]
        print( data )
        return data


# get_index_feature_today( 1 )

# 操作码4 写入股价预测增长率（股票预测结果表）
def set_increase_rate(flag2, forecast):
    row_obj = StockForecast( stock_info_id=extract_stock_id( ans2[flag2] ),
                             trade_date=get_today_format(),
                             forecast=forecast )
    session.add( row_obj )
    session.commit()


# set_increase_rate(2,10.45)

# 操作码5 写入指数分析结果（指数预测结果表）
def set_index_prediction(flag3, forecast):
    row_obj = IndexForecast( index_info_id=extract_index_id( ans3[flag3] ),
                             trade_date=get_today_format(),
                             forecast=forecast )
    session.add( row_obj )
    session.commit()


# set_index_prediction(2,10.45)

# 操作码18 查看个股预测结果(返回所有股票二元组：股票名称，预测结果)
def get_stock_prediction():
    res = session.execute(
        session.query( StockInfo.stock_name,
                       StockForecast.forecast ).filter( StockForecast.stock_info_id == StockInfo.id ) ).fetchall()
    data = []
    for r in res:
        data.append( list( r ) )
    print( data )
    return data


# get_stock_prediction()

# 操作码25查看个股详细信息（股票详情+每日行情）一共有多天
def get_stock_info(stock_code):
    res = session.execute( session.query( StockInfo.id ).filter( StockInfo.stock_code == stock_code ) ).fetchall()[0][0]
    ans = session.execute(
        session.query( StockInfo, StockPrice, StockForecast ).filter( StockInfo.id == res,
                                                                      StockPrice.stock_info_id == res,
                                                                      StockForecast.stock_info_id == res ) ).fetchall()
    data = [ele for ele in (
        map( lambda item: (item[2], item[3], item[4].strftime( "%Y-%m-%d" ), item[5], item[6],
                           item[9].strftime( "%Y-%m-%d" ), item[10], item[11], item[12], item[13], item[14], item[19]),
             ans ))]
    data1 = []
    for r in data:
        data1.append( list( r ) )
    print( data1 )
    return data1


# get_stock_info( '333' )
# 操作码16 查看行业指数预测结果 返回名字和预测结果
def get_industry_index_prediction():
    res = session.execute(
        session.query( IndexInfo.name, IndexForecast.forecast ).filter(
            IndexInfo.category == "行业指数", IndexInfo.id == IndexForecast.index_info_id ) ).fetchall()
    data = []
    for r in res:
        data.append( list( r ) )
    print( data )
    return data


# get_industry_index_prediction()

# 操作码17 查看大盘指数预测结果
def get_market_index_prediction():
    res = session.execute(
        session.query( IndexInfo.name, IndexForecast.forecast ).filter(
            IndexInfo.category == "综合指数", IndexInfo.id == IndexForecast.index_info_id ) ).fetchall()
    data = []
    for r in res:
        data.append( list( r ) )
    print( data )
    return data


# get_market_index_prediction()

# 队列-->列表
def return_list(res):
    data = []
    for r in res:
        data.append( list( r ) )
    print( data )
    return data


# 操作码24 筛选合适的股票或指数 五个参数"market":"","publisher":"","category":"","industry":"","area"
# 返回名称，预测值
def filter(market, publisher, category, industry, area):
    if market != "":
        res = session.execute(
            session.query( IndexInfo.name, IndexForecast.forecast ).filter( IndexInfo.market == market ) ).fetchall()
        return return_list( res )
    elif publisher != "":
        res = session.execute(
            session.query( IndexInfo.name, IndexForecast.forecast ).filter(
                IndexInfo.publisher == publisher ) ).fetchall()
        return return_list( res )
    elif area != "":
        res = session.execute(
            session.query( StockInfo.stock_name, StockForecast.forecast ).filter( StockInfo.area == area ) ).fetchall()
        return return_list( res )
    elif industry != "":
        res = session.execute( session.query( StockInfo.stock_name, StockForecast.forecast ).filter(
            StockInfo.industry == industry ) ).fetchall()
        return return_list( res )
    elif category != "":
        res = session.execute(
            session.query( IndexInfo.name, IndexForecast.forecast ).filter(
                IndexInfo.category == category ) ).fetchall()
        return return_list( res )


# filter("","","","","深圳")

# 操作码23 搜索股票或指数 数据有重复
# index:ts_code/name和stock:ts_code/name
# 返回ts_code/name
def search(string):
    res = session.execute(
        session.query( IndexInfo.ts_code, IndexInfo.name ).filter(
            IndexInfo.ts_code.like( "%" + string + "%" ) ) ).fetchall()

    res1 = session.execute(
        session.query( IndexInfo.ts_code, IndexInfo.name ).filter(
            IndexInfo.name.like( "%" + string + "%" ) ) ).fetchall()

    res2 = session.execute(
        session.query( StockInfo.ts_code, StockInfo.stock_name ).filter(
            StockInfo.ts_code.like( "%" + string + "%" ) ) ).fetchall()

    res3 = session.execute(
        session.query( StockInfo.ts_code, StockInfo.stock_name ).filter(
            StockInfo.stock_name.like( "%" + string + "%" ) ) ).fetchall()
    data = []
    for r in res:
        data.append( r )
    for r1 in res1:
        data.append( r1 )
    for r2 in res2:
        data.append( r2 )
    for r3 in res3:
        data.append( r3 )
    ans = [ele for ele in (map( lambda item: (item[0], item[1]), data ))]
    answer = d.fromkeys( ans )
    answer = answer.keys()
    answer = list( answer )
    print( answer )
    return answer


# search( "gu" )

# 操作码26 添加收藏
def set_collection(user_id, stock_info_id):
    ans = session.execute(
        session.query( Collection.user_id, Collection.stock_info_id ).filter( Collection.user_id == user_id,
                                                                              Collection.stock_info_id == stock_info_id ) ).fetchall()
    if len( ans ) != 0:
        print( "收藏已存在", ans )
    else:
        row_obj = Collection( user_id=user_id, stock_info_id=stock_info_id, collect_time=get_today_format() )
        session.add( row_obj )
        session.commit()


# set_collection(1,2)

# 操作码27 删除收藏
def delete_collection(user_id, stock_info_id):
    res = session.query( Collection ).filter( Collection.user_id == user_id,
                                              Collection.stock_info_id == stock_info_id ).first()
    session.delete( res )
    session.commit()
# delete_collection(1,1)

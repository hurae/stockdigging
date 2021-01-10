from sqlalchemy.orm import sessionmaker, relationship

from storage.operation import models
from storage.operation.models import IndexInfo, StockInfo, IndexPoint, StockPrice, StockComment, IndexComment, \
    StockPopular, IndexPopular
from digging_utils import get_year_format, get_today_format


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
    print( res )
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
                          low=low )
    session.add( row_obj )
    session.commit()


# set_index_state('222', '2020-1-1', 1.1, 2.1, 1.0, 1.1)


# extract_stock_id:通过ts_code查询股票id
def extract_stock_id(ts_code):
    res = session.execute( session.query( StockInfo.id ).filter( StockInfo.ts_code == ts_code ) ).fetchall()[0][0]
    print( res )
    return res


# operation 9 插入股票行情:股价表
def set_stock_state(ts_code, trade_date, open, high, low, close):
    row_obj = StockPrice( stock_info_id=extract_stock_id( ts_code ),
                          trade_date=trade_date,
                          open=open,
                          high=high,
                          low=low,
                          close=close )
    session.add( row_obj )
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


# operation 11 写入指数评论:指数评论表、指数热度表
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

# 查看对应股票的一年内所有评论
def get_stock_history_comment(ts_code):
    res = session.execute( session.query( StockComment.content ).filter(
        StockInfo.ts_code == ts_code,
        StockComment.stock_info_id == StockInfo.id,
        get_year_format() < StockComment.comment_date,
        StockComment.comment_date < get_today_format() ) ).fetchall()
    print( "data:", res )
    return res


# get_stock_history_comment("gupiao4")

# 查看对应指数的一年内所有评论
def get_index_history_comment(ts_code):
    res = session.execute( session.query( IndexComment.content ).filter(
        IndexInfo.ts_code == ts_code,
        IndexComment.index_info_id == IndexInfo.id,
        get_year_format() < IndexComment.comment_date,
        IndexComment.comment_date > get_today_format() ) ).fetchall()
    print( "data:", res )
    return res


# get_index_today_comment("zhishu2")

# 查看对应股票的今天所有评论
def get_stock_today_comment(ts_code):
    res = session.execute( session.query( StockComment.content ).filter(
        StockInfo.ts_code == ts_code,
        StockComment.stock_info_id == StockInfo.id,
        StockComment.comment_date == get_today_format() ) ).fetchall()
    print( "data:", res )
    return res


# get_stock_today_comment("gupiao4")


# 查看对应指数的今天内所有评论
def get_index_today_comment(ts_code):
    res = session.execute( session.query( IndexComment.content ).filter(
        IndexInfo.ts_code == ts_code,
        IndexComment.index_info_id == IndexInfo.id,
        IndexComment.comment_date == get_today_format() ) ).fetchall()
    print( "data:", res )
    return res


# get_index_today_comment("zhishu2")


# operation 1 查看历史所有评论
# def get_all_comment():
#     # 股票所有评论
#     query = session.query( StockInfo.ts_code, StockComment.comment_date ).all()
#     result = map( lambda item: (item[0], item[1].strftime( "%Y-%m-%d" )), query )
#     for i in result:
#         # print(i[0])
#         res = session.execute( session.query( StockComment.content ).filter(
#             StockInfo.ts_code == i[0],
#             StockComment.stock_info_id == StockInfo.id,
#             get_year_format() < i[1],
#             i[1] < get_today_format() ) ).fetchall()
#     print( "data:", res )

    # ans = [ele for ele in (map( lambda item: (item[0], item[1].strftime( "%Y-%m-%d" )), query ))]
    # print(ans)
    # print( len( query ) )


# if __name__ == "__main__":
Session = sessionmaker( bind=models.engine )
session = Session()

set_stock_state("600187.SH", "20210105", 2.46, 2.46, 2.39, 2.41)

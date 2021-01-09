# coding: utf-8
# the model.py is used to dbORM and connect the database
from sqlalchemy import Column, Date, Float, String, create_engine, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMBLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine( "mysql+pymysql://root:Xijiao123@47.110.150.159:3306/stock?charset=utf8" )

Base = declarative_base()
metadata = Base.metadata


class IndexInfo( Base ):
    __tablename__ = 'index_info'

    id = Column( INTEGER( 11 ), primary_key=True )
    ts_code = Column( String( 20 ) )
    name = Column( String( 20 ) )
    fullname = Column( String( 10 ) )
    market = Column( String( 10 ) )
    publisher = Column( String( 20 ) )
    index_type = Column( String( 10 ) )
    category = Column( String( 10 ) )
    base_date = Column( Date )
    base_point = Column( String( 10 ) )
    list_date = Column( Date )
    weight_rule = Column( Float( 100, True ) )
    desc = Column( String( 255 ) )
    exp_date = Column( Date )
    index_points = relationship( "IndexPoint", back_populates="index_infos" )


class StockInfo( Base ):
    __tablename__ = 'stock_info'

    id = Column( INTEGER( 11 ), primary_key=True )
    ts_code = Column( String( 10 ), comment='tushare的id' )
    stock_name = Column( String( 10 ), comment='股票名' )
    stock_code = Column( String( 6 ), comment='股票代码' )
    list_data = Column( Date, comment='上市时间' )
    area = Column( String( 5 ), comment='区域' )
    industry = Column( String( 20 ), comment='行业' )
    stock_prices = relationship( "StockPrice", back_populates="stock_infos" )


class Test( Base ):
    __tablename__ = 'test'

    id = Column( INTEGER( 11 ), primary_key=True )
    name = Column( String( 255 ) )
    password = Column( String( 255 ) )


class User( Base ):
    __tablename__ = 'user'

    id = Column( INTEGER( 11 ), primary_key=True )
    name = Column( String( 255 ) )
    signature = Column( String( 255 ) )
    favcion = Column( MEDIUMBLOB, comment='头像' )
    state = Column( INTEGER( 11 ) )
    password = Column( String( 255 ) )
    salt = Column( String( 8 ) )
    phone = Column( String( 11 ) )
    last_login = Column( Date )


class Collection( Base ):
    __tablename__ = 'collection'

    id = Column( INTEGER( 11 ), primary_key=True )
    user_id = Column( INTEGER( 11 ), ForeignKey( 'user.id' ), unique=True )
    stock_info_id = Column( INTEGER( 11 ) )
    collect_time = Column( Date )


class IndexComment( Base ):
    __tablename__ = 'index_comment'

    id = Column( INTEGER( 11 ), primary_key=True )
    index_info_id = Column( INTEGER( 11 ), ForeignKey( 'index_info.id' ) )
    content = Column( String( 255 ) )
    comment_date = Column( Date )
    # index_infos = relationship( "IndexInfo", back_populates="index_comments" )


class IndexForecast( Base ):
    __tablename__ = 'index_forecast'

    id = Column( INTEGER( 11 ), primary_key=True )
    index_info_id = Column( INTEGER( 11 ), ForeignKey( 'index_info.id' ) )
    trade_date = Column( Date )
    forecast = Column( Float )


class IndexPoint( Base ):
    __tablename__ = 'index_point'

    id = Column( INTEGER( 11 ), primary_key=True )
    index_info_id = Column( INTEGER, ForeignKey( 'index_info.id' ) )
    trade_date = Column( Date )
    close = Column( Float( 255 ) )
    open = Column( Float( 255 ) )
    high = Column( Float( 255 ) )
    low = Column( Float( 255 ) )
    # 设置外键关系,格式：从表变量名=relationship（“对应的主表类名”，back_populates="对应主表的设置的变量名"）
    # 主表的对应关系反之
    index_infos = relationship( "IndexInfo", back_populates="index_points" )


class IndexPopular( Base ):
    __tablename__ = 'index_popular'

    id = Column( INTEGER( 11 ), primary_key=True )
    index_info_id = Column( INTEGER( 11 ), ForeignKey( 'stock_info.id' ) )
    comment_date = Column( Date )
    num = Column( INTEGER( 11 ) )
    public_index = Column( Float( 11 ) )


class StockComment( Base ):
    __tablename__ = 'stock_comment'

    id = Column( INTEGER( 11 ), primary_key=True )
    stock_info_id = Column( INTEGER( 11 ), ForeignKey( 'stock_info.id' ) )
    content = Column( String( 255 ) )
    comment_date = Column( Date )


class StockForecast( Base ):
    __tablename__ = 'stock_forecast'

    id = Column( INTEGER( 11 ), primary_key=True )
    stock_info_id = Column( INTEGER( 11 ), ForeignKey( 'stock_info.id' ) )
    trade_date = Column( Date )
    forecast = Column( Float )


class StockPopular( Base ):
    __tablename__ = 'stock_popular'

    id = Column( INTEGER( 11 ), primary_key=True )
    stock_info_id = Column( INTEGER( 11 ), ForeignKey( 'stock_info.id' ) )
    comment_date = Column( Date )
    num = Column( INTEGER( 11 ) )
    public_index = Column( Float( 11 ) )


class StockPrice( Base ):
    __tablename__ = 'stock_price'

    id = Column( INTEGER( 11 ), primary_key=True )
    stock_info_id = Column( INTEGER, ForeignKey('stock_info.id'))
    trade_date = Column( Date )
    open = Column( Float( 255 ) )
    high = Column( Float( 255 ) )
    low = Column( Float( 255 ) )
    close = Column( Float( 255 ) )
    stock_infos = relationship( "StockInfo", back_populates="stock_prices" )


def init_db():
    Base.metadata.create_all( engine )


def drop_db():
    Base.metadata.drop_all( engine )


if __name__ == '__main__':
    init_db()
# 外键报错原因：没有正向和反向的relationship
# 外键设置应该是表的id，而不是类的id(本质问题)

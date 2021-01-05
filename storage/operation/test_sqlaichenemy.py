# 1,导入官宣模型
from pip._internal.resolution.resolvelib.factory import Factory
from sqlalchemy.ext.declarative import declarative_base
# 导入数据类型
from sqlalchemy import Column, Integer, String, Date
# 导入连接数据库的包
from sqlalchemy import create_engine
import pymysql

# 2,实例化官宣模型
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# 3,创建object
# 当前这个object继承了Base也就是说代表object继承了ORM模型
# 4,创建数据库引擎
engine = create_engine("mysql+pymysql://root:Xijiao123@47.110.150.159:3306/stock?charset=utf8")

if __name__ == '__main__':
# 5,Base自动检索所有继承Base的ORM对象,并且创建所有的数据表
Base.metadata.create_all(engine)

    Session = sessionmaker(engine)
    session = Session()

new_stock=set_stock_info(stock_name='123')
session.add)(new_stock)
# new_person = Person(name='new person')
# session.add(new_person)
# session.commit()
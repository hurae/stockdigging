import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, UniqueConstraint, Index
Base = declarative_base()
class Stock_Info(Base):

class Users(Base):
    __tablename__ = 'users'  # 数据库表名称
    id = Column(Integer, primary_key=True)  # id 主键
    name = Column(String(32), index=True, nullable=False)  # name列，索引，不可为空
    # email = Column(String(32), unique=True)
    #datetime.datetime.now不能加括号，加了括号，以后永远是当前时间
    # ctime = Column(DateTime, default=datetime.datetime.now)
    # extra = Column(Text, nullable=True)

    __table_args__ = (
        # UniqueConstraint('id', 'name', name='uix_id_name'), #联合唯一
        # Index('ix_id_name', 'name', 'email'), #索引
    )

def init_db():
    """
    根据类创建数据库表
    :return:
    """
    engine = create_engine(
        "mysql+pymysql://root:123456@127.0.0.1:3306/aaa?charset=utf8",
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )

    Base.metadata.create_all(engine)

def drop_db():
    """
    根据类删除数据库表
    :return:
    """
    engine = create_engine(
        "mysql+pymysql://root:123456@127.0.0.1:3306/aaa?charset=utf8",
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )

    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    # drop_db()
    init_db()
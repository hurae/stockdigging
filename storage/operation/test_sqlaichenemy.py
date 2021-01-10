# 实例化官宣模型
from sqlalchemy.orm import sessionmaker
import models

Session = sessionmaker( bind=models.engine )
session = Session()

# 增

session.add_all( [
    models.StockInfo( ts_code='123',
                      stock_name='测试1',
                      stock_code='0069',
                      list_data='2020-1-1',
                      area='上海',
                      industry='123' ),
    models.StockInfo( ts_code='456',
                      stock_name='测试2',
                      stock_code='0079',
                      list_data='2020-2-1',
                      area='深圳',
                      industry='123' )
] )

session.commit()

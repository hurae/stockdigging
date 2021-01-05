import pymysql

#操作码1.查看历史所有评论
# def get_all_comment()：

# 操作码7.写入股票基本信息(插入数据)
def set_stock_info(conn,ts_code,stock_name,stock_code,list_data,area,industry):
    # 获取游标对象
    cursor = conn.cursor()
    t = (ts_code,stock_name,stock_code,list_data,area,industry)
    sql = "insert into stock_info(ts_code,stock_name,stock_code,list_data,area,industry) values(%s,%s,%s,%s,%s,%s)"
    insert = cursor.executemany(sql, [(t)])
    print('批量插入返回受影响的行数：', insert)
    conn.commit()
    cursor.close()

# 1.连接数据库
conn = pymysql.connect(
    host='47.110.150.159',
    port=3306,
    user='root',
    password='Xijiao123',
    db='stock',
    charset='utf8',
)
# 2.具体操作
print('start inserting data...')
set_stock_info(conn,"gupiao","12345","12345","1998-11-19","12345","12345")
# 5. 关闭连接
conn.close()


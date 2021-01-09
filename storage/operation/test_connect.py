import pymysql

# 1.连接数据库
conn = pymysql.connect(
    host='47.110.150.159',
    port=3306,
    user='root',
    password='Xijiao123',
    db='stock',
    charset='utf8',
)

# 获取游标对象
cursor = conn.cursor()

# 插入数据
sql = "insert into test (name,password) values ('pan','123')"
cursor.execute( sql )

# 另一种插入数据的方式，通过字符串传入值
sql = "insert into test (name,password) values(%s,%s)"
insert = cursor.executemany( sql, [('wen', '20'), ('tom', '10')] )
print( '批量插入返回受影响的行数：', insert )

# 查询数据
sql = "select * from test"
cursor.execute( sql )
while 1:
    res = cursor.fetchone()
    if res is None:
        # 表示已经取完结果集
        break
    print( res )

# 更新一条数据
update = cursor.execute( "update test set name='pan' where name ='wen'" )
print( '修改后受影响的行数为：', update )
# 更新2条数据
sql = "update test set password=%s where name=%s"
update = cursor.executemany( sql, [(15, 'pan'), (18, 'test')] )

# 查询一条数据
cursor.execute( "select * from test where name in ('pan','test')" )
print( cursor.fetchall() )

# 删除2条数据
sql = "delete from test where id=%s"
cursor.executemany( sql, [7, 8, 9] )
# 删除数据
# cursor.execute("delete from test where id>4")
# 提交事务
conn.commit()

# 4. 关闭游标
cursor.close()
# 5. 关闭连接
conn.close()

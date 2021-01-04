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
# 获取游标
cursor = conn.cursor()

# 插入数据
sql= "insert into test (id,name,password) values (1,'frank','manager')"
cursor.execute(sql)
conn.commit()
print('成功insert')

# 4. 关闭游标
cursor.close()
# 5. 关闭连接
conn.close()


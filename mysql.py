import pymysql
def select_enterprise():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "mySQL#h@d00p", "industry_graph", charset='utf8' )

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT uni_code,com_name FROM enterprise \
           WHERE import_flag = '%d'" % (0)
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
       for row in results:
          print(row)
          # fname = row[0]
          # lname = row[1]
          # age = row[2]
          # sex = row[3]
          # income = row[4]
          # 打印结果
          # print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
          #        (fname, lname, age, sex, income )
    except:
       print("Error: unable to fecth data")

    # 关闭数据库连接
    db.close()
    return results

def updata_enterprise_import_flag(enterprises):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "mySQL#h@d00p", "industry_graph", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    for enterprise in enterprises:
        # SQL 查询语句
        sql = "UPDATE enterprise SET import_flag = 1 WHERE uni_code = '%s'" % (enterprise["uni_code"])
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()

    # 关闭数据库连接
    db.close()
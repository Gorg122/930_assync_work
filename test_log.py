import pymysql.cursors
import time

def connect():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='root',
                          database='labstandstatus',
                          cursorclass=pymysql.cursors.DictCursor)
    return con


def log_upload(stat_work_time, sts_3_time, sts_4_time, sts_5_time, fin_time, type_pr, comm_numm, file_size, email):
    con = connect()
    with con:
        cur = con.cursor()
        try:
            sql = ("""INSERT INTO log_table
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")
            cur.execute(sql, (stat_work_time, sts_3_time, sts_4_time, sts_5_time, fin_time, type_pr, comm_numm, file_size, email))
            con.commit()
            print("Лог записан")

            sql = ("""SELECT LAST_INSERT_ID()""")
            cur.execute(sql)
            last_id = cur.fetchone()
            print('Данная работа была записана в лог с id '+ last_id[0])
        except:
            print("Лог не записан")

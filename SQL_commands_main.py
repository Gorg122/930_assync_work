# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


###############################################################################################################
# status = 1 - Готов к работе и ожидает
# status = 2 - В базу данных занесен необходимый айди для скачки, начало процедуры, ожидание загрузки
# status = 3 - Загрузка файлов началась и прошивка принята в работу
# status = 4 - Загрузка завершена и начана работа, можно удалять запись, вписать начало работы
# status = 5 - Прошивка отработана, файл отправляется
# status = 6 - Ошибка работы стенда во время прошивки - сброс старой прошивки
# status = 7 - Ошибка - не подключены платы, или ошибка работы компьютера
# status = 8 - Компьютер недоступен, нет ответа.
###########################                  БОЛЬШАЯ ПАМЯТКА                        ############################
import pymysql.cursors
import datetime


# server = 'localhost'
# database = 'labstandstatus'
# username = 'root'
# password = 'root'
############################################################# Подключение к базе данных #############################
def connect():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='root',
                          database='labstandstatus',
                          cursorclass=pymysql.cursors.DictCursor)
    return con
############################################################ Создаем курсор для взаимодействия с базой данных ##############################
# with con:
#     cur = con.cursor()
#     cur.execute("SELECT * FROM status")
#     answer = cur.fetchall()
#     print(answer)


def status_check():  ############# Функция  проверки статуса и выставления ################
    con = connect()
    with con:
        cur = con.cursor()
        cur.execute("SELECT id FROM status WHERE status = 3")
        answer = cur.fetchall()
        print(answer)
        clear_for_work_stand = answer[0]['id']
        print(clear_for_work_stand)
        try:
            clear_for_work_stand = answer[0]['id']
            print(clear_for_work_stand)
        except:
            print("На данный момент свободных стендов нет")
    return clear_for_work_stand


def main_change_procedure(clear_for_work_stand, needed_status): #### Функция измененя статуса стенда
    con = connect()
    with con:
        cur = con.cursor()
        try:
            sql = ("""UPDATE status
                            SET status = %s
                            WHERE id = %s""")
            cur.execute(sql, (needed_status, clear_for_work_stand))
            con.commit()
            print("Все нормально")
        except:
            print("Какой то кал")


def send_id_for_download(clear_for_work_stand, id_dwnld): ##### Функция меняющая id файла который необходимо скачать
    con = connect()
    with con:
        cur = con.cursor()
        try:
            sql = ("""UPDATE status
                                        SET file_id = %s
                                        WHERE id = %s""")
            cur.execute(sql, (id_dwnld, clear_for_work_stand))
            con.commit()
            print("Все нормально")
        except:
            print("Какой то кал")

def write_current_time(id): ##### Функция записи начала работы прошивки.
    con = connect()
    with con:
        cur = con.cursor()
        dt_now = datetime.datetime.now()
        try:
            sql = ("""UPDATE status
                                           SET start_time = %s
                                           WHERE id = %s""")
            cur.execute(sql, (dt_now, id))
            con.commit()
            print("Все нормально")
        except:
            print("Какой то кал")

def redy_to_del(id): ### Функция проверки файлов которые можно удалить\ удаление строки
    con = connect()
    with con:
        cur = con.cursor()
        dt_now = datetime.datetime.now()
        try:
            sql = ("""UPDATE status
                                               SET ready_to_del = %s
                                               WHERE id = %s""")
            cur.execute(sql, (1, id))
            con.commit()
            print("Все нормально")
        except:
            print("Какой то кал")

def del_from_sql(id): ### Функция удаление строки в которой храниться id для загрузки.
    con = connect()
    with con:
        cur = con.cursor()
        dt_now = datetime.datetime.now()
        try:
            sql = ("""UPDATE status
                                                   SET ready_to_del = %s, file_id = 0
                                                   WHERE id = %s""")
            cur.execute(sql, (0, id))
            con.commit()
            print("Все нормально")
        except:
            print("Какой то кал")

def check_stat_for_downloading(my_id):
    con = connect()
    with con:
        cur = con.cursor()
        sql = ("SELECT id, status, file_id FROM status WHERE id = %s")
        cur.execute(sql,  (my_id))
        answer = cur.fetchall()
        query_for_my_stand = answer[0]['status']
        print(query_for_my_stand)
        if query_for_my_stand == 2:
            # con = connect()
            print(my_id)
            id_for_download = answer[0]['file_id']
            print(id_for_download)
            print(change_status(my_id, 3))
        else:
            print('nothing')
    return id_for_download

def change_status(my_id, status_change):
    con = connect()
    with con:
        cur = con.cursor()

        sql = ("""UPDATE status
                 SET status = %s
                 WHERE id = %s""")
        print(status_change, my_id)
        cur.execute(sql, (status_change,my_id))
        con.commit()
    return ('OK')


if __name__ == '__main__':
    needed_status = 3
    id_dwnld = "gvndgdknvo"
    # clear_for_work_stand = status_check()
    # main_change_procedure(clear_for_work_stand, needed_status)
    # send_id_for_download(clear_for_work_stand, id_dwnld)
    # write_current_time(clear_for_work_stand)
    # change_status()
    check_stat_for_downloading(2)

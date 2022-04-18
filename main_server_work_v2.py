from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pymysql.cursors
import time
# import zipfile
# from New_all_2 import Launch
# from emailsend import send_email
# import smtplib
# import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
# from email import encoders                                  # Импортируем энкодер
# from email.mime.base import MIMEBase                        # Общий тип
# from email.mime.text import MIMEText                        # Текст/HTML
# from email.mime.image import MIMEImage                      # Изображения
# from email.mime.audio import MIMEAudio                      # Аудио
# from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект
import datetime
# import shutil
# import io
# from googleapiclient.http import MediaIoBaseDownload

email_name = "Not_email"

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'client_secret_2.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def main():
    #################################### Должно быть в начале 1 раз #############
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    service_sheets = discovery.build('sheets', 'v4', http=http)
    return service_sheets
    #################################### Должно быть в начале 1 раз #############

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart2.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def connect():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='root',
                          database='labstandstatus',
                          cursorclass=pymysql.cursors.DictCursor)
    return con

def status_check():  ############# Функция  проверки статуса и выставления ################
    con = connect()
    with con:
        cur = con.cursor()
        cur.execute("SELECT id FROM status WHERE status = 1")
        answer = cur.fetchall()
        try:
            clear_for_work_stand = answer[0]['id']
            print(clear_for_work_stand)
            return clear_for_work_stand
        except:
            print("На данный момент свободных стендов нет")
            return 0

def send_id_for_download(id_dwnld, email_name_sql, clear_for_work_stand ): ##### Функция меняющая id файла который необходимо скачать
    con = connect()
    with con:
        cur = con.cursor()
        # try:
        sql = ("""UPDATE status
                                        SET file_id = %s, emai_name = %s
                                        WHERE id = %s""")
        cur.execute(sql, (id_dwnld, email_name_sql,clear_for_work_stand))
        con.commit()
        change_status(clear_for_work_stand, 2)
        print("Все нормально")
        # except:
        # print("Какой то кал")

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


def exel_work(service_sheets):
    ranges = ["A2:C2"] #в этом месте надо выбрать ечейку которые будем исспользовать.
    spreadsheetId2 = "1hNTK6F98X5-lB1TIialANY9diKIXrQXRUQKMTVrKzB4"
    results = service_sheets.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId2,
                                     ranges = ranges,
                                     valueRenderOption = 'UNFORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    try:
        sheet_values = results['valueRanges'][0]['values'][0][2]
        value_id = sheet_values.split('=')[1]
        email_name = results['valueRanges'][0]['values'][0][1]
        print(value_id)
        return (value_id, email_name)
    except:
        print("Значений нет")
        return (0, 0)

def exel_del(service_sheets):
    ranges = ["A2:C2"]  # в этом месте надо выбрать ечейку которые будем исспользовать.
    spreadsheetId2 = "1hNTK6F98X5-lB1TIialANY9diKIXrQXRUQKMTVrKzB4"
    results = service_sheets.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId2,
                                                              ranges=ranges,
                                                              valueRenderOption='UNFORMATTED_VALUE',
                                                              dateTimeRenderOption='FORMATTED_STRING').execute()

    try:
        results_del = service_sheets.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId2, body={
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": 1843988947,
                            "dimension": "ROWS",
                            "startIndex": 1,
                            "endIndex": 2
                        }
                    }
                }
            ]
        })
        results_del.execute()
    except:
        print("Значений нет")
        return (0, 0)


def infinet_check(service_sheets, file_id, email):
    pc_id = status_check()
    print(pc_id)
    if pc_id != 0:
        send_id_for_download(file_id, email, pc_id)
        print("запись успешно записана")
        exel_del(service_sheets)
        return 1
    time.sleep(20)

def sub_main(service_sheets):
    id, email = exel_work(service_sheets)
    if (id != 0) and (email != 0):
        some_flag = 0
        while some_flag == 0:
            some_flag = infinet_check(service_sheets, id, email)
            print("Нет свободных компов") ##### Здесь должен быть цикл на проверку новых компов
    else:
        print("Нет записей")
        time.sleep(20)
    sub_main(service_sheets)


if __name__ == '__main__':
    sheets = main()
    sub_main(sheets)

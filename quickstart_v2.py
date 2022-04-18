from __future__ import print_function

import shutil

import httplib2
import os
import io
from googleapiclient.http import MediaIoBaseDownload
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import zipfile
from New_all_2 import Launch
from emailsend import send_email
import pymysql.cursors
import datetime
import time
import smtplib
import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект

email_name = "Not_email"
GLOBAL_PC_ID = 1

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'client_secret_2.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

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

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service
    # path_firmware = file_downloader(service, id, email)
    # file_delliter(id, service)
    # return service ,path_firmware

    addr_to = "sasha.lorens@yandex.ru"  # Получатель
    files = [
        "C:/Users/sasha/PycharmProjects/pythonProject1/sah.lorens@gmail.com/filename.zip"]  # Список файлов, если вложений нет, то files=[]                                      # Если нужно отправить все файлы из заданной папки, нужно указать её
    # send_email(addr_to, "Тема сообщения", "Текст сообщения", files)

def file_delliter(file_id, service):
    try:
        service.files().delete(fileId=file_id).execute()
    except:
        print('Ошибка: файла не существует')

def file_downloader(service, value_id, email_name):
    file_id = value_id
    email_short_name = email_name.split('@',2)[0]
    request = service.files().get_media(fileId=file_id)
    if not os.path.isdir('student_zip/'+email_short_name):    #Создание дериктории для хранения архива с файлами для прошивки
        os.makedirs('student_zip/'+email_short_name)
    fh = io.FileIO('student_zip/'+email_short_name+'/filename.zip', 'wb') #Загрузка
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    path_firmware = 'student_zip/'+email_short_name+''
    zip_file = zipfile.ZipFile('student_zip/'+email_short_name+'/filename.zip') #Разархивирование файла
    zip_file.extractall('student_zip/'+email_short_name)
    return path_firmware

def connect():
    con = pymysql.connect(host='DESKTOP-CG9VKI4',
                          port=3306,
                          user='user_1',
                          password='user_1',
                          database='labstandstatus',
                          cursorclass=pymysql.cursors.DictCursor)
    return con

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

def check_stat_for_downloading(my_id):
    con = connect()
    with con:
        cur = con.cursor()
        sql = ("SELECT id, status, file_id, emai_name FROM status WHERE id = %s")
        cur.execute(sql,  (my_id))
        answer = cur.fetchall()
        query_for_my_stand = answer[0]['status']
        if query_for_my_stand == 2:
            id_for_download = answer[0]['file_id']
            email_for_download = answer[0]['emai_name']
            print(id_for_download)
            print(change_status(my_id, 3))
            return id_for_download, email_for_download
        else:
            return 0, 0
            print('nothing')

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
            print("Не работает")



def sub_main(service):
    file_id, email = check_stat_for_downloading(GLOBAL_PC_ID)
    if (file_id != 0) and (email != 0):
        path_firmware = file_downloader(service, file_id, email)
        file_delliter(file_id, service)
        change_status(GLOBAL_PC_ID, 4)
        write_current_time(GLOBAL_PC_ID)

        email_name_cur = str(email.split('@')[0])
        print(email_name)
        file_p = "C:/PROJECT_930/Prototype_new_3/Archived/" + email_name_cur
        if Launch(path_firmware) == "OK":
            # new_users_dir = "C:\PROJECT_930\Prototype_new_2\Archived"
            print(send_email(addr_to=email,  # "sasha.lorens@yandex.ru",
                             msg_subj="Ваша прошивка",
                             msg_text="Ваши файлы",
                             files=os.listdir(file_p)))
            change_status(GLOBAL_PC_ID, 5)
            new_path = "C:/PROJECT_930/Prototype_new_3/"
            main_dir = path_firmware.split('/')[0]
            for dirs in os.listdir(new_path + main_dir):
                # os.rmdir(new_path + main_dir + "/" + dirs)
                shutil.rmtree(new_path + main_dir + "/" + dirs)


        else:
            print("SDFKMSJKFZNKLJFSRHFSRZBLHJFSBRGFLBHGRHLG RSG SRHLJG RLHGJD BGHLJDLJHG")
        change_status(GLOBAL_PC_ID, 1)
    time.sleep(20)
    sub_main(service)


if __name__ == '__main__':
    service = main()
    sub_main(service)

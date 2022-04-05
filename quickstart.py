from __future__ import print_function
import httplib2
import os
import io
from googleapiclient.http import MediaIoBaseDownload
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import zipfile
import smtplib
import mimetypes                                            # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders                                  # Импортируем энкодер
from email.mime.base import MIMEBase                        # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.image import MIMEImage                      # Изображения
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект


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
    service_sheets = discovery.build('sheets', 'v4', http=http)
    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            if '{0}'.format(item['name']) == 'schoolMIPS-00_simple - alex lorens.zip':
                print('{0} ({1})'.format(item['name'], item['id']))



    id, email = exel_work(service_sheets)
    file_downloader(service, id, email)

    addr_to = "sasha.lorens@yandex.ru"  # Получатель
    files = [
        "C:/Users/sasha/PycharmProjects/pythonProject1/sah.lorens@gmail.com/filename.zip"]  # Список файлов, если вложений нет, то files=[]                                      # Если нужно отправить все файлы из заданной папки, нужно указать её
    send_email(addr_to, "Тема сообщения", "Текст сообщения", files)

def extended_exel_work(service_sheets):
    ranges = []














def exel_work(service_sheets):
    ranges = ["A9:C9"] #в этом месте надо выбрать ечейку которые будем исспользовать.
    spreadsheetId2 = '1hNTK6F98X5-lB1TIialANY9diKIXrQXRUQKMTVrKzB4'
    results = service_sheets.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId2,
                                     ranges = ranges,
                                     valueRenderOption = 'UNFORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()

    sheet_values = results['valueRanges'][0]['values'][0][2]
    value_id = sheet_values.split('=')[1]

    email_name = results['valueRanges'][0]['values'][0][1]

    print(sheet_values)
    print(value_id)
    return (value_id, email_name)

def file_downloader(service, value_id, email_name):
    file_id = value_id
    request = service.files().get_media(fileId=file_id)
    if not os.path.isdir(email_name):    #Создание дериктории для хранения архива с файлами для прошивки
        os.mkdir(email_name)
    fh = io.FileIO(''+email_name+'/filename.zip', 'wb') #Загрузка
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    zip_file = zipfile.ZipFile(''+email_name+'/filename.zip') #Разархивирование файла
    zip_file.extractall(email_name)



if __name__ == '__main__':
    main()
import requests
import datetime


URL = 'https://cloud-api.yandex.net/v1/disk/resources'
TOKEN = 'AQAAAAAIQKhOAADLW7IIpZ6ywEKymmaczK7ncl0'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

def create_folder(path):
    """Создание папки. \n path: Путь к создаваемой папке."""
    print(requests.put(f'{URL}?path={path}', headers=headers))

def upload_file(loadfile, savefile, replace=True):
    """Загрузка файла.
    savefile: Путь к файлу на Диске
    loadfile: Путь к загружаемому файлу
    replace: true or false Замена файла на Диске"""
    res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file':f})
        except KeyError:
            print(res)

def disk_file_status(savefile):
    requests.put(f'{URL}/publish?path={savefile}', headers=headers).json()
    res = requests.get(f'{URL}?path={savefile}&fields=file', headers=headers).json()
    print(res)

# def check_del():
#     now = datetime.datetime.now()
#     res_json = requests.get(f'{URL}/resources?path=project_soc', headers=headers).json()
#     for element in res_json['items']:
#         if element["modified"] <= (now - 7):
#             print('some')
# create_folder('projects_soc/saha.lorens@yandex.ru')
upload_file(r'C:\Users\sasha\PycharmProjects\pythonProject1\client_secret_2.json', 'projects_soc/saha.lorens@yandex.ru/file.zip')
disk_file_status('projects_soc/saha.lorens@yandex.ru/file.zip')

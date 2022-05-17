import zipfile
import resource
import contextlib

def file_zip_correct():
    try:
        archive = zipfile.ZipFile('file.zip', 'r')
        archive.testzip()
        archive_list = archive.namelist()
        for itm in archive_list:
            if (itm.split('.')[1] == 'bat') or (itm.split('.')[1] == 'inf') or (itm.split('.')[1] == 'mp4'):
                raise Exception()
        print('Все файлы соответсвуют безопастности')
    except zipfile.BadZipFile:
        print('Неправильный зип файл')
    except NameError:
        print('Нет такого файла')
    except Exception:
        print('Опасный файл')


@contextlib.contextmanager
def limit(limit, type=resource.RLIMIT_AS):
    soft_limit, hard_limit = resource.getrlimit(type)
    resource.setrlimit(type, (limit, hard_limit)) # set soft limit
    try:
        yield
    finally:
        resource.setrlimit(type, (soft_limit, hard_limit)) # restore


with limit(1 << 30): # 1GB 
    # 1GB  Здесь должна быть по идее разархивация файла
    print('okey')

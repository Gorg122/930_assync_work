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




"""
## Скрипт в Google Scripts который позволяет предотвратить спам поьзователей.



function myFunction_2() {
  ss = SpreadsheetApp.getActiveSpreadsheet();
  Logger.log(ss.getRange('B2').getValue());
  email_data = ss.getRange('B2').getValue();
  ss.getRange('H1').setValue("=СЧЁТЕСЛИ(B2:B11;B2)");
  if(ss.getRange('H1').getValue() >= 5){
    ss.getRange('I1').setValue("=СТРОКА(ПРОСМОТР(B2;B2:B11))")
    num = ss.getRange('I1').getValue();
    ss.getRange('G1').setValue('=ПРАВСИМВ(A2; ПОИСК(" ";A2;1)-2)');
    ss.getRange('G2').setValue('=ПРАВСИМВ(A'+num+'; ПОИСК(" ";A'+num+';1)-2)');
    ss.getRange('G3').setValue('=ВРЕМЯ(ЛЕВСИМВ(G2; ПОИСК(":";G2;1)-1);ПСТР(G2; ПОИСК(":";G2) + 1; ПОИСК(":";G2;ПОИСК(":";G2)+1) - ПОИСК(":";G2) - 1);ПРАВСИМВ(G2; ПОИСК(":";G2;1)-2)) - ВРЕМЯ(ЛЕВСИМВ(G1; ПОИСК(":";G1;1)-1);ПСТР(G1; ПОИСК(":";G1) + 1; ПОИСК(":";G1;ПОИСК(":";G1)+1) - ПОИСК(":";G1) - 1);ПРАВСИМВ(G1; ПОИСК(":";G1;1)-2))');
    ss.getRange('G4').setValue('=ВРЕМЗНАЧ(G3)');
    time_num = ss.getRange('G4').getValue();
    if(time_num >= 0.02083333333){
      MailApp.sendEmail(ss.getRange('B2').getValue(), "Лабораторные стенды УЛ САПР", "Вы привысили колличество отправок прошивок за 30 минут, ваши прошивки были удалены из очереди по подозрению  в спаме, пожалуйста, не присылайте больше 5 прошивок за 30 минут. Спасибо!")
      for(var i = 3; i < 11; i++){
        if(ss.getRange('B'+i+'').getValue() == ss.getRange('B2').getValue()){
          ss.deleteRow(i);
        };
    };
  };
};
};


"""

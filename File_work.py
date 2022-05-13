import os
import shutil
import re
import time
import serial
import sys
import subprocess
import configparser
from win32com.shell import shell, shellcon

from SOF_TO_FPGA_4 import FPGA_flash
from Find_arduino_v2 import Find_Arduino


def Script_file_detect(User_path_to_file, root_path, errs_path):

    errors_file = open(errs_path, "w")

    script_file_path = "%"

    for root, dirs, files in os.walk(User_path_to_file):
        for file in files:
            if file.endswith(".txt") \
                    and not file.endswith(".sof") \
                    and not (file.endswith("JTAG_config.txt")) \
                    and not (file.endswith("Compil_result.txt")) \
                    and not (file.endswith("errors.txt")) \
                    and not (file.endswith("video_timing.txt")) \
                    and not (root == "db"):
                script_file_path = root + '/' + file
                #result_dir = os.path.join(root_path, root)
                script_file_name = file
                script_file_path = root_path + "/" + script_file_path
                print(script_file_path)

    if not os.path.exists(script_file_path):
        errors_file.write("Отсутствует файл сценария\n")
        errors_file.close()
        return("Neok", "Neok")
    else:
        #return("OK")
        errors_file.close()
        return(script_file_path, script_file_name)

def Arduino_Serial(script_file_path, errs_path, Arduino_port):
    input_file = open(script_file_path)


    print(len(re.findall(r"[\n']+?", open(script_file_path).read())))
    all_strings = len(re.findall(r"[\n']+?", open(script_file_path).read()))

    # выведем количество без пустых строк
    print(len(re.findall(r"[\n']+", open(script_file_path).read())))
    strings = len(re.findall(r"[\n']+", open(script_file_path).read()))

    video_file = open("video_timing.txt", "w")
    video_file.write(str(strings * 4))
    video_file.close()


    time.sleep(3)

    time.sleep(1)

    errors_file = open(errs_path, "w")

    lines = input_file.readlines()

    curent_pin = 0
    but = ["button"]
    sw = ["switch"]
    end = ["end"]
    #numbers = ["09"]
    delay = ["delay"]
    start = ["ardok"]
    switches = dict([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)])
    current_commands = 0

    arduino = serial.Serial(port=Arduino_port, baudrate=9600, timeout=.1)
    y = 0

    # waiting for device
    time.sleep(3)

    while y != 1:
        poslanie = "Hello"
        print("prohodka")
        # st = str(poslanie)
        arduino.write(bytes(poslanie, 'utf-8'))
        # data = arduino.readline()
        # data = arduino.read(arduino.inWaiting())
        data = str(arduino.readline().decode().strip('\r\n'))
        if str(data).count(start[0]):
            print("Poluchenorazhreshenie")
            # data = ""
            # poslanie = "1H"
            # arduino.write(bytes(poslanie, 'utf-8'))
            y += 1
    # data = arduino.read(arduino.inWaiting())
    print("Начало передачи сигналов")
    for i in range(strings):

        num = re.findall(r'\d+', str(lines[i]))
        false_pin = False

        for item in num:
            numbers = int(item)
        if (lines[i] != "\n"):
            print(numbers)
            if (int(numbers) > 8) or (int(numbers) < 1):
                i += 1
                false_pin = True
                errors_file.write("Количество активных пинов равно 9 (строка " + str(i) + ")\n")
                print("not write pin\n")
        if (lines[i] == "\n"):
            i += 1

        elif (false_pin == False):
            if (lines[i].count(but[0])):  # Кнопки
                curent_pin = num[0]
                comand_but1 = str(curent_pin) + "H"
                y = 0
                data = ""
                # while y != 1:
                arduino.write(bytes(comand_but1, 'utf-8'))
                time.sleep(0.5)
                data = str(arduino.readline().decode().strip('\r\n'))
                time.sleep(0.5)
                #print(data,'\n')
                #arduino.write(comand_but1)
                # arduino.write(bytes("", 'utf-8'))
                #time.sleep(1)
                # if data.count(h1[0]):
                # y += 1
                #print("EST")
                # arduino.write(bytes("Hoy", 'utf-8'))
                #print(comand_but1)
                #time.sleep(0.1)
                print(data,'\n')
                data = ""
                #time.sleep(0.1)
                comand_but2 = str(curent_pin) + "L"
                arduino.write(bytes(comand_but2, 'utf-8'))
                #arduino.write(comand_but2)
                #print(comand_but2)
                time.sleep(0.5)
                data = str(arduino.readline().decode().strip('\r\n'))
                time.sleep(0.5)
                print(data,'\n')
                current_commands += 1
                data = ""
                # print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100)\n digitalWrite(pin"+str(curent_pin)+", LOW);\n")
                #
                # output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n digitalWrite(pin"+str(curent_pin)+", LOW);\n")
            # elif (lines[i].count(sw[0])):
            #     if switches[i-1] == 0:
            #         print("digitalWrite(pin" + str(lines[i][-2]) + ", HIGH);\n sleep(500)\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
            #         output_file.write("digitalWrite(pin" + str(lines[i][-2]) + ", HIGH);\n sleep(500)\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
            #         switches[i-1] = 1

            elif (lines[i].count(sw[0])) and (switches[int(num[0])] == 0) and (false_pin != True):  # Свитч 0
                curent_pin = num[0]
                # print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                # output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                # switches[int(curent_pin)] = 1
                comand_sw1 = str(curent_pin) + "H"
                arduino.write(bytes(comand_sw1, 'utf-8'))
                #print(comand_sw1)
                time.sleep(0.5)
                data = str(arduino.readline().decode().strip('\r\n'))
                time.sleep(0.5)
                print(data,'\n')
                #time.sleep(0.1)
                switches[int(curent_pin)] = 1
                current_commands += 1
                data = ""

            elif (lines[i].count(sw[0])) and switches[int(num[0])] == 1 and false_pin != True:  # Свитч 1
                curent_pin = num[0]
                # print("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(100);\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                # output_file.write("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(100);\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                # switches[int(curent_pin)] = 0
                # switches.insert(int(lines[i][-2]),1)
                comand_sw2 = str(curent_pin) + "L"
                arduino.write(bytearray(comand_sw2, 'utf-8'))
                #print(comand_sw2)
                time.sleep(0.5)
                data = str(arduino.readline().decode().strip('\r\n'))
                time.sleep(0.5)
                print(data,'\n')
                #time.sleep(0.1)
                switches[int(curent_pin)] = 0
                current_commands += 1
                data = ""

            elif (lines[i].count(end[0])):
                print(switches)
                input_file.close()
                print(current_commands)
                break
    # output_file.close()
    input_file.close()
    errors_file.close()
    return("Ok")

def File_switch(User_path_to_file, root_path, sof_path, script_file_path, sof_file_name, script_file_name, vid_chek):
    # serial.Serial.close(arduino)

    users_dir = root_path + '/' + User_path_to_file
    if os.path.exists(root_path + '/' + User_path_to_file + "/filename.zip"):
        os.remove(root_path + '/' + User_path_to_file + "/filename.zip")

    chek = 1

    os.chdir(users_dir)
    print(users_dir, '\n')

    chek1 = ""
    chek2 = ""
    chek3 = ""
    log_name = "@"
    er_name = "$"
    config_file = "!"
    for files in os.listdir(users_dir):
        if files.find("errors.txt") != -1:
            check_er = open(files)
            chek1 = check_er.read(2)
            er_name = files
            check_er.close()
            # print(chek1, '\n')

        print('\n')

        if files.find("Proj_compil_result.txt") != -1:
            check_comp = open(files)
            chek2 = check_comp.read(2)
            log_name = files
            check_comp.close()
            # print(chek2, '\n')

        time.sleep(2)

        if files.find("JTAG_config.txt") != -1:
            check_conf = open(files)
            chek3 = check_conf.read(2)
            config_file = files
            check_conf.close()
            # print(chek2, '\n')

        # config_name = "JTAG_config.txt"
        # if config_name in files:
        #     config_file = files
        #     #print(chek2, '\n')

    errs_file_path = users_dir + "/" + er_name
    compil_path = users_dir + "/" + log_name
    config_path = users_dir + "/" + config_file

    if chek1 == "" and os.path.exists(errs_file_path):
        os.remove(errs_file_path)

    if chek2 == "" and os.path.exists(compil_path):
        os.remove(compil_path)

    if chek3 == "" and os.path.exists(config_path):
        os.remove(config_path)

    # Перемещение файлов в конечную папку пользователя
    if not os.path.exists(users_dir + "/" + "Report"):
        os.mkdir(users_dir + "/" + "Report")

    print("File with errors = " + er_name, '\n')
    if os.path.exists(errs_file_path):
        print("Перенос файла ошибок\n")
        shutil.copy(errs_file_path, users_dir + "/" + "Report" + "/" + er_name)
        time.sleep(1)
        os.remove(errs_file_path)

    print("File_compil = " + log_name, '\n')
    if os.path.exists(compil_path):
        print("Перенос файла отчета компиляции\n")
        shutil.copy(compil_path, users_dir + "/" + "Report" + "/" + log_name)
        time.sleep(1)
        os.remove(compil_path)

    print("Config file = " + config_file)
    if os.path.exists(config_path):
        print("Перенос файла отчета прошивки\n")
        shutil.copy(config_path, users_dir + "/" + "Report" + "/" + config_file)
        time.sleep(1)
        os.remove(config_path)

    print("TXT_script_file = ", script_file_path)
    print(script_file_path, '\n')
    if os.path.exists(script_file_path):
        print("Перенос файла сценария\n")
        shutil.copy(script_file_path, users_dir + "/" + "Report" + "/" + script_file_name)
        time.sleep(1)
        os.remove(script_file_path)

    print("SOF_FILE = ", sof_path)
    print(sof_path, '\n')
    if os.path.exists(sof_path):
        print("Перенос файла прошивки\n")
        shutil.copy(sof_path, users_dir + "/" + "Report" + "/" + sof_file_name)
        time.sleep(1)
        os.remove(sof_path)


    marker = ["done"]
    video_fragment = "subprocess.Popen object at"

    # Проверка на окончание записи видео
    video_end_chek = "<_io.BufferedReader name=4>"
    # video_found = True
    # while video_found:
    #     try:
    #         vid_chek = str(Video_chek.stdout)
    #         if vid_chek.find(video_end_chek) != -1:


    print(vid_chek, '\n')
    i = 0
    video_path = root_path + "/video/output.mp4"
    video_dir = root_path + "/video"
    copy_dst = root_path + "/" + User_path_to_file + "/Report/output.mp4"
    vid_exists = True

    # def mycopy(src, dst, follow_symlinks=True):
    #     print("video_copying")
    #     shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
    #     return "OK"

    def mycopy(src, dst, follow_symlinks=True):
        print("video_copying")
        shutil.copy(src=src, dst=dst, follow_symlinks=follow_symlinks)
        #
        return "OK"
    # def robocopy(source, destination, extension=''):
    #     os.system("robocopy {} {} {} /xx /njh".format(source, destination, extension))
    #     return "OK"
    while vid_exists:
        # if os.path.exists(prot_dir + "video_done.txt"):
        # vid_chek= open("video_done.txt")
        # video_chek = vid_chek.readline()
        # print("File_read,'\n")
        # if os.path.exists("output.mp4") and (video_chek.count(marker)):
        # print(Video_chek)

        if os.path.exists(video_path) and os.path.exists(root_path + "/video_done.txt") \
                and vid_chek.find(video_end_chek) != -1:  # Video_chek.stdout != "b''":
            print("File_est", '\n')
            time.sleep(20)
            #shutil.copy(video_path, copy_dst, follow_symlinks=True)
            #os.popen('copy ' + video_path + " " + copy_dst)
            shutil.copytree(video_dir, (root_path + '/' + User_path_to_file + "/Report/output.mp4"),
                            copy_function=mycopy)
            time.sleep(20)
            #shutil.copytree(video_path, (root_path + '/' + User_path_to_file + "/Report/output.mp4"), copy_function=mycopy)
            #copy_chek = robocopy(source=root_path, destination=root_path + '/' + User_path_to_file + "/Report", extension='*.mp4')
            # shutil.copytree(video_dir, (root_path + '/' + User_path_to_file + "/Report/output.mp4"),
            #                 copy_function=mycopy, dirs_exist_ok=True)
            # a = mycopy(src=video_path, dst=root_path + '/' + User_path_to_file + "/Report/output.mp4")
            # if a == "OK":
            #     print("video_copied")
            #     #os.remove(video_path)
            # #print("Video_copied")
            # #if copy_chek == "OK":
            print("Видео удаляется")
            os.remove(video_path)
            time.sleep(20)
            vid_exists = False
        elif i == 200:
            i += 1
            print(i)
        else:
            break
        # else:
        #     i += 1
        #     vid_exists = False

    if os.path.exists(root_path + "/video_done.txt") \
            and os.path.isfile(root_path + "/video_done.txt"):
        print("Удаление файла video_done.txt\n")
        os.remove(root_path + "/video_done.txt")

    if os.path.exists(root_path + "/video_timing.txt") \
            and os.path.isfile(root_path + "/video_timing.txt"):
        print("Удаление файла video_timing.txt\n")
        os.remove(root_path + "/video_timing.txt")
    # shutil.make_archive("Your_archive", 'zip', User_path_to_file + "//Your_archive.zip")
    # archive = zipfile.ZipFile('result.zip', 'w')
    # for file in os.listdir(users_dir):
    # archive.write(file, compress_type=zipfile.ZIP_DEFLATED)
    new_users_dir = root_path + "/Archived"
    archive_dir = root_path + "/Archive"
    os.chdir(new_users_dir)

    result_directory = User_path_to_file.split('/', 2)[1]
    if os.path.exists(new_users_dir + "/" + result_directory):
        shutil.rmtree(new_users_dir + "/" + result_directory)
        os.mkdir(result_directory)
        os.chdir(os.path.join(new_users_dir, result_directory))
        # os.rmdir(new_users_dir + "/" + result_directory)
        print("Создание архива на отправку/n")
        shutil.make_archive("result", 'zip', users_dir)
        #     time.sleep(2)
        print("Архив на отправку создан/n")
    else:
        os.mkdir(result_directory)
        os.chdir(os.path.join(new_users_dir, result_directory))
        print("Создание архива на отправку")
        shutil.make_archive("result", 'zip', users_dir)
        #     time.sleep(2)
        print("Архив на отправку создан")
    if os.path.exists(archive_dir):
        users_directory = archive_dir + "/" + result_directory
        if os.path.exists(users_directory):
            shutil.rmtree(users_directory)
            os.mkdir(users_directory)
            os.chdir(users_directory)
            print("Создание архива в хранилище/n")
            shutil.make_archive("result", 'zip', users_dir)
            #     time.sleep(2)
            print("Архив в хранилище создан/n")
        else:
            os.mkdir(users_directory)
            os.chdir(users_directory)
            print("Создание архива в хранилище/n")
            shutil.make_archive("result", 'zip', users_dir)
            #     time.sleep(2)
            print("Архив в хранилище создан/n")
    else:
        os.chdir(root_path)
        os.mkdir(archive_dir)
        users_directory = archive_dir + "/" + result_directory
        if os.path.exists(users_directory):
            shutil.rmtree(users_directory)
            os.mkdir(users_directory)
            os.chdir(users_directory)
            print("Создание архива в хранилище/n")
            shutil.make_archive("result", 'zip', users_dir)
            #     time.sleep(2)
            print("Архив в хранилище создан/n")
        else:
            os.mkdir(users_directory)
            os.chdir(users_directory)
            print("Создание архива в хранилище/n")
            shutil.make_archive("result", 'zip', users_dir)
            #     time.sleep(2)
            print("Архив в хранилище создан/n")
    return("Ok")

def Launch(User_path_to_file):

    # Открываем файл настроек
    #os.chdir(os.getcwd())
    #os.chdir("C:/PROJECT_930/Prototype_with_mail_bot/")

    config = configparser.ConfigParser()
    config.read("Config.ini")
    # with open('Config.ini') as configfile:
    #     config.read(configfile)
    #
    #     #Actualised a directory with a script.
    #     # abspath = os.path.abspath(__file__)
    #     # dname = os.path.dirname(abspath)
    #     # os.chdir(dname)
    #
    #     # Задаем директорию проекта
    #     #root_path = config['Path']['root_path']
    #root_path ="C:/PROJECT_930/Prototype_new_3"
    root_path = config['Project']['Path']
    print(root_path)
    errs_f = "errors.txt"
    errs_name = root_path + "/" + User_path_to_file
    errs_path = errs_name + '/' + errs_f
    errors_file = open(errs_path, "w")

    #Поиск файла прошивки

    # zip_dir = User_path_to_file.split("/",1)[0]
    # main_dir = root_path + "/" + zip_dir
    # print("ZIP DIR PATH = " + zip_dir,'/n')
    # if os.path.exists(zip_dir):
    #     for dirs in os.listdir(zip_dir):
    #         shutil.rmtree(zip_dir + "/" + dirs)

    script_file_path, script_file_name = Script_file_detect(User_path_to_file=User_path_to_file,
                                                            root_path=root_path,
                                                            errs_path=errs_path)
    print(script_file_path)
    print(script_file_path)
    # scetch_name = "scetch"
    if os.path.exists(script_file_path):

        sof_path = "#"
        sof_file_name = "#"
        Arduino_port = Find_Arduino()
        print(Arduino_port, '\n')
        print(Arduino_port[0:3], '\n')
        if Arduino_port[0:3] != 'COM':
            errors_file.write("Проблема при передаче управляющих сигналов, свяжитесь с преподавателем\n")

        # print(FPGA_flash(User_path=User_path_to_file))
        if FPGA_flash(User_path=User_path_to_file) != 'OK':
            errors_file.write("Проблема с компиляцией проекта, или прошивкой платы, изучите файлы логов\n")



        for root, dirs, files in os.walk(User_path_to_file):
            for file in files:
                if file.endswith(".sof"):
                    sof_path = os.path.join(root, file)
                    print(sof_path)
                    sof_path = root_path + "/" + sof_path
                    sof_file_name = file
                    print(sof_path)

        vid_chek = "video_none"
        if os.path.exists(sof_path):
            Video_chek = subprocess.Popen([sys.executable, 'Video.py'], stdout=subprocess.PIPE)
            vid_chek = str(Video_chek.stdout)
            serial = Arduino_Serial(script_file_path=script_file_path,
                                    errs_path=errs_path,
                                    Arduino_port=Arduino_port)
            if serial == "OK":
                print("Передача данных окончена")
            # file_work = File_switch(User_path_to_file=User_path_to_file,
            #                         root_path=root_path, sof_path=sof_path,
            #                         scrip_file_path=script_file_path,
            #                         sof_file_name=sof_file_name,
            #                         script_file_name=script_file_name)

        else:
            errors_file.write("Отсутствует файл прошивки или проект на ПЛИС\n")
    else:
        errors_file.write("Отправте данные повторно, включая файл сценария\n")
    errors_file.close()

    file_work = File_switch(User_path_to_file=User_path_to_file, root_path=root_path,
                            sof_path=sof_path, script_file_path=script_file_path,
                            sof_file_name=sof_file_name,
                            script_file_name=script_file_name,
                            vid_chek=vid_chek)

    #users_dir = os.path.join(root_path,User_path_to_file)

    #    os.remove(files)
    #shutil.copy(r"C:\PROJECT_930\Prototype_new_2\result.zip", "" + User_path_to_file)
    #for files in os.listdir(users_dir):
        #if not files.endswith("output.mp4"):
        #    errors_file.write("Отсутствует файл видеозаписи работы платы, перезалейте свои файлы\n")







    #     # archive.close()
    # for files in User_path_to_file:

    # for files in os.listdir(User_path_to_
    #shutil.copy(users_dir + r"/result/result.zip", r"C:\PROJECT_930\Prototype_new_2\Archived")

    # def empty(confirm, show_progress, sound):
    #     flags = 0
    #     if not confirm:
    #         flags |= shellcon.SHERB_NOCONFIRMATION
    #     if not show_progress:
    #         flags |= shellcon.SHERB_NOPROGRESSUI
    #     if not sound:
    #         flags |= shellcon.SHERB_NOSOUND
    #     shell.SHEmptyRecycleBin(None, None, flags)
    # empty(confirm=False, show_progress=True, sound=False)
    # print("Корзина очищена")
    #config.close()

    return("OK")

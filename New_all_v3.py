#Добавлена обработка всех возможных ошибок в тексте текстового файла
#Добавлена проверка на наличие текстового файла
#Добавлена обработка пустых строк
#Добавлено создание папки с названием файла скетча
#Добавлена переменная общего пути


import os
import shutil
import re
import time
import serial
import sys
import subprocess
import zipfile
from SOF_TO_FPGA_4 import FPGA_flash
from Find_arduino_v2 import Find_Arduino


def Launch(User_path_to_file):

    #Actualised a directory with a script.
    # abspath = os.path.abspath(__file__)
    # dname = os.path.dirname(abspath)
    # os.chdir(dname)

    #Поиск файла прошивки






    # scetch_name = "scetch"
    errs_f = "errors.txt"
    pat = r"C:\PROJECT_930\Prototype_new_2"
    errs_name = os.path.join(pat,User_path_to_file)
    #errs_path = os.path.join(errs_name,errs_f)
    errs_path = errs_name + '/' + errs_f
    #sof_path = "scetch"
    errors_file = open(errs_path, "w")

    file_path = "C/10000"
    sof_path = "C/100000"

    for root, dirs, files in os.walk(User_path_to_file):
        for file in files:
            if file.endswith(".txt") and not(file.endswith("JTAG_config.txt")) \
                    and not(file.endswith("Compil_result.txt")) \
                    and not(file.endswith("errors.txt"))\
                    and not(file.endswith("video_timing.txt")):


                file_path = root + '/' + file
                result_dir = os.path.join(User_path_to_file,root)
                script_file_name = file
                print(result_dir)
                print(file_path)
    prot_dir1 = "C:/PROJECT_930/Prototype_new_2/"
    file_path = prot_dir1 + file_path



    if not os.path.exists(file_path):

        errors_file.write("Отсутствует файл сценария\n")

    Arduino_port = Find_Arduino()
    print(Arduino_port,'\n')
    print(Arduino_port[0:3],'\n')
    if Arduino_port[0:3] != 'COM':
        errors_file.write("Проблема при передаче управляющих сигналов, свяжитесь с преподавателем\n")



    #print(FPGA_flash(User_path=User_path_to_file))
    if FPGA_flash(User_path=User_path_to_file) != 'OK':

        errors_file.write("Проблема с компиляцией проекта, или прошивкой платы, изучите файлы логов\n")

    Video_chek = subprocess.Popen([sys.executable, 'Video.py'], stdout=subprocess.PIPE)


    for root, dirs, files in os.walk(User_path_to_file):
        for file in files:
            if file.endswith(".sof"):
                sof_path = os.path.join(root, file)
                print(sof_path)


    # Выведем все строки включая пустые
    print(len(re.findall(r"[\n']+?", open(file_path).read())))
    all_strings = len(re.findall(r"[\n']+?", open(file_path).read()))

    # выведем количество без пустых строк
    print(len(re.findall(r"[\n']+", open(file_path).read())))
    strings = len(re.findall(r"[\n']+", open(file_path).read()))

    video_file = open("video_timing.txt", "w")
    video_file.write(str(strings * 3))
    video_file.close()





    if os.path.exists(file_path) and os.path.exists(sof_path):
        print(sof_path)

        #subprocess.Popen([sys.executable, 'Video.py'])

        time.sleep(3)

        # Запускаем процесс прошивки платы ПЛИС в подпроцессе

        #software = subprocess.call("C:\\intelFPGA_lite\\17.0\\quartus\\bin64\\quartus_pgm.exe -c \"USB-Blaster [USB-0]\" -m JTAG -o p;C:/PROJECT_930/PROTOTYPE/golden.sof")
        #time.sleep(1)

        #FPGA_flashing = subprocess.Popen([sys.executable, 'SOF_TO_FPGA_4.py'], )

        #os.system("@echo off")
        #os.system("cd C:\\intelFPGA_lite\\17.1\\quartus\\bin64\ rem")# quartus_pgm.exe -m JTAG -o p; sof_path Jtag_info.txt)
        #os .system("quartus_pgm.exe -m JTAG -o p;{0}> Jtag_info.txt".format(str(sof_path)))
        #os.system("quartus_pgm.exe -m JTAG -o p; golden.sof > Jtag_info.txt")

        # В подпроцессе запускаем запись видео
        #subprocess.call("Video.py", shell = True)
        #exec(open("Video.py").read())
        #subprocess.call("Video.py", shell=True)
        #print(sys.executable)

        # Arduino_port = subprocess.Popen([sys.executable, 'Find_arduino_v2'],
        #                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                 text=True)


        time.sleep(1)



        input_file = open(file_path)
        errors_file = open(errs_path, "w")

        lines = input_file.readlines()



        curent_pin = 0
        but = ["button"]
        sw = ["switch"]
        end = ["end"]
        numbers = ["09"]
        delay = ["delay"]
        start = ["ardok"]
        switches = dict([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)])
        current_commands = 0


        arduino = serial.Serial(port=Arduino_port, baudrate=9600, timeout=.1)
        y = 0

        # waiting for device
        time.sleep(3)

        while y != 1:
            poslanie = "Hellohel\n"
            print("prohodka")
            # st = str(poslanie)
            arduino.write(bytearray(poslanie, 'utf-8'))
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
        for i in range(all_strings):

            # if (lines[i] == "\n"):
            #     i = i + 1
            #     print("Empty string")
            # print(lines[i][-2])
            num = re.findall(r'\d+', str(lines[i]))
            false_pin = False
            # #if (i != all_strings):
            #     #if (int(lines[i][-2]) > 8) or (int(lines[i][-2]) < 1):
            # print(num)
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
            #    print("Empty string")

            # if (i):
            #     i = i + 1
            #     errors_file.write("Количество активных пинов равно 9\n")
            #     print("Количество активных пинов равно 9\n")

            elif (false_pin == False):
                if (lines[i].count(but[0])):  # Кнопки
                    curent_pin = num[0]
                    comand_but1 = str(curent_pin) + "Hllllll\n"
                    y = 0
                    data = ""
                    # while y != 1:
                    # arduino.write(bytearray(comand_but1, 'utf-8'))
                    # arduino.write(bytes("", 'utf-8'))
                    time.sleep(1)
                    # if data.count(h1[0]):
                    # y += 1
                    print("EST")
                    # arduino.write(bytes("Hoy", 'utf-8'))
                    print(comand_but1)
                    time.sleep(0.1)
                    print(data)
                    data = ""
                    time.sleep(0.1)
                    comand_but2 = str(curent_pin) + "Ldddddd\n"
                    # arduino.write(bytearray(comand_but2, 'utf-8'))
                    print(comand_but2)
                    time.sleep(0.1)
                    print(data)
                    current_commands += 1
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
                    comand_sw1 = str(curent_pin) + "Hssssss\n"
                    # arduino.write(bytearray(comand_sw1, 'utf-8'))
                    print(comand_sw1)
                    time.sleep(1)
                    print(data)
                    time.sleep(0.1)
                    switches[int(curent_pin)] = 1
                    current_commands += 1

                elif (lines[i].count(sw[0])) and switches[int(num[0])] == 1 and false_pin != True:  # Свитч 1
                    curent_pin = num[0]
                    # print("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(100);\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                    # output_file.write("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(100);\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                    # switches[int(curent_pin)] = 0
                    # switches.insert(int(lines[i][-2]),1)
                    comand_sw2 = str(curent_pin) + "Lssssss\n"
                    # arduino.write(bytearray(comand_sw2, 'utf-8'))
                    print(comand_sw2)
                    time.sleep(1)
                    print(data)
                    time.sleep(0.1)
                    switches[int(curent_pin)] = 0
                    current_commands += 1

                elif (lines[i].count(end[0])):
                    print(switches)
                    input_file.close()
                    print(current_commands)
                    break
        # output_file.close()
    else:
        errors_file.write("Отсутствует файл сценария или файл прошивки\n")
        #errors_file.close()

    users_dir = "C:/PROJECT_930/Prototype_new_2/" + User_path_to_file
    #    os.remove(files)
    #shutil.copy(r"C:\PROJECT_930\Prototype_new_2\result.zip", "" + User_path_to_file)
    for files in os.listdir(users_dir):
        if files.endswith("output.mp4"):
            errors_file.write("Отсутствует файл видеозаписи работы платы, перезалейте свои файлы\n")
    errors_file.close()
    #serial.Serial.close(arduino)
    if os.path.exists(User_path_to_file + "//filename.zip"):
        os.remove(User_path_to_file + "//filename.zip")

    chek = 1

    os.chdir(users_dir)
    print(users_dir,'\n')
    print(users_dir,'\n')
    prot_dir = "C:/PROJECT_930/Prototype_new_2/"

    for files in os.listdir(users_dir):
        if files.endswith("errors.txt"):
            check = open(files)
            chek1 = check.read(2)
            er_name = files
            check.close()
            #print(chek1, '\n')

        print('\n')
        if files.endswith("Proj_compil_result.txt"):
            check = open(files)
            chek2 = check.read(2)
            log_name = files
            check.close()
            #print(chek2, '\n')

        if files.endswith("JTAG_config.txt"):
            config_file = files
            #print(chek2, '\n')

    if chek1 == "" and os.path.exists(users_dir + "/" + er_name):
        os.remove(users_dir + "/" + er_name)

    if chek2 == "" and os.path.exists(users_dir + "/" + log_name):
        os.remove(users_dir + "/" + log_name)

    # Перемещение файлов в конечную папку пользователя
    if not os.path.exists(users_dir + "/" + "Report"):
        os.mkdir(users_dir + "/" + "Report")

    if os.path.exists(users_dir + "/" + er_name):
        print("Перенос файла ошибок\n")
        shutil.copy(users_dir + "/" + er_name, users_dir + "/" + "Report" + "/" + er_name)
        time.sleep(1)
        os.remove(users_dir + "/" + er_name)

    if os. path.exists(users_dir + "/" + log_name):
        print("Перенос файла отчета компиляции\n")
        shutil.copy(users_dir + "/" + log_name, users_dir + "/" + "Report" + "/" + log_name)
        time.sleep(1)
        os.remove(users_dir + "/" + log_name)



    if os. path.exists(users_dir + "/" + config_file):
        print("Перенос файла отчета прошивки\n")
        shutil.copy(users_dir + "/" + config_file, users_dir + "/" + "Report" + "/" + config_file)
        time.sleep(1)
        os.remove(users_dir + "/" + config_file)





    # if os. path.exists(file_path):
    #     print("Перенос файла сценария\n")
    #     shutil.copy(file_path, users_dir + "/" + "Report" + "/" + script_file_name)
    #     time.sleep(1)
    #     os.remove(file_path)


    vid_exists = True
    marker = ["done"]
    video_fragment = "subprocess.Popen object at"
    while vid_exists:
        #if os.path.exists(prot_dir + "video_done.txt"):
            # vid_chek= open("video_done.txt")
            #video_chek = vid_chek.readline()
            #print("File_read,'\n")
        #if os.path.exists("output.mp4") and (video_chek.count(marker)):
        #print(Video_chek)
        if os.path.exists(prot_dir + "output.mp4") and os.path.exists(prot_dir + "video_done.txt")\
                and Video_chek.stdout != "b''":
            print("File_est",'\n')
            shutil.copy(prot_dir + "output.mp4",  prot_dir + '/' + User_path_to_file + "/Report/output.mp4")
            os.remove(prot_dir + "output.mp4")
            vid_exists = False

    if os.path.exists(prot_dir + "video_done.txt"):
        print("Удаление файла video_done.txt\n")
        os.remove(prot_dir + "video_done.txt")

    if os.path.exists(prot_dir + "video_timing.txt"):
        print("Удаление файла video_timing.txt\n")
        os.remove(prot_dir + "video_timing.txt")
    # shutil.make_archive("Your_archive", 'zip', User_path_to_file + "//Your_archive.zip")
    #archive = zipfile.ZipFile('result.zip', 'w')
    #for file in os.listdir(users_dir):
        # archive.write(file, compress_type=zipfile.ZIP_DEFLATED)
    new_users_dir = "C:/PROJECT_930/Prototype_new_2/Archived"
    os.chdir(new_users_dir)

    result_directory = User_path_to_file.split('/', 2)[1]
    if os.path.exists(new_users_dir + "/" + result_directory):
        shutil.rmtree(new_users_dir + "/" + result_directory)
        #os.rmdir(new_users_dir + "/" + result_directory)
    else:
        os.mkdir(result_directory)
        os.chdir(os.path.join(new_users_dir, result_directory))
    print("Создание архива")
    shutil.make_archive("result", 'zip', users_dir)
    #     time.sleep(5)
    print("архив создан")
    #     # archive.close()
    # for files in User_path_to_file:

    # for files in os.listdir(User_path_to_
    #shutil.copy(users_dir + r"/result/result.zip", r"C:\PROJECT_930\Prototype_new_2\Archived")



    return("OK")


#if __name__ == '__main__':
#Launch(User_path_to_file="C:\PROJECT_930\Prototype_new\student_zip\sasha.lorens@yandex.ru")
#Launch(User_path_to_file="C:\intelFPGA_lite\Otladka")
#Launch(User_path_to_file="C:\PROJECT_930\Prototype_new_2\student_zip\proverka@mail.ru")
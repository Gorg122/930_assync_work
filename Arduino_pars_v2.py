#Добавлена обработка всех возможных ошибок в тексте текстового файла
#Добавлена проверка на наличие текстового файла
#Добавлена обработка пустых строк
#Добавлено создание папки с названием файла скетча
#Добавлена переменная общего пути


import re
import os
import shutil


#output_file = open("scetch.ino", "w")
filePath = __file__
main_path = os.getcwd()
users_mail = "example"
file_name = "buttons.txt"
scetch_name = "scetch"
errs_f = "errors.txt"
output_dir = os.path.join(main_path,users_mail)
#erros_path = os.path.join(main_path, )
file_path = os.path.join(main_path, file_name)
errors_file = open(output_dir + "errors.txt", "w")

if os.path.exists(file_path):

    # выведем все строки включая пустые

    print(len(re.findall(r"[\n']+?", open(file_path).read())))
    all_strings = len(re.findall(r"[\n']+?", open(file_path).read()))

    # выведем количество без пустых строк
    print(len(re.findall(r"[\n']+", open(file_path).read())))
    strings = len(re.findall(r"[\n']+", open(file_path).read()))
    # if all_strings != strings:
    #     errors_file.write("Ваш файл сценария не должен содержать пустых строк\n")
    input_file = open(file_path)

    lines = input_file.readlines()
    scetch_dir = os.path.join(main_path, scetch_name)
    if os.path.exists(scetch_dir):
        shutil.rmtree(scetch_dir)
        #os.rmdir(scetch_dir)
    else:
        os.mkdir(scetch_dir)
    scetch_path = os.path.join(scetch_dir, scetch_name)

    output_file = open(scetch_path + ".ino", "w")
    output_file.write("""
    int pin1 = 2;\n
    int pin2 = 3;\n
    int pin3 = 4;\n
    int pin4 = 5;\n
    int pin5 = 8;\n
    int pin6 = 9;\n
    int pin7 = 10;\n
    int pin8 = 11;\n
    void setup()\n
    {\n
    pinMode(pin1, OUTPUT);\n
    pinMode(pin2, OUTPUT);\n
    pinMode(pin3, OUTPUT);\n
    pinMode(pin4, OUTPUT);\n
    pinMode(pin5, OUTPUT);\n
    pinMode(pin6, OUTPUT);\n
    pinMode(pin7, OUTPUT);\n
    pinMode(pin8, OUTPUT);\n
    digitalWrite(pin1, LOW);\n
    digitalWrite(pin2, LOW);\n
    digitalWrite(pin3, LOW);\n
    digitalWrite(pin4, LOW);\n
    digitalWrite(pin5, LOW);\n
    digitalWrite(pin6, LOW);\n
    digitalWrite(pin7, LOW);\n
    digitalWrite(pin8, LOW);\n
    }\n
    void loop()\n
    {\n
    """)
    but = ["button"]
    sw = ["switch"]
    end = ["end"]
    empty = [""]
    numbers = ["0","9"]
    switches = dict([(1, 0),(2, 0),(3, 0),(4, 0),(5, 0),(6, 0),(7, 0),(8, 0)])

    for i in range(all_strings):

        # if (lines[i] == "\n"):
        #     i = i + 1
        #     print("Empty string")
        #print(lines[i][-2])
        num = re.findall(r'\d+', str(lines[i]))
        false_pin = False
        # #if (i != all_strings):
        #     #if (int(lines[i][-2]) > 8) or (int(lines[i][-2]) < 1):
        # print(num)
        if (lines[i] != "\n"):
            print(num[0])
            if (int(num[0]) > 8) or (int(num[0]) < 1):
                i += 1
                false_pin = True
                errors_file.write("Количество активных пинов равно 9 (строка " + str(i) + ")\n")
                print("not write pin\n")
        if (lines[i] == "\n"):
             i += 1
             print("Empty string")
        # if (i):
        #     i = i + 1
        #     errors_file.write("Количество активных пинов равно 9\n")
        #     print("Количество активных пинов равно 9\n")
        elif (false_pin == False):
            if (lines[i].count(but[0])):
                curent_pin = num[0]
                print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100)\n digitalWrite(pin"+str(curent_pin)+", LOW);\n")

                output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n digitalWrite(pin"+str(curent_pin)+", LOW);\n")
            # elif (lines[i].count(sw[0])):
            #     if switches[i-1] == 0:
            #         print("digitalWrite(pin" + str(lines[i][-2]) + ", HIGH);\n sleep(500)\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
            #         output_file.write("digitalWrite(pin" + str(lines[i][-2]) + ", HIGH);\n sleep(500)\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
            #         switches[i-1] = 1

            elif (lines[i].count(sw[0])) and (switches[int(num[0])] == 0) and (false_pin != True):
                curent_pin = num[0]
                print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                switches[int(curent_pin)] = 1

            elif (lines[i].count(sw[0])) and switches[int(num[0])] == 1 and false_pin != True:
                curent_pin = num[0]
                print("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(100);\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                output_file.write("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(100);\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                switches[int(curent_pin)] = 0
                #switches.insert(int(lines[i][-2]),1)

            elif (lines[i].count(end[0])):
                print(switches)
                input_file.close()
                output_file.write("}")
                output_file.close()
                break
else:

    errors_file.write("Файл отсутствует\n")
    print("Файл отсутствует\n")
errors_file.close()









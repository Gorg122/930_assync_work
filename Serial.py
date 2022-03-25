import re
import time
import serial
import os

# Вывод актуальной директории исполняемого скрипта.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)



# выведем все строки включая пустые
print(len(re.findall(r"[\n']+?", open('buttons.txt').read())))
all_strings = len(re.findall(r"[\n']+?", open('buttons.txt').read()))

# выведем количество без пустых строк
print(len(re.findall(r"[\n']+", open('buttons.txt').read())))
strings = len(re.findall(r"[\n']+", open('buttons.txt').read()))
# if all_strings != strings:
#     errors_file.write("Ваш файл сценария не должен содержать пустых строк")

input_file = open("buttons.txt")
errors_file = open("errors.txt", "w")
#output_file = open("scetch.txt", "w")
lines = input_file.readlines()

curent_pin = 0
but = ["button"]
sw = ["switch"]
end = ["end"]
empty = [""]
numbers = ["12345678"]
not_count = ["09"]
delay = ["delay"]
start = ["start"]
h1 = ["1H"]
switches = dict([(1, 0),(2, 0),(3, 0),(4, 0),(5, 0),(6, 0),(7, 0),(8, 0)])
current_commands = 0


# arduino.write(bytes("H","utf-8"))
# arduino.write(bytes("e","utf-8"))
# arduino.write(bytes("l","utf-8"))
# arduino.write(bytes("l","utf-8"))
# arduino.write(bytes("o","utf-8"))
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)
y = 0
# while y != 1:
#     poslanie = "Hello"
#     arduino.write(bytes(poslanie, 'utf-8'))
#     time.sleep(1)
#     # data1 = arduino.readline()
#     # time.sleep(1)
#     # print(data1)
#     data = arduino.readline()
#     time.sleep(1)
#     print(data)
#     if str(data).count(start[0]):
#         print("Poluchenorazhreshenie")
#         y += 1
y = 0
#waiting for device
time.sleep(3)
while y != 1:
    poslanie = "Hello\n"
    print("prohodka")
    #st = str(poslanie)
    arduino.write(bytearray(poslanie, 'utf-8'))
    #data = arduino.readline()
    #data = arduino.read(arduino.inWaiting())
    data = str(arduino.readline().decode().strip('\r\n'))
    if str(data).count(start[0]):
        print("Poluchenorazhreshenie")
        #data = ""
        #poslanie = "1H"
        #arduino.write(bytes(poslanie, 'utf-8'))
        y += 1
#data = arduino.read(arduino.inWaiting())
for i in range(strings+1):
    is_empty = len(lines[i])
    if is_empty < 2:
        print("Empty string\n")
        errors_file.write("Файл не должен содержать пустых строк\n")
        i = i + 1
    elif (not_count[0].count(lines[i][-2])):
        print("Pins must be from 1 to 8")
        errors_file.write("Пины должны иметь значения от 1 до 8\n")
    else:
        curent_pin = lines[i][-2]
    if (numbers[0].count(lines[i][-2])):
        if (lines[i].count(but[0])):
            #print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(500)\n digitalWrite(pin"+str(curent_pin)+", LOW);\n")
            #output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(500);\n digitalWrite(pin"+str(curent_pin)+", LOW);\n")
            comand_but1 = str(curent_pin) + "H\n"
            y = 0
            data = ""
            #while y != 1:
            arduino.write(bytearray(comand_but1, 'utf-8'))
            #arduino.write(bytes("", 'utf-8'))
            time.sleep(1)
                #if data.count(h1[0]):
                    #y += 1
            print("YES")
            #arduino.write(bytes("NO", 'utf-8'))
            print(comand_but1)
            time.sleep(1)
            print(data)
            data = ""
            time.sleep(0.5)
            comand_but2 = str(curent_pin) + "L\n"
            arduino.write(bytearray(comand_but2, 'utf-8'))
            print(comand_but2)
            time.sleep(1)
            print(data)
            current_commands += 1

        elif (lines[i].count(sw[0])) and switches[int(curent_pin)] == 0:
            #print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(500);\n")
            #output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(500);\n")
            comand_sw1 = str(curent_pin) + "H\n"
            arduino.write(bytearray(comand_sw1, 'utf-8'))
            print(comand_sw1)
            time.sleep(1)
            print(data)
            time.sleep(0.5)
            switches[int(curent_pin)] = 1
            current_commands += 1

        elif (lines[i].count(sw[0])) and switches[int(curent_pin)] == 1:
            #print("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(500);\n")
            #output_file.write("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(500);\n")
            comand_sw2 = str(curent_pin) + "L\n"
            arduino.write(bytearray(comand_sw2, 'utf-8'))
            print(comand_sw2)
            time.sleep(1)
            print(data)
            time.sleep(0.5)
            switches[int(curent_pin)] = 0
            current_commands += 1
        elif (lines[i].count(end[0])):
            print(switches)
            print(data[1])
            break
#output_file.write("}")
input_file.close()
#output_file.close()
errors_file.close()
print(current_commands)
serial.Serial.close(arduino)











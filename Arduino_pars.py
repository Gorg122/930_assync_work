import re
errors_file = open("errors.txt", "w")
# выведем все строки включая пустые
print(len(re.findall(r"[\n']+?", open('buttons.txt').read())))
all_strings = len(re.findall(r"[\n']+?", open('buttons.txt').read()))

# выведем количество без пустых строк
print(len(re.findall(r"[\n']+", open('buttons.txt').read())))
strings = len(re.findall(r"[\n']+", open('buttons.txt').read()))
if all_strings != strings:
    errors_file.write("Ваш файл сценария не должен содержать пустых строк")

input_file = open("buttons.txt")
output_file = open("scetch.ino", "w")
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

lines = input_file.readlines()
line = input_file.readline()

# итерация по строкам
print(lines[0][-2])
print(lines[0][5:11])
print(lines[3].count("button"))
but = ["button"]
sw = ["switch"]
end = ["end"]
switches = dict([(1, 0),(2, 0),(3, 0),(4, 0),(5, 0),(6, 0),(7, 0),(8, 0)])

for i in range(strings+1):
    if i > 9:
        errors_file.write("Количество активных пинов равно 9")
    elif (lines[i].count(but[0])):
        print("digitalWrite(pin" + str(lines[i][-2]) + ", HIGH);\n sleep(500)\n digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")

        output_file.write("digitalWrite(pin" + str(lines[i][-2]) + ", HIGH);\n delay(500);\n digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")

    elif (lines[i].count(sw[0])) and switches[int(lines[i][-2])] == 0:
        curent_pin = lines[i][-2]
        print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(500);\n")
        output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(500);\n")
        switches[int(curent_pin)] = 1

    elif (lines[i].count(sw[0])) and switches[int(lines[i][-2])] == 1:
        curent_pin = lines[i][-2]
        print("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(500);\n")
        output_file.write("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(500);\n")
        switches[int(curent_pin)] = 0
        #switches.insert(int(lines[i][-2]),1)

    elif (lines[i].count(end[0])):
        print(switches)
        break

output_file.write("}")
input_file.close()
output_file.close()


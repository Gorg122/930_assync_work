import os.path
import subprocess


def FPGA_flash(sof_path):
    # Задаем ключ успешной прошивки платы
    main_key = ["Quartus Prime Programmer was successful. 0 errors"]

    # Задаем директорию исполняемых файлов quartus
    # Задаем изначальную директорию исполняемых файлов Quartus
    quartus_path = "C:/intelFPGA_lite/21.1/quartus/bin64/quartus_pgm.exe"
    jtag_path = "C:/intelFPGA_lite/21.1/quartus/bin64/jtagconfig.exe"
    if os.path.exists(quartus_path):  # Проверяем существует ли данный путь исполняемых файлов
        quartus_root_path = quartus_path
        #print(quartus_root_path)
    # В случае если такого пути нет, производим поиск пути исполняемых файлов в корневой папке
    else:
        find_in = "C:/intelFPGA_lite"  # Задаем корневую папку
        name = "quartus_pgm.exe"
        for root, dirs, files in os.walk(find_in):  # В цикле проходим все папки и файлы в корневой папке
            if name in files:
                quartus_root_path = os.path.join(root, name)  # Добавляем в путь папки и необходимый файл
                # print(quartus_root_path)

    #Выводим порт подключения ПЛИС
    curent_FPGA = subprocess.run(quartus_root_path + " -l", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #print(curent_FPGA,"\n")
    #print(curent_FPGA.returncode,"\n") # флаг успешного выполнения команды
    #print(curent_FPGA.stdout,"\n") # Вывод консоли

    # Достаем название устройства и порт подключения
    #print(curent_FPGA.stdout.split('\n', 1)[0])
    curent_port = curent_FPGA.stdout.split('\n', 1)[0]
    curent_port = str(curent_port[3:])
    print(curent_port)

    if not curent_FPGA:
        raise IOError("Плата ПЛИС не найдена")


    modules_FPGA = subprocess.run("{0} -c \"{1}\" -a".format(quartus_root_path, curent_port), stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True)
    #modules_FPGA = subprocess.run(quartus_root_path + " -c \""+curent_port+"\" -a", stdout=subprocess.PIPE,
    #                              stderr=subprocess.PIPE, text=True)
    print(modules_FPGA, "\n")
    print(modules_FPGA.returncode, "\n")  # флаг успешного выполнения команды
    print(modules_FPGA.stdout, "\n")  # Вывод консоли

    #for devices in modules_FPGA.stdout.split('\n', 4)[3]:
        #curent_device = devices
    #Multipl_FPGA = subprocess.run(jtag_path, stdout=subprocess.PIPE,
     #                             stderr=subprocess.PIPE, text=True)
    i = 0
    print(modules_FPGA.stdout.split('\n\n', 2)[0])
    cur_dev = modules_FPGA.stdout.rsplit('Info: ***************', 2)[0]
    print(cur_dev,'\n')
    print(cur_dev)
    print(type(cur_dev))
    device_numbers = cur_dev.split('\n')
    print(device_numbers)
    print(type(device_numbers))
    #if len(device_numbers) >= 4:
    #    print("Govno")
    #for i in device_numbers:

    #devices = cur_dev.split('\n',3)
    #print(devices,'\n')
    #for device in cur_dev:
    #    i += 1
    if len(device_numbers) > 4:
        curent_device = modules_FPGA.stdout.split('\n', 3)[2]
        #curent_device = modules_FPGA.stdout.split('\n', 3)[0]
        curent_device = str(curent_device[12:36])
        #print(curent_device)
        print("Pidor")
        result = subprocess.run('{0} -m JTAG -c "{1}" -o p;{2}@{3}'.format(quartus_root_path, curent_port, sof_path, i),
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout, '\n')  # Вывод консоли
        if result.stdout.count(main_key[0]):
            return ("OK")
        else:
            return ("Прошить плату не удалось")

    # Задаем параметры прошивки ПЛИС
    # sof_path = "C:/intelFPGA_lite/Project/NEW_PROTOTYPE_2/golden.sof"
    #result = subprocess.run("{0} -c \"{1}\" -m JTAG -o p;{2}".format(quartus_root_path, curent_port, sof_path),
    #                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    else:
        print("Net")
        result = subprocess.run('{0} -m JTAG -c "{1}" -o p;{2}'.format(quartus_root_path, curent_port, sof_path),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout,'\n') # Вывод консоли

        if result.stdout.count(main_key[0]):
            return ("OK")
        else:
            return ("Прошить плату не удалось")
    # print(result.stderr,'\n')


#FPGA_flash(sof_path="C:/py/DE1_SoC_Default.sof")
print(FPGA_flash(sof_path="C:/intelFPGA_lite/Project/For_lida/golden.sof"))
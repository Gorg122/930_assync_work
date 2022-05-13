import os.path
import subprocess
import sys
import time
import shlex

def FPGA_flash(User_path):

    # Задаем ключ успешной прошивки платы
    main_key = ["Quartus Prime Programmer was successful. 0 errors"]

    # Задаем директорию исполняемых файлов quartus
    # Задаем изначальную директорию исполняемых файлов Quartus
    Quartus_pgm_path = "C:/intelFPGA_lite/17.0/quartus/bin64/quartus_pgm.exe"
    Quartus_jtag_path = "C:/intelFPGA_lite/17.0/quartus/bin64/jtagconfig.exe"
    Quartus_sh_path = "C:/intelFPGA_lite/17.0/quartus/bin64/quartus_sh.exe"
    root_directory = "C:/PROJECT_930/Prototype_new_2"
    # Задаем необходимые переменные
    qpf_path = "Not_yet"
    qsf_path = "Not_yet"
    sof_path = "Not_yet"

    log_file = open(User_path + "/JTAG_config.txt", "w")
    #compil_file = open(User_path + "/Proj_compilation.txt", "w")

    minus = "quartus_pgm.exe"

    if os.path.exists(Quartus_pgm_path):  # Проверяем существует ли данный путь исполняемых файлов
        Quartus_pgm_path = Quartus_pgm_path
        Quartus_root_path = Quartus_pgm_path.replace(minus,'')
       # print(Quartus_root_path,'\n')
    # В случае если такого пути нет, производим поиск пути исполняемых файлов в корневой папке

    # Вот твой пример поиска по всем вложенным папка по конкретному названию файла
    else:
        find_in = "C:/intelFPGA_lite"  # Задаем корневую папку
        name = "quartus_pgm.exe"
        for root, dirs, files in os.walk(find_in):  # В цикле проходим все папки и файлы в корневой папке
            if name in files:
                Quartus_pgm_path = os.path.join(root, name)  # Добавляем в путь папки и необходимый файл
        Quartus_root_path = Quartus_pgm_path.replace(minus,'')
        #print(Quartus_root_path,'\n')
    ful_path = "C:/PROJECT_930/Prototype_new_2"
    if os.path.exists(Quartus_sh_path):  # Проверяем существует ли данный путь исполняемых файлов
        Quartus_sh_path = Quartus_sh_path

        #Quartus_root_path = Quartus_sh_path - minus
        #print(Quartus_root_path)
    # В случае если такого пути нет, производим поиск пути исполняемых файлов в корневой папке

    else:
        find_in = "C:/intelFPGA_lite"  # Задаем корневую папку
        name = "quartus_sh.exe"
        for root, dirs, files in os.walk(find_in):  # В цикле проходим все папки и файлы в корневой папке
            if name in files:
                Quartus_sh_path = os.path.join(root, name)  # Добавляем в путь папки и необходимый файл
                print(Quartus_sh_path)
        #Quartus_root_path = Quartus_sh_path - minus
    for qpf_file in os.listdir(User_path):
        if qpf_file[qpf_file.rfind(".") + 1:] in ['qpf']:
            # full_path = os.path.join(directory, file_name)
            qpf_path = ful_path + "/" + User_path + "/" + qpf_file
            print(qpf_path,'\n')

    for qsf_file in os.listdir(User_path):
        if qsf_file[qsf_file.rfind(".") + 1:] in ['qsf']:
            # full_path = os.path.join(directory, file_name)
            qsf_path = ful_path + "/" + User_path + "/" + qsf_file
            print(qsf_path,'\n')

    for root, dirs, files in os.walk(User_path):
        for file in files:
            if file.endswith(".sof"):
                sof_path = os.path.join(ful_path, root, file)
                print(sof_path)

    if (os.path.exists(qpf_path)) and (os.path.exists(qsf_path)) and not(os.path.exists(sof_path)):
        #Change_dir = os.system("cd {0}".format(User_path))
        #print("cd {0}".format(User_path), '\n')
        #print(Change_dir, '\n')


        Compil_file = "Proj_compil_result.txt"
        #md_path = 'C:\Windows\WinSxS\wow64_microsoft - windows - commandprompt_31bf3856ad364e35_10.0.19041.746_none_735abbdbad8c902f\cmd.exe'
        #command = 'cd {0}&&{1} --flow compile <{2}> [-c {3}] > Jtag_config.txt'.format(User_path, Quartus_sh_path, qpf_path, qsf_path)
        command = "{0} --flow compile <{1}> [-c {2}] >{3}".format(Quartus_sh_path, qpf_path, qsf_path, Compil_file)

        #command1 = 'cd {0}'.format(User_path)
        #Project_compilation = os.system("{0} --flow compile < {1} > [-c {2}".format(Quartus_sh_path,qpf_path,qsf_path))
        os.chdir(User_path)
        # pre_compil = os.system(command1)
        # Proj_comp = os.system(command)
        #
        # print(Proj_comp)
        # Project_compilation = subprocess.run(command1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        #os.chdir(User_path)
        print(User_path)
        print("Проект ПЛИС компилируется\n")
        Project_compilation1 = subprocess.run(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=True)
        #Project_compilation.stdin = command
        #print(Project_compilation.stde
        # print(Project_compilation.stdout,'\n')
        # print(Project_compilation,'\n')
        print(Project_compilation1.stdout, '\n')
        print(Project_compilation1, '\n')
        print("Компиляция окончена\n")
        os.chdir(root_directory)




        # Project_compilation = subprocess.run(
        #     "cd {0}; {1} --flow compile <{2}> [-c {3}]".format(User_path, Quartus_sh_path, qpf_path, qsf_path), stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE, text=True)


        # command = '''
        # ['cd', '{0}';
        # '{1}', '--flow compile <{2}> [-c {3}]']
        # '''.format(User_path, Quartus_sh_path, qpf_path, qsf_path)
        # print(command)

        #command1 = 'cd {0}'.format(User_path)
        #command2 = '{0} --flow compile <{1}> [-c {2}]'.format(Quartus_sh_path, qpf_path, qsf_path)

        #process = subprocess.Popen(['C:\Windows\WinSxS\wow64_microsoft-windows-commandprompt_31bf3856ad364e35_10.0.19041.746_none_735abbdbad8c902f\cmd.exe', "cd [{0}]".format(User_path), "{0} [--flow compile <{1}> [-c {2}]".format(Quartus_sh_path, qpf_path, qsf_path)], stdout=subprocess.PIPE, shell=True, text=True)

        # process = subprocess.Popen([
        #                                "cd {0}".format(User_path),
        #                                "{0} --flow compile <{1}> [-c {2}]".format(Quartus_sh_path, qpf_path,
        #                                                                            qsf_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                            shell=True)

        #out, err = process.communicate(command)
        # print(process.stdout)
        # print(process.stderr)
        # print(process)
        #
        #
        # #Project_compil = os.system("quartus_sh --flow compile < {0} > [-c {1}]".format(qpf_path, qsf_file))
        # #print(Project_compilation.stdout,'\n')
        # compil_file.write(process.stdout)
        # print(Project_compilation)
        #
        # command = "echo a; echo b"




        # ret1 = subprocess.call('cd {0}'.format(User_path), capture_output=True, text=True)
        # ret2 = subprocess.call('{0} --flow compile <{1}> [-c {2}]'.format(Quartus_sh_path, qpf_path, qsf_path), capture_output=True, text=True)

        #ret1 = subprocess.call('cd {0}'.format(User_path))
        #ret2 = subprocess.call('{0} --flow compile <{1}> [-c {2}]'.format(Quartus_sh_path, qpf_path, qsf_path))
        # before Python 3.7:
        # # before Python 3.7:
        # ret = subprocess.run(command, stdout=subprocess.PIPE, shell=True)

        #print(ret1, '\n')
        #print(ret2, '\n')




        #print(ret.stdout, '\n')
        #print(ret.stderr, '\n')

    #    sof_file_find = False
    #     timer = 0
    #     while not (sof_file_find):
    #         for root, dirs, files in os.walk(User_path):
    #             for file in files:
    #                 print("Poisk_sof\n")
    #                 timer += 1
    #                 if timer > 2000:
    #                     sys.exit()
    #                 if file.endswith(".sof"):
    #                     print("Poisk")
    #                     sof_path = os.path.join(root, file)
    #                     print(sof_path)
    #                     sof_file_find = True
    # elif (os.path.exists(sof_path)):
    #     sof_file_find = False
    #     #sof_dir = User_path + "\\output_files"
    #     # while not(sof_file_find):
    #     #     for sof_file in os.listdir(User_path):
    #     #         #time.sleep(5)
    #     #         #print("Poisk")
    #     #         if sof_file[sof_file.rfind(".") + 1:] in ['sof']:
    #     #             # full_path = os.path.join(directory, file_name)
    #     #             sof_path = sof_dir + "\\" + sof_file
    #     #             sof_file_find = True
    #     #             #print(sof_path,'\n')
    #     timer = 0
    #     while not (sof_file_find):
    #         for root, dirs, files in os.walk(User_path):
    #             for file in files:
    #                 print("Poisk_sof\n")
    #                 timer += 1
    #                 if timer > 2000:
    #                     sys.exit()
    #                 if file.endswith(".sof"):
    #                     print("Poisk")
    #                     sof_path = os.path.join(root, file)
    #                     print(sof_path)
    #                     sof_file_find = True

        # while not(sof_file_find):
        #     for root, dirs, files in os.walk(User_path):  # В цикле проходим все папки и файлы в корневой папке
        #         time.sleep(5)
        #         print("Poisk")
        #         if files[files.rfind(".") + 1:] in ['sof']:
        #             # full_path = os.path.join(directory, file_name)
        #             sof_path = root + "\\" + files
        #             sof_file_find = True
        #             print(sof_path,'\n')


    #quartus_sh - -flow compile < C:\intelFPGA_lite\Project\Proj_compil\lab1.qpf > [-c C:\intelFPGA_lite\Project\Proj_compil\lab1.qsf]
    #Выводим порт подключения ПЛИС

    for root, dirs, files in os.walk(User_path):
        for file in files:
            if file.endswith(".sof"):
                sof_path = os.path.join(ful_path, root, file)
                print(sof_path)

    if os.path.exists(sof_path):
        print("Proshivka")
        curent_FPGA = subprocess.run(Quartus_pgm_path + " -l", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(curent_FPGA,"\n")
        # print(curent_FPGA.returncode,"\n") # флаг успешного выполнения команды
        # print(curent_FPGA.stdout,"\n") # Вывод консоли

        # Достаем название устройства и порт подключения
        #print(curent_FPGA.stdout.split('\n', 1)[0])

        curent_port = curent_FPGA.stdout.split('\n', 1)[0]
        curent_port = str(curent_port[3:])
        print(curent_port)

        if not curent_FPGA:
           raise IOError("Плата ПЛИС не найдена")


        modules_FPGA = subprocess.run("{0} -c \"{1}\" -a".format(Quartus_pgm_path, curent_port), stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)


        #modules_FPGA = subprocess.run(quartus_root_path + " -c \""+curent_port+"\" -a", stdout=subprocess.PIPE,
        #                             stderr=subprocess.PIPE, text=True)

        # print(modules_FPGA, "\n")
        # print(modules_FPGA.returncode, "\n")  # флаг успешного выполнения команды
        # print(modules_FPGA.stdout, "\n")  # Вывод консоли

        #for devices in modules_FPGA.stdout.split('\n', 4)[3]:
            #curent_device = devices
        #Multipl_FPGA = subprocess.run(jtag_path, stdout=subprocess.PIPE,
         #                             stderr=subprocess.PIPE, text=True)

        i = 0

        #print(modules_FPGA.stdout.split('\n\n', 2)[0])
        cur_dev = modules_FPGA.stdout.rsplit('Info: ***************', 2)[0]
        # print(cur_dev,'\n')
        # print(cur_dev)
        # print(type(cur_dev))
        device_numbers = cur_dev.split('\n')
        # print(device_numbers)
        # print(type(device_numbers))




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
            print("Несколько ядер")
            result = subprocess.run('{0} -m JTAG -c "{1}" -o p;{2}@{3}'.format(Quartus_pgm_path, curent_port, sof_path, i),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout, '\n')  # Вывод консоли
            log_file.write(result.stdout)
            log_file.close()
            if result.stdout.count(main_key[0]):
                return ("OK")
                print("OK")
            else:
                return ("Прошить плату не удалось")
                print("Neok")
        # Задаем параметры прошивки ПЛИС
        # sof_path = "C:/intelFPGA_lite/Project/NEW_PROTOTYPE_2/golden.sof"

        #result = subprocess.run("{0} -c \"{1}\" -m JTAG -o p;{2}".format(quartus_root_path, curent_port, sof_path),
        #                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        else:
            print("Одно ядро\n")
            print(sof_path+"\n")
            result = subprocess.run('{0} -m JTAG -c "{1}" -o p;{2}'.format(Quartus_pgm_path, curent_port, sof_path),
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            log_file.write(result.stdout)
            log_file.close()
            #print(result.stdout,'\n') # Вывод консоли

            if result.stdout.count(main_key[0]):
                return ("OK")
            else:
                return ("Прошить плату не удалось")
        #print(result.stderr,'\n')


#FPGA_flash(sof_path="C:/py/DE1_SoC_Default.sof")


#Тут задаешь тот самый путь к папке с проектом
#print(FPGA_flash(User_path="C:/intelFPGA_lite/Project/Proj_compil"))
#if __name__ == '__main__':

#FPGA_flash(User_path="C:\PROJECT_930\Prototype_new\Probnik\Project_2")


#FPGA_flash(User_path="C:\PROJECT_930\Prototype_new\Probnik\Ptoject_2\Lab_1\Script\lab1_2")



#FPGA_flash(User_path="C:\PROJECT_930\Prototype_new\student_zip\sasha.lorens@yandex.ru")
#FPGA_flash(User_path="C:/PROJECT_930/Prototype_new_2/student_zip/Desorder2881488")

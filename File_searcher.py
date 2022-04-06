def Files_search:
    minus = "quartus_pgm.exe"

        if os.path.exists(Quartus_pgm_path):                    # Проверяем существует ли данный путь исполняемых файлов
            Quartus_pgm_path = Quartus_pgm_path
            Quartus_root_path = Quartus_pgm_path.replace(minus,'')      # Создаем переменную пути к папке пользователя
            print(Quartus_root_path,'\n')
        # В случае если такого пути нет, производим поиск пути исполняемых файлов в корневой папке

        else:
            find_in = "C:/intelFPGA_lite"  # Задаем корневую папку
            name = "quartus_pgm.exe"
            for root, dirs, files in os.walk(find_in):  # В цикле проходим все папки и файлы в корневой папке
                if name in files:
                    Quartus_pgm_path = os.path.join(root, name)  # Добавляем в путь папки и необходимый файл
            Quartus_root_path = Quartus_pgm_path.replace(minus,'')
            print(Quartus_root_path,'\n')

        if os.path.exists(Quartus_sh_path):  # Проверяем существует ли данный путь исполняемых файлов
            Quartus_sh_path = Quartus_sh_path

            #Quartus_root_path = Quartus_sh_path - minus
            #print(Quartus_root_path)
        # В случае если такого пути нет, производим поиск пути исполняемых файлов в корневой папке

        else:                                                       # Поиск расположения quartus_sh.exe
            find_in = "C:/intelFPGA_lite"                           # Задаем корневую папку
            name = "quartus_sh.exe"
            for root, dirs, files in os.walk(find_in):              # В цикле проходим все папки и файлы в корневой папке
                if name in files:
                    Quartus_sh_path = os.path.join(root, name)      # Добавляем в путь папки и необходимый файл
                    print(Quartus_sh_path)
            #Quartus_root_path = Quartus_sh_path - minus

        for qpf_file in os.listdir(User_path):                      # Производим поиск qpf файла в папке пользователя
            if qpf_file[qpf_file.rfind(".") + 1:] in ['qpf']:
                # full_path = os.path.join(directory, file_name)
                qpf_path = User_path + "\\" + qpf_file
                print(qpf_path,'\n')

        for qsf_file in os.listdir(User_path):                      # Производим поиск qsf файла в папке пользователя
            if qsf_file[qsf_file.rfind(".") + 1:] in ['qsf']:
                # full_path = os.path.join(directory, file_name)
                qsf_path = User_path + "\\" + qsf_file
                print(qsf_path,'\n')

        # Change_dir = subprocess.run("cd {0}".format(quartus_root_path))
        # print(Change_dir,'\n')

        Change_dir = os.system("cd {0}".format(User_path))
        print(Change_dir, '\n')
Files_search()
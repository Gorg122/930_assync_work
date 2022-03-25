import warnings
import subprocess

#Задаем директорию исполняемых файлов quartus
quartus_root_path = "C:/intelFPGA_lite/17.1/quartus/bin64/quartus_pgm.exe"
#Вывод порта подключения ПЛИС
curent_FPGA = subprocess.run(quartus_root_path + " -l", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(curent_FPGA,"\n")
#print(curent_FPGA.returncode,"\n")
print(curent_FPGA.stdout,"\n")
#Достаем название устройства и порт подключения
print(curent_FPGA.stdout.split('\n', 1)[0])
curent_port = curent_FPGA.stdout.split('\n', 1)[0]
curent_port = str(curent_port [2:])
print(curent_port)

if not curent_FPGA:
    raise IOError("No FPGA found")

#Задаем параметры прошивки ПЛИС
sof_path = "C:/PROJECT_930/PROTOTYPE/golden.sof"
result = subprocess.call("{0} -c \"{1}\" -m JTAG -o p;{2}".format(quartus_root_path,curent_port,sof_path))
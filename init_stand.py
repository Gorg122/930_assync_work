import subprocess
import sys
import configparser

##pip3.main(['install', 'subprocess'])

subprocess.check_call([sys.executable, 'pip', 'update'])
subprocess.check_call([sys.executable, 'pip', 'upgrade'])
package = 'subprocess', \
          'PyMySQL', \
          'pyserial', \
          'pywin32', \
          'google.oauth2', \
          'googleapiclient.http', \
          'googleapiclient.discovery', \
          'googleapiclient.discovery', \
          'opencv-contrib-python', \
          'google-api-python-client'
for item in range(len(package)):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package[item]])



curent_FPGA = subprocess.run(Quartus_pgm_path + " -l", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(curent_FPGA)
print("Укажите плату с каким индексом в данный момент необходимо использовать")
fpgas = curent_FPGA.stdout.split('*********************', 2)[0]
print(fpgas)
if fpgas.find("1)") != -1 and fpgas.find("2)") == -1:
    print("Используется одна плата, будет использован ее индекс")
    port = 1
if fpgas.find("1)") != -1 and fpgas.find("2)") != -1:
    input("Укажите плату с каким индексом в данный момент необходимо использовать ", port)
config = configparser.ConfigParser()
config.read("Config.ini")
config['FPGA']['port'] = port
with open('Config.ini', 'w') as configfile:
    config.write(configfile)


import warnings
import serial
import serial.tools.list_ports

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description  # may need tweaking to match new arduinos
]
if not arduino_ports:
    raise IOError("Плата Arduino не найдена")
if len(arduino_ports) > 1:
    warnings.warn('Найдено несколько плат Arduino')

ser = serial.Serial(arduino_ports[0])
print(ser,'\n')
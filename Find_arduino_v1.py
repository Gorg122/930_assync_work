import warnings
import serial
import serial.tools.list_ports

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description  
]
if not arduino_ports:
    raise IOError("Плата Ардуино не найдена")
if len(arduino_ports) > 1:
    warnings.warn('Найдено несколько плат будет использована первая')

ser = serial.Serial(arduino_ports[0])
print(ser)
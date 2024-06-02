# Importing Libraries
import random

import serial
import time

# https://projecthub.arduino.cc/ansh2919/serial-communication-between-python-and-arduino-663756
arduino = serial.Serial(
    port='/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_44238313938351E04290-if00',
    baudrate=9600,
    timeout=1)
# /dev/ttyACM0
# https://stackoverflow.com/questions/23669855/linux-pyserial-could-not-open-port-dev-ttyama0-no-such-file-or-directory
# ls /dev/serial/by-id/


def write_read(x):
    transfer = bytes(x, 'utf-8')
    print(f"Sending \"{transfer}\"")
    arduino.write(transfer)
    time.sleep(0.05)
    # data = arduino.readline()
    return 'Send'


def test_data_transfer():
    # name;value;min;max
    data = """temperature;15;-10;35
storage;4000;0;13500
radiation;0.125;0;1
demand;350;0;1500
wind;3.5;0;10
generation;450;0;1500""".split('\n')
    time.sleep(5)
    for i in range(0, len(data)):
        write_read(data[i] + '\n')
        time.sleep(3)

def test_radiation_speed():
    # name;percentage;COLOR
    # \d{2};0\.\d{3};\d{2}
    data = """WND;0.125;0;1
radiation;0.95;0;1
radiation;0.5;0;1
radiation;0.125;0;1
radiation;0.75;0;1""".split('\n')
    time.sleep(5)
    #for i in range(0, len(data)):
    #    write_read(data[i] + '\n')
    #    time.sleep(3)
    colors = ['BLACK', 'WHITE', 'RED', 'LIME', 'YELLOW', 'CYAN', 'MAGENTA', 'MAROON', 'OLIVE', 'GREEN']
    maxlen = max([len(x) for x in colors])
    while True:
        write_read(f'{3:2};{0:.3f};{random.randint(0, len(colors) - 1):2}\n')
        time.sleep(3)
        write_read(f'{3:2};{random.random():.3f};{random.randint(0, len(colors) - 1):2}\n')
        time.sleep(3)
        write_read(f'{3:2};{1:.3f};{random.randint(0, len(colors) - 1):2}\n')
        time.sleep(3)


def test_arduino():
    while True:
        num = input("Enter a number: ")  # Taking input from user
        value = write_read(num)
        print(value)  # printing the value


if __name__ == '__main__':
    # https://projecthub.arduino.cc/ansh2919/serial-communication-between-python-and-arduino-663756
    # test_data_transfer()
    test_radiation_speed()

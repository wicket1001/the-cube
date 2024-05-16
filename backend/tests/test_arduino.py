# Importing Libraries
import serial
import time

arduino = serial.Serial(port='/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_75533353837351B0A150-if00', baudrate=9600, timeout=.1)  # /dev/ttyACM0


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


def test_arduino():
    while True:
        num = input("Enter a number: ")  # Taking input from user
        value = write_read(num)
        print(value)  # printing the value


if __name__ == '__main__':
    # https://projecthub.arduino.cc/ansh2919/serial-communication-between-python-and-arduino-663756
    test_data_transfer()

# Importing Libraries
import serial
import time

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


def test_arduino():
    while True:
        num = input("Enter a number: ")  # Taking input from user
        value = write_read(num)
        print(value)  # printing the value


if __name__ == '__main__':
    # https://projecthub.arduino.cc/ansh2919/serial-communication-between-python-and-arduino-663756
    test_arduino()

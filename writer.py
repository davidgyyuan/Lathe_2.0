import serial

ser = serial.Serial('/dev/cu.usbmodem1411', 9600)


def write(degrees):
    """
    Writes to Arduino a number in string format.
    :param degrees: A string that can be parsed to an int
    """
    while True:
        while not is_accepting_input():
            pass
        ser.write(degrees.encode())


def is_accepting_input():
    """"
    :return: Boolean representing if the Arduino is ready to accept an input.
    """
    return ser.readline().startswith(b'y')

if __name__ == '__main__':
    write('50')

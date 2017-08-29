import serial

class Comms:
    def __init__(self, device: str):
        """
        :param device: Serial port Arduino is located on.
        """
        self.ser = serial.Serial(device, 9600)

    def write(self, degrees: str):
        """
        Writes to Arduino a number in string format.
        :param degrees: A string that can be parsed to an int
        """
        while True:
            while not self.is_accepting_input():
                pass
            self.ser.write(degrees.encode())

    def is_accepting_input(self):
        """"
        :return: Boolean representing if the Arduino is ready to accept an input.
        """
        status = self.ser.read(2)
        return status[0] == 84

    def is_powered(self):
        """"
        :return: Boolean representing if the server board is powered.
        """
        status = self.ser.read(2)
        return status[1] == 84


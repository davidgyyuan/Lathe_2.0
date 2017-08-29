import gui
import comms

import tkinter

if __name__ == "__main__":
    root = tkinter.Tk()
    mainFrame = gui.Frame(root)
    root.resizable(width=False, height=False)
    root.after(500, func=mainFrame.check())
    root.mainloop()


def start(device: str, file):
    """
    Starts drilling process
    :param device: Serial port to send and receive info.
    :param file: File to read data from
    """
    port = comms.Comms(device)


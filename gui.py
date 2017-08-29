import comms
import tkinter
from tkinter import filedialog
import platform
import os
import subprocess

class Frame(tkinter.Frame):
    def __init__(self, parent):
        """Define frame components and instance variables."""
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.row_counter = -1
        self.file = None
        self.filename_text = tkinter.StringVar()
        self.serial_options = subprocess.getoutput("ls /dev/cu.*").split("\n")
        self.serial_choice = tkinter.StringVar()

        self.file_frame = tkinter.Frame()
        self.begin_frame = tkinter.Frame()

        self.file_label = tkinter.Label(self.file_frame, textvariable=self.filename_text)
        self.file_select_button = tkinter.Button(self.file_frame, text="Select File", command=self.select_file)
        self.begin_button = tkinter.Button(self.begin_frame, text="Start Print", command=self.start_print)
        self.serial_drop = tkinter.OptionMenu(parent, self.serial_choice, *self.serial_options)

        self.initialize_user_interface()

        # Ensures GUI starts at front.
        if platform.system().startswith('Darwin'):
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        else:
            parent.lift()

    def initialize_user_interface(self):
        """Sets up user interface."""
        self.parent.title("Lathe 2.0 Interface")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="white")

        self.filename_text.set("File: None")
        for option in self.serial_options:
            self.serial_choice.set(option)
            if 'usbmodem' in option:
                break

        self.serial_drop.pack(fill=tkinter.X)

        self.file_frame.pack()
        self.file_label.pack(side=tkinter.LEFT)
        self.file_select_button.pack(side=tkinter.LEFT)

        self.begin_frame.pack()
        self.begin_button.pack()

    def select_file(self):
        """Brings up file selector and sets self.file"""
        filename = filedialog.askopenfilename()
        self.file = open(filename, "r")
        self.filename_text.set("File: " + os.path.basename(self.file.name))

    def start_print(self):
        """Begins the printing process"""
        port = comms.Comms(self.serial_choice.get())

    def complain(self, string: str):
        """
        Prints out problems to user in pop-up window.
        :param string: The string to be displayed to the user.
        """
        top = tkinter.Toplevel(master=self.parent)
        top.title("Something went wrong...")
        msg = tkinter.Message(top, text=string, width=1000)
        msg.pack(side="top", padx=10, pady=10)
        button = tkinter.Button(top, text="Dismiss", command=top.destroy)
        button.pack()

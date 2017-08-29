import main
import comms

import tkinter
from tkinter import filedialog, ttk
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
        self.power_text = tkinter.StringVar()

        self.file_frame = tkinter.Frame()
        self.begin_frame = tkinter.Frame()
        self.progress_frame = tkinter.Frame(relief=tkinter.GROOVE, borderwidth=1)
        self.progress_frame_row = tkinter.Frame(self.progress_frame)
        self.power_frame = tkinter.Frame()

        self.file_label = tkinter.Label(self.file_frame, textvariable=self.filename_text)
        self.file_select_button = tkinter.Button(self.file_frame, text="Select File", command=self.select_file)
        self.begin_button = tkinter.Button(self.begin_frame,
                                           state=tkinter.DISABLED, text="Start Print", command=self.start_print)
        self.serial_drop = tkinter.OptionMenu(parent, self.serial_choice, *self.serial_options)
        self.row_label = tkinter.Label(self.progress_frame_row, text="Row Progress:")
        self.row_progress = ttk.Progressbar(self.progress_frame_row,
                                            orient="horizontal", length=200, mode="determinate")
        self.col_label = tkinter.Label(self.progress_frame_row, text="Entire Progress:")
        self.col_progress = ttk.Progressbar(self.progress_frame_row,
                                            orient="horizontal", length=200, mode="determinate")
        self.power_label = tkinter.Label(self.power_frame, text="Status:")
        self.power_canvas = tkinter.Canvas(self.power_frame, width=24, height=24)
        self.power_status_label = tkinter.Label(self.power_frame, textvar=self.power_text)

        self.initialize_user_interface()

        # Ensures GUI starts at front.
        if platform.system().startswith('Darwin'):
            os.system(
                '''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
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
        self.power_canvas.create_oval(4, 8, 20, 24, outline="red", fill="red", width=2)
        self.power_text.set("Not connected")

        self.serial_drop.pack(fill=tkinter.X)
        self.file_frame.pack(fill=tkinter.X)
        self.file_label.pack(side=tkinter.LEFT)
        self.file_select_button.pack(side=tkinter.RIGHT)

        self.begin_frame.pack()
        self.begin_button.pack()

        self.progress_frame.pack(fill=tkinter.X, padx=3, pady=3)
        self.progress_frame_row.pack(fill=tkinter.X)
        self.row_label.grid(row=0)
        self.row_progress.grid(row=0, column=1)
        self.col_label.grid(row=1)
        self.col_progress.grid(row=1, column=1)

        self.power_frame.pack(fill=tkinter.X)
        self.power_label.pack(side=tkinter.LEFT)
        self.power_canvas.pack(side=tkinter.LEFT)
        self.power_status_label.pack(side=tkinter.LEFT)

    def select_file(self):
        """Brings up file selector and sets self.file"""
        filename = filedialog.askopenfilename()
        self.file = open(filename, "r")
        self.filename_text.set("File: " + os.path.basename(self.file.name))
        if self.file is not None:
            self.begin_button.config(state=tkinter.NORMAL)

    def start_print(self):
        """Begins the printing process"""
        main.start(self.serial_choice.get(), self.file)

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

    def check(self):
        """Continuous check for new info to update frame. Runs every half second."""
        # TODO:Insert power check
        self.parent.after(500, func=self.check)


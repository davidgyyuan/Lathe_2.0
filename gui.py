import tkinter
from tkinter import filedialog
import platform
import os


class Frame(tkinter.Frame):
    def __init__(self, parent):
        """Define frame components and instance variables."""
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.row_counter = -1
        self.file = None

        self.filename_text = tkinter.StringVar()
        self.file_label = tkinter.Label(textvariable=self.filename_text)
        self.file_select_button = tkinter.Button(text="Select File", command=self.select_file)

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
        self.file_label.grid(row=self.count(1), sticky=tkinter.NW)
        self.file_select_button.grid(row=self.count(1), sticky=tkinter.NW)

    def select_file(self):
        """Brings up file selector and sets self.file"""
        filename = filedialog.askopenfilename()
        self.file = open(filename, "r")
        self.filename_text.set("File: " + os.path.basename(self.file.name))

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

    def count(self, newline: int):
        """
        :param newline: Counter increments by how much.
        :return: Current count.
        """
        if newline:
            self.row_counter += 1
        return self.row_counter

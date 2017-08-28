import tkinter
import platform
import os


class Frame(tkinter.Frame):
    def __init__(self, parent):
        """Define frame components and instance variables."""
        tkinter.Frame.__init__(self, parent)
        self.parent = parent

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

    def complain(self, string):
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

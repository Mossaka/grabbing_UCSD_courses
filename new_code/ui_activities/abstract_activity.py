import tkinter as tk


class AbstractActivity(tk.Frame):
    """ Abstract activites show in the main page """
    def __init__(self, master=None, connector=None, *args, **kwargs):
        """ any activity should have one function frame and interactive frame"""
        super().__init__(master)
        self.is_show = False
        self._connector = connector

    def create_widgets(self):
        """ create all the widgets"""
        self.function_frame_()
        self.interactive_frame_()
        self.is_show = True

    def instruction_frame_(self):
        """ the implementation of the instruction frame"""
        pass

    def function_frame_(self):
        """ the implementation of the function frame"""
        pass

    def interactive_frame_(self):
        """ the implementation of the interactive frame"""
        pass

    def destroy(self):
        """ destroy all the frames """
        self.function_frame.pack_forget()
        self.interactive_frame.pack_forget()
        self.is_show = False

    def recover(self):
        """ recover all the frames """
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        self.interactive_frame.pack(fill=tk.BOTH)
        self.is_show = False

    def check_connection(self):
        return self._connector.connected

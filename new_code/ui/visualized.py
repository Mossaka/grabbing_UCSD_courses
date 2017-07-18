from new_code import Strings
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from new_code.connecting import Connector


class Visualized:
    def __init__(self, tk_frame=None, connector=None):
        self.tk_frame = tk_frame
        self.search_entry = None
        self.canvas = None
        self.search_frame = None
        self.interactive_frame = None
        self._connector = connector
        self._is_show = False

    def create_widgets(self):
        self.search_frame_()
        self.interactive_frame_()
        self._is_show = True

    def search_frame_(self):
        self.search_frame = tk.Frame(self.tk_frame, height=100, bd=2)
        self.search_frame.pack(fill=tk.BOTH, expand=True)

        self.search_entry = tk.Entry(self.search_frame, width=50)
        self.search_entry.grid(row=1, column=2, columnspan=10, sticky=tk.EW)
        self.search_entry.bind("<Return>", self._search)
        search_btn = tk.Button(self.search_frame, text='Search', command=self._search)
        search_btn.grid(row=1, column=12, sticky=tk.EW)
        self.search_frame.columnconfigure(0, weight=5)
        self.search_frame.rowconfigure(1, weight=5)
        self.search_frame.rowconfigure(3, weight=10)
        self.search_frame.columnconfigure(13, weight=5)

    def interactive_frame_(self):
        self.interactive_frame = tk.Frame(self.tk_frame, height=100)
        self.interactive_frame.pack(fill=tk.BOTH, expand=True)
        self.interactive_frame.columnconfigure(0, weight=1)
        self.interactive_frame.columnconfigure(1, weight=8)
        self.interactive_frame.columnconfigure(2, weight=1)
        self.interactive_frame.rowconfigure(0, weight=10)

        self.canvas = tk.Canvas(self.interactive_frame, width=800, height=400)
        self.canvas.grid(row=0, column=1, sticky=tk.NSEW)
        self.canvas.create_oval(100, 100, 400, 400, fill='blue')

    def _search(self, event=None):
        search_text = self.search_entry.get().upper()
        # whole match
        if self._connector.find_course(search_text):
            pass

    def destroy(self):
        self.search_frame.pack_forget()
        self.interactive_frame.pack_forget()
        self._is_show = False

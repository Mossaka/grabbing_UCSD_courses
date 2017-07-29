import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from new_code import Strings
from new_code.ui_activities.abstract_act import AbstractActivity


class TreeView(AbstractActivity):
    """ the treeview class """
    def __init__(self, tk_frame=None, connector=None):
        super().__init__(tk_frame)
        self.tk_frame = tk_frame
        self.search_entry = None
        self.tree_view = None
        self._connector = connector

    def instruction_frame_(self):
        self.instruction_frame = tk.Frame(self.tk_frame)
        self.instruction_frame.pack(fill=tk.BOTh, expand=True)

    def function_frame_(self):
        self.function_frame = tk.Frame(self.tk_frame, height=100, bd=2)
        self.function_frame.pack(fill=tk.BOTH, expand=True)

        self.search_entry = tk.Entry(self.function_frame, width=50)
        self.search_entry.grid(row=1, column=2, columnspan=10, sticky=tk.EW)
        self.search_entry.bind("<Return>", self._search)
        search_btn = tk.Button(self.function_frame, text='Search', command=self._search)
        search_btn.grid(row=1, column=12, sticky=tk.EW)
        self.function_frame.columnconfigure(0, weight=5)
        self.function_frame.rowconfigure(1, weight=5)
        self.function_frame.rowconfigure(3, weight=10)
        self.function_frame.columnconfigure(13, weight=5)

    def interactive_frame_(self):
        self.interactive_frame = tk.Frame(self.tk_frame, height=100)
        self.interactive_frame.pack(fill=tk.BOTH, expand=True)
        self.tree_view = ttk.Treeview(self.interactive_frame, columns=Strings.FIELDS, selectmode="extended")
        self.tree_view.grid(row=0, column=1, sticky=tk.NSEW)

        self.interactive_frame.columnconfigure(0, weight=1)
        self.interactive_frame.columnconfigure(1, weight=8)
        self.interactive_frame.columnconfigure(2, weight=1)
        self.interactive_frame.rowconfigure(0, weight=10)

        self.tree_view.heading('#0', text='Course ID', anchor=tk.CENTER)
        self.tree_view.heading('#1', text='Description', anchor=tk.CENTER)
        self.tree_view.heading('#2', text='Pre-requisites', anchor=tk.CENTER)
        self.tree_view.heading('#3', text='Sequence Courses', anchor=tk.CENTER)
        self.tree_view.column("#0", stretch=tk.YES, minwidth=10, width=20)

    def _search(self, event=None):
        search_text = self.search_entry.get().upper()
        # whole match
        if self._connector.find_course(search_text):
            course = self._connector.get_course(search_text)
            pre_ids = []
            for key in course.get_prere():
                pre_ids.append(course.get_prere()[key].get_course_id())
            post_ids = []
            for key in course.get_postre():
                post_ids.append(course.get_postre()[key].get_course_id())
            pre_id_str = ','.join(pre_ids)
            post_id_str = ','.join(post_ids)
            values = (course.get_description(), pre_id_str, post_id_str)
            self.tree_view.insert('', 'end', text=search_text, values=values)
        else:
            messagebox.showinfo('Course not Found!', 'Please enter another course ID')


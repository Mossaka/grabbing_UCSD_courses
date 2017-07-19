import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from new_code import Strings
from new_code.connecting import Connector
from new_code.ui.course_planner import CoursePlanner
from new_code.ui.tree_view import TreeView
from new_code.ui.visualized import Visualized


class MainPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self._connector = Connector()
        self.tree_view_frame = TreeView(master, self._connector)
        self.bubbles = Visualized(master, self._connector)
        self.course_planner = CoursePlanner(master, self._connector)
        self.parsed = False
        self.parse_progress = None
        self.pages = []
        self.create_widgets()

    def create_widgets(self):
        self.enter_frame()

    def enter_frame(self):
        _enter_frame = tk.Frame(self)
        _enter_frame.pack(fill=tk.BOTH, expand=True)

        self.parse_progress = ttk.Progressbar(_enter_frame, orient='horizontal', length=200, mode='determinate')
        grab_course_btn = tk.Button(_enter_frame, text=Strings.GET_COUR_BTN_STR, command=self.start_thread)

        tk.Button(_enter_frame, text=Strings.TREE_VIEW_BTN_STR, command=self.open_tree_view)\
            .grid(row=0, column=0, padx=10, pady=10)
        tk.Button(_enter_frame, text=Strings.VIS_BUBBLES_BTN_STR, command=self.open_bubbles) \
            .grid(row=0, column=1, padx=10, pady=10)
        tk.Button(_enter_frame, text=Strings.COURSE_PLANNER_BTN_STR, command=self.open_course_planner) \
            .grid(row=0, column=2, padx=10, pady=10)

        grab_course_btn.grid(row=0, column=4, pady=10, padx=10)
        self.parse_progress.grid(row=0, column=5, pady=10, padx=10)
        _enter_frame.columnconfigure(3, weight=4)
        _enter_frame.columnconfigure(8, weight=4)

        ttk.Separator(_enter_frame).grid(row=1, column=0, columnspan=10, sticky=tk.EW)
        self.parse_progress['value'] = 0

    def make_widges(self, page):
        page.create_widgets()
        self.pages.append(page)

    def destroy_existing_pages(self):
        for page in self.pages:
            if page is not None:
                page.destroy()

    def open_tree_view(self):
        self.destroy_existing_pages()
        self.make_widges(self.tree_view_frame)

    def open_bubbles(self):
        self.destroy_existing_pages()
        self.make_widges(self.bubbles)

    def open_course_planner(self):
        self.destroy_existing_pages()
        self.make_widges(self.course_planner)

    def start_thread(self):
        """ Multi-Threading implementation of parsing courses"""
        if self.parsed:
            messagebox.showinfo('Already Parsed', 'You have Already Parsed the courses!')
            return
        self.parse_course_thread = ParseCourseThread(self._connector)
        self.parse_course_thread.start()

        self.periodiccall()

    def periodiccall(self):
        """A periodic call while thread is still alive. Update the progress bar mainly"""
        self.parse_progress.step(0.25)
        if self.parse_course_thread.is_alive():
            self.after(100, self.periodiccall)
        else:
            self.parse_progress['value'] = 100
            self.parsed = True


class ParseCourseThread(threading.Thread):
    def __init__(self, connector):
        threading.Thread.__init__(self)
        self._connector = connector

    def run(self):
        """runs the main program"""
        self._connector.parse_all_majors()
        print("---start parsing courses from websites---")
        for ab, link in self._connector.major_links.items():
            if not self._connector.parse_courses(link):
                messagebox.showerror('Error', ConnectionError)
                exit()
        print("Parsing success!")
        print("---start parsing prerequisites and postrequisites---")

        self._connector.parse_prerequisites()
        self._connector.parse_postrequsites()

        print("Parsing success!")
        messagebox.showinfo('Parsing Success!', 'The courses have been parsed successfully!')
        exit()




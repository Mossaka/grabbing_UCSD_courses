import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pprint import pprint
from new_code import Strings
from new_code.connecting import Connector
from new_code.ui.info_course import ShowInfo
from new_code.ui.abstract_act import AbstractActivity
from new_code.ui.canvas_rect import AllCourses

class CoursePlanner(AbstractActivity):
    def __init__(self, tk_frame=None, connector=None):
        super().__init__(tk_frame)

        self.tk_frame = tk_frame
        self.enter_etr = None
        self.update_btn = None
        self._connector = connector
        self.courses = AllCourses.Instance()
        self.counter = 0
        self.row = 0

    def instruction_frame_(self):
        self.instruction_frame = tk.Frame(self.tk_frame)
        self.instruction_frame.pack(fill=tk.BOTh, expand=True)

    def function_frame_(self):
        self.function_frame = tk.Frame(self.tk_frame, height=100)
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.function_frame, text='New Course: ').grid(row=0, column=2, padx=20, pady=20)
        self.enter_etr = tk.Entry(self.function_frame)
        self.update_btn = tk.Button(self.function_frame, text='Update', command=self.update)
        self.update_btn.bind('<Return>', self.update)
        self.enter_etr.grid(row=0, column=3, padx=20, pady=20)
        self.update_btn.grid(row=0, column=1, padx=20, pady=20)

    def interactive_frame_(self):
        self.interactive_frame = tk.Frame(self.tk_frame)
        self.interactive_frame.pack(fill=tk.BOTH)
        self.canvas = tk.Canvas(self.interactive_frame, width=1200, height=1000)
        self.canvas.grid(row=1, column=0, pady=20, padx=20, sticky=tk.NSEW)

    def update(self, event=None):
        if not self.enter_etr.get():
            messagebox.showerror("Error: ", "No information is entered")

        course_id = self.enter_etr.get().upper()

        self.counter += 1
        if self.counter % 9 == 0:
            self.counter = 1
            self.row += 1

        x1 = Strings.INIT_X + Strings.PADDING_X * (self.counter - 1)
        y1 = Strings.INIT_Y + Strings.PADDING_Y * self.row
        x2 = x1 + Strings.REC_LEN
        y2 = y1 + Strings.REC_HEI
        self.make_rectangle(x1, y1, x2, y2, Strings.LIGHT_COLOR_CODES['blue'], course_id )

    def make_rectangle(self, x, y, width, height, color, course_id=None):
        if course_id:
            self.courses.allcourses[course_id] =\
                self.canvas.create_rectangle(x, y, width, height, fill=color, outline=color,
                                             tag=course_id)
            self.canvas.create_text(x + Strings.OFFSET_X, y + Strings.OFFSET_Y,
                                    text=course_id, fill='white', font=Strings.FONT_COURSE)
            self.canvas.tag_bind(self.courses.allcourses[course_id], '<ButtonPress-1>', self.on_call)
        else:
            self.canvas.create_rectangle(x, y, width, height, fill=color, outline=color)

    def on_call(self, event=None):
        if self.canvas.find_withtag(tk.CURRENT):
            item = self.canvas.gettags(tk.CURRENT)
            course_id = ' '.join(item[:2])

            # show a new window of the information about the course
            ShowInfo(self.tk_frame, course_id, self._connector)
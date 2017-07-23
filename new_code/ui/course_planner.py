import threading
import tkinter as tk
from tkinter import messagebox
from new_code import Strings
from new_code.ui.info_course import ShowInfo
from new_code.ui.abstract_act import AbstractActivity
from new_code.ui.singletons import AllCourses
from new_code.ui.singletons import Canvas
from new_code.ui.course_paint import CoursePaint
from random import randint


class CoursePlanner(AbstractActivity):
    def __init__(self, tk_frame=None, connector=None):
        super().__init__(tk_frame)

        self.tk_frame = tk_frame
        self.instruction_frame = tk.Frame(self.tk_frame)
        self.function_frame = tk.Frame(self.tk_frame, height=100)
        self.interactive_frame = tk.Frame(self.tk_frame)
        self.canvas = Canvas.Instance()
        self.canvas.canvas = tk.Canvas(self.interactive_frame, width=1200, height=1000)
        self.paintcanvas = self.canvas.canvas
        self.enter_etr = None
        self.update_btn = None
        self._connector = connector
        self.courses = AllCourses.Instance()
        self.counter = 0
        self.row = 0

    def instruction_frame_(self):
        self.instruction_frame.pack(fill=tk.BOTh, expand=True)

    def function_frame_(self):
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.function_frame, text='New Course: ').grid(row=0, column=2, padx=20, pady=20)
        self.enter_etr = tk.Entry(self.function_frame)
        self.update_btn = tk.Button(self.function_frame, text='Update', command=self.update)
        self.update_btn.bind('<Return>', self.update)
        self.enter_etr.grid(row=0, column=3, padx=20, pady=20)
        self.update_btn.grid(row=0, column=1, padx=20, pady=20)

    def interactive_frame_(self):
        self.interactive_frame.pack(fill=tk.BOTH)
        self.paintcanvas.grid(row=1, column=0, pady=20, padx=20, sticky=tk.NSEW)

    def update(self, event=None, course_id=None):
        if not self.enter_etr.get():
            messagebox.showerror("Error: ", "No information is entered")
            return
        if not self.check_connection():
            messagebox.showerror("Connection Error", "The courses have been parsed")
            return
        if course_id is None:
            course_id = self.enter_etr.get().upper()
        if not self._connector.find_course(course_id):
            messagebox.showerror("Course not found Error", "{} is not found!".format(course_id))
        self.counter += 1
        if self.counter % 9 == 0:
            self.counter = 1
            self.row += 1

        x1 = Strings.INIT_X + Strings.PADDING_X * (self.counter - 1)
        y1 = Strings.INIT_Y + Strings.PADDING_Y * self.row
        x2 = x1 + Strings.REC_LEN
        y2 = y1 + Strings.REC_HEI
        self.make_rectangle(x1, y1, x2, y2, Strings.LIGHT_COLOR_CODES[randint(0, 4)], course_id )

    def make_rectangle(self, x, y, width, height, color, course_id=None):
        course_paint = CoursePaint(x, y, width=width, height=height, color=color, outline=color, id=course_id)
        if course_id:
            self.courses.allcourses[course_id] = course_paint
            ui_id = self.paintcanvas.create_rectangle(course_paint.x, course_paint.y,
                                                 course_paint.width, course_paint.height,
                                                 fill=course_paint.color, outline=course_paint.color,
                                                 tag=course_id)
            self.courses.allcourses[course_id].ui_id = ui_id
            self.paintcanvas.create_text(course_paint.x + Strings.OFFSET_X, course_paint.y + Strings.OFFSET_Y,
                                    text=course_id, fill='white', font=Strings.FONT_COURSE)
            self.paintcanvas.tag_bind(self.courses.allcourses[course_id].ui_id, '<ButtonPress-1>', self.on_call)
        else:
            self.paintcanvas.create_rectangle(course_paint.x, course_paint.y, course_paint.width,
                                         course_paint.height, fill=course_paint.color, outline=
                                         course_paint.color)

    def on_call(self, event=None):
        if self.paintcanvas.find_withtag(tk.CURRENT):
            item = self.paintcanvas.gettags(tk.CURRENT)
            course_id = ' '.join(item[:2])

            # show a new window of the information about the course
            ShowInfo(self.tk_frame, course_id, self._connector)
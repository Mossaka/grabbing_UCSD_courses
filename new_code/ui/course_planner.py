import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from new_code import Strings
from new_code.connecting import Connector
from new_code.ui.info_course import ShowInfo


class CoursePlanner:
    def __init__(self, tk_frame=None, connector=None):
        self.tk_frame = tk_frame
        self.canvas = None
        self.interactive_frame = None
        self._connector = connector
        self._is_show = False
        self.courses = {}
        self.counter = 0
        self.row = 0

    def create_widgets(self):
        self.interactive_frame_()
        self.canvas_frame_()
        self._is_show = True

    def interactive_frame_(self):
        self.interactive_frame = tk.Frame(self.tk_frame, height=100)
        self.interactive_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.interactive_frame, text='New Course: ').grid(row=0, column=2, padx=20, pady=20)
        self.enter_etr = tk.Entry(self.interactive_frame)
        self.update_btn = tk.Button(self.interactive_frame, text='Update', command=self.update)
        self.update_btn.bind('<Return>', self.update)
        self.enter_etr.grid(row=0, column=3, padx=20, pady=20)
        self.update_btn.grid(row=0, column=1, padx=20, pady=20)

    def canvas_frame_(self):
        self.canvas_frame = tk.Frame(self.tk_frame)
        self.canvas_frame.pack(fill=tk.BOTH)
        self.canvas = tk.Canvas(self.canvas_frame, width=1200, height=1000)
        self.canvas.grid(row=1, column=0, pady=20, padx=20, sticky=tk.NSEW)

    def update(self, event=None):
        if not self.enter_etr.get():
            messagebox.showerror("Error: ", "No information is entered")

        course_id = self.enter_etr.get().upper()

        self.counter += 1
        if self.counter % 9 == 0:
            self.counter = 1
            self.row += 1

        def get_x():
            return 10 + Strings.PADDING_X * (self.counter - 1)

        def get_y():
            return 10 + Strings.PADDING_Y * self.row

        def get_x2():
            return get_x() + Strings.REC_LEN

        def get_y2():
            return get_y() + Strings.REC_HEI
        x1 = get_x()
        y1 = get_y()
        x2 = get_x2()
        y2 = get_y2()
        self.make_rectangle(x1, y1, x2, y2, Strings.LIGHT_COLOR_CODES['blue'], course_id )

    def make_rectangle(self, x, y, width, height, color, course_id=None):
        if course_id:
            self.courses[course_id] =\
                self.canvas.create_rectangle(x, y, width, height, fill=color, outline=color)
            self.canvas.create_text(x + Strings.OFFSET_X, y + Strings.OFFSET_Y,
                                    text=course_id, fill='white', font=Strings.FONT_COURSE )
            self.canvas.tag_bind(self.courses[course_id], '<ButtonPress-1>', self.onRecCall )
        else:
            self.canvas.create_rectangle(x, y, width, height, fill=color, outline=color)


    def destroy(self):
        self.interactive_frame.pack_forget()
        self._is_show = False

    def onRecCall(self, event=None, course_id=None):
        print('Got object click', event.x, event.y)
        ShowInfo(self, course_id, self._connector)

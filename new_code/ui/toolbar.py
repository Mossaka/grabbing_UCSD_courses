import tkinter as tk
from new_code.ui.singletons import AllCourses
from new_code.ui.singletons import Canvas
from new_code.ui.singletons import CoursePlannerSingleton
from pprint import pprint
from new_code.ui.course_paint import CoursePaint
from new_code import Strings
import csv

class ToolBar(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.menubar = tk.Menu(master)
        self.create_menu()
        master.master.config(menu=self.menubar)

    def create_menu(self):
        file_menu_text = "File/Open/Save/|/Exit"
        edit_menu_text = "Edit/Forward/Back/Copy/Paste"
        help_menu_text = "Help/About"
        self.execute_menu(file_menu_text)
        self.execute_menu(edit_menu_text)
        self.execute_menu(help_menu_text)

    def execute_menu(self, menu_text):
        menu = tk.Menu(self.menubar, tearoff=0)
        menu_cmd = menu_text.split('/')
        cascade_name = menu_cmd.pop(0)
        for menu_name in menu_cmd:
            if menu_name is '|':
                menu.add_separator()
            else:
                menu.add_command(label=menu_name,
                                 command=getattr(eval(cascade_name)(),  # class name
                                                 "_" + menu_name.lower()))  # method name
        self.menubar.add_cascade(label=cascade_name, menu=menu)


class File:
    def _open(self):
        course_planner= CoursePlannerSingleton()
        course_planner.update('math 140a')
        """
        allcourses = AllCourses.Instance()
        canvas = Canvas.Instance()
        canvaspaint = canvas.canvas
        with open('Planner.csv', 'r') as to_open:
            to_open_reader = csv.reader(to_open)
            for row in to_open_reader:
                if len(row) > 0:
                    course_paint = CoursePaint(row[1], row[2], width=row[3], height=row[4],
                                               color=row[5], outline=row[5], id=row[6])
                    allcourses.allcourses[course_paint.id] = course_paint

        for course_id, course_paint in allcourses.allcourses.items():
            canvaspaint.create_rectangle(course_paint.x, course_paint.y,
                                                 course_paint.width, course_paint.height,
                                                 fill=course_paint.color, outline=course_paint.color,
                                                 tag=course_id)
            canvaspaint.create_text(float(course_paint.x) + Strings.OFFSET_X, float(course_paint.y) + Strings.OFFSET_Y,
                               text=course_id, fill='white', font=Strings.FONT_COURSE)
        """

    def _save(self):
        allcourses = AllCourses.Instance()
        with open('Planner.csv', 'w') as to_save:
            to_save_writter = csv.writer(to_save, delimiter=',')
            for key, value in allcourses.allcourses.items():
                to_save_writter.writerow(key)

    def _exit(self):
        print("this is exit!")


class Edit:
    def _forward(self):
        print("this is forward")

    def _back(self):
        print("this is back")

    def _copy(self):
        print("this is copy")

    def _paste(self):
        print("this is paste")


class Help:
    def _about(self):
        print("this is about")
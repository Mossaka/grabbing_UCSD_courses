import tkinter as tk
from new_code.ui.canvas_rect import AllCourses
from pprint import pprint

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
        print("this is open!")

    def _save(self):
        allcourses = AllCourses.Instance()
        pprint(allcourses.allcourses)

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
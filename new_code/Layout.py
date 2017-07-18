import tkinter as tk
from tkinter import ttk

from new_code.connecting import *

_fields = ("Description", "Prerequisites", "Postrequisites")
class main_page(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self._connector = Connector()

    def create_widgets(self):
        self.pack(fill=tk.BOTH, expand=True)

        _enter_frame = tk.Frame(self)
        _enter_frame.pack(fill=tk.BOTH, expand=True)
        
        self.grab_course_btn = tk.Button(_enter_frame, text="Get Courses", command=self._parse_course)
        self.grab_course_btn.grid(row=0, column=4, columnspan=2)

        self.switch = ttk.Combobox(_enter_frame,
                                   values=('treeview table', 'visualized courses'))
        self.switch.bind("<<ComboboxSelected>>", func=self.switch_func)
        self.switch.current(0)
        self.switch.grid(row=0, column=6, columnspan=2)

        _enter_frame.columnconfigure(0, weight=4)
        _enter_frame.columnconfigure(4, weight=1)
        _enter_frame.columnconfigure(6, weight=1)
        _enter_frame.columnconfigure(8, weight=4)

        _search_frame = tk.Frame(self, height=100, bd=2)
        _search_frame.pack(fill=tk.BOTH, expand=True)

        self.search_entry = tk.Entry(_search_frame, width=50)
        self.search_entry.grid(row=1, column=2, columnspan=10, sticky=tk.EW)

        self.search_btn = tk.Button(_search_frame, text='Search', command=self._search)
        self.search_btn.grid(row=1, column=12, sticky=tk.EW)
        _search_frame.columnconfigure(0, weight=5)
        _search_frame.rowconfigure(1, weight=5)
        _search_frame.rowconfigure(3,weight=10)
        _search_frame.columnconfigure(13,weight=5)

        _interactive_frame = tk.Frame(self, height=100)
        _interactive_frame.pack(fill=tk.BOTH, expand=True)
        self.treeview = ttk.Treeview(_interactive_frame, columns=_fields, selectmode="extended")
        self.treeview.grid(row=0, column=1, sticky=tk.NSEW)

        _interactive_frame.columnconfigure(0, weight=1)
        _interactive_frame.columnconfigure(1, weight=8)
        _interactive_frame.columnconfigure(2, weight=1)
        _interactive_frame.rowconfigure(0, weight=10)

        self.treeview.heading('#0', text='Course ID', anchor = tk.CENTER)
        self.treeview.heading('#1', text='Description', anchor = tk.CENTER)
        self.treeview.heading('#2', text='Pre-requisites', anchor = tk.CENTER)
        self.treeview.heading('#3', text='Sequence Courses', anchor = tk.CENTER)

        self.treeview.column("#0", stretch=tk.YES, minwidth=10, width=20)

        self.canvas = tk.Canvas(_interactive_frame, width=800, height=400)
        self.canvas.grid(row=0, column=1, sticky=tk.NSEW)
        self.canvas.grid_forget()
        self.canvas.create_oval(100,100,400,400, fill='blue')


    def _parse_course(self):
        """runs the main program"""
        self._connector.parse_all_majors()
        print("---start parsing courses from websites---")
        for ab, link in self._connector.major_links.items():
            self._connector.parse_courses(link)
        print("Parsing success!")
        print("---start parsing prerequisites and postrequisites---")

        self._connector.parse_prerequisites()
        self._connector.parse_postrequsites()
        print("Parsing success!")

    def switch_func(self, event):
        if self.switch.get() == 'treeview table':
            self.canvas.grid_forget()
            self.treeview.grid(row=0, column=1, sticky=tk.NSEW)
        else:
            self.treeview.grid_forget()
            self.canvas.grid(row=0, column=1, sticky=tk.NSEW)

    def _search(self):
        search_text = self.search_entry.get().upper()

        #whole match
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
            self.treeview.insert('', 'end', text=search_text, values=values)

def main():
    root = tk.Tk()
    root.geometry("1200x800+30+30")
    root.title("UCSD Course Helper")
    menu = tk.Menu(root)
    app = main_page(root)
    app.mainloop()

if __name__ == '__main__':
    main()
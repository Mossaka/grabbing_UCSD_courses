import tkinter as tk


class ShowInfo:
    def __init__(self, upper, course_ID, connector):
        self.info_level = tk.Toplevel(upper)
        self.info_level.title("More Info about {}".format(course_ID))
        self.info_level.geometry()
        self.info_level.resizable(0, 0)
        self.info_level.bind('<Escape>', lambda event: self.info_level.destroy())
        self.info_level.focus()
        self.connector = connector
        self.course_ID = course_ID
        self.course = self.connector.get_course(self.course_ID)
        self.info_frame = tk.Frame(self.info_level)
        self.create_widgets()

    def create_widgets(self):
        self.info_frame.pack()

        name_label = tk.Label(self.info_frame, text='Name: {}'.format(self.course_ID) )
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NE)
        description_label = tk.Label(self.info_frame, text='Description: {}'.format(self.course.get_description()))
        description_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NE)
from new_code.ui_main.mainapp import *


class MainProgram:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(Strings.GEOMETRY)
        self.root.title(Strings.PROGRAM_TITLE)
        self.main_loop()

    def main_loop(self):
        app = MainApp(self.root)
        app.pack(side="top", fill="both", expand=True)
        app.mainloop()

if __name__ == '__main__':
    MainProgram()

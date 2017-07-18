from new_code import Strings
from new_code.ui.main_page import *


class MainProgram:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(Strings.GEOMETRY)
        self.root.title(Strings.PROGRAM_TITLE)
        self.main_loop()

    def main_loop(self):
        menu = tk.Menu(self.root)
        app = MainPage(self.root)
        app.mainloop()

if __name__ == '__main__':
    MainProgram()

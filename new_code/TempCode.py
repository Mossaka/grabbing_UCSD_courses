from tkinter import *
root = Tk()
Button(root, text='A').pack(side=LEFT, expand=YES, fill=Y)
Button(root, text='B').pack(side=TOP, expand=YES, fill=BOTH)
Button(root, text='C').pack(side=RIGHT, expand=YES, fill=NONE, anchor=NE)
Button(root, text='D').pack(side=LEFT, expand=NO, fill=Y)
root.mainloop()
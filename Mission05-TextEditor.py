from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *

import os

window = Tk()
window.geometry("500x300")
window.title("My Text Editor v0.01")
window.resizable(width=TRUE, height=TRUE)
textPad = Text(window, width=100, height=80)

def selectFile():
    filename = askopenfilename(parent=window, filetypes=(("Text File", "*.txt;*.raw"), ("All File", "*.*")))
    window.title(os.path.split(filename)[1])
    with open(filename, "r") as f:
        text = f.read()
    textPad.insert("1.0", text, "a")

def saveFile():
    saveTxt = asksaveasfile(parent=window, mode="w", defaultextension=".txt",
                            filetypes=(("Text File", "*.txt;*.raw"), ("All File", "*.*")))
    saveTxt.write(textPad.get(1.0, END)) # 1.0 -> (1, 0)
    saveTxt.close()

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command=selectFile)
fileMenu.add_command(label="Save", command=saveFile)

textPad.pack()
window.mainloop()
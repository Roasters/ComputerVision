from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *

import os

window = Tk()
window.title('GIF 사진 뷰어 Beta (Ver 0.01)')
window.geometry("500x300")
window.resizable(width=FALSE, height=TRUE)

fnameList = []
folder = askdirectory(parent=window)
for dirName, subDirList, fnames in os.walk(folder):
    for fname in fnames:
        if os.path.splitext(fname)[1].upper() == ".GIF":
            fnameList.append(os.path.join(dirName, fname))

## 전역변수 선언부 ##
num = 0 # 현재 사진 순번
## 함수 선언부
def clickPrev() :
    global num
    num -= 1
    if num < 0:
        num = len(fnameList) - 1
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo=photo

def clickNext() :
    global num
    num += 1
    if num >= len(fnameList) :
        num = 0
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo=photo

def clickHome():
    global num
    num = 0
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo=photo

def clickEnd():
    global num
    num = len(fnameList) - 1
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo=photo

def keyPress(key):
    global num
    if key.keycode == 36:
        num = 0
    if key.keycode == 35:
        num = len(fnameList) - 1
    if key.keycode == 37:
        num -= 1
        if num < 0:
            num = len(fnameList) - 1
    if key.keycode == 39:
        num += 1
        if num >= len(fnameList):
            num = 0
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo=photo

def jumpTo(count=0):
    if count == 0:
        count = askinteger("건너뛸 수", "숫자-->")
    for _ in range(count):
        clickNext()

def selectFile():
    filename = askopenfilename(parent=window, filetypes=(("GIF File", "*.gif;*.raw"),("All File", "*.*")))
    photo = PhotoImage(file = filename)
    pLabel.configure(image=photo)
    pLabel.image= photo

photo = PhotoImage(file = fnameList[num])
pLabel = Label(window, image=photo)

mainMenu = Menu(window)
window.config(menu=mainMenu)

moveMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Move", menu=moveMenu)
moveMenu.add_command(label="Prev", command=clickPrev)
moveMenu.add_separator()
moveMenu.add_command(label="Next", command=clickNext)

jumpMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Jump", menu=jumpMenu)
jumpMenu.add_command(label="1", command=lambda: jumpTo(1))
jumpMenu.add_command(label="3", command=lambda: jumpTo(3))
jumpMenu.add_command(label="5", command=lambda: jumpTo(5))
jumpMenu.add_command(label="Enter Num", command=jumpTo)
jumpMenu.add_separator()
jumpMenu.add_command(label="Select File", command=selectFile)


btnPrev = Button(window, text='<< 이전 그림', command=clickPrev)
btnNext = Button(window, text='다음 그림>>', command=clickNext)
btnHome = Button(window, text='처음 그림', command=clickHome)
btnEnd = Button(window, text='마지막 그림', command=clickEnd)

window.bind("<Key>", keyPress)

btnHome.place(x=70, y=10); btnPrev.place(x=150, y=10); btnNext.place(x=250, y=10); btnEnd.place(x=350, y=10)
pLabel.place(x=50, y=50)
window.mainloop()

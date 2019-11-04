from tkinter import *
from tkinter.colorchooser import *
from tkinter.simpledialog import *

def mouseClick(event):
    global x1, y1, x2, y2
    x1 = event.x
    y1 = event.y

def mouseDropCircle(event):
    global x1, y1, x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_oval(x1, y1, x2, y2, width=penWidth, fill=penColor)

def mouseDropLine(event):
    global x1, y1, x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)

def getColor():
    global penColor
    color = askcolor()
    penColor = color[1]

def getWidth():
    global penWidth
    penWidth = askinteger("Line Thickness", "Enter the line thickness (1~10)", minvalue=1, maxvalue=10)

def createCircle():
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDropCircle)
    canvas.pack()

def createLine():
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDropLine)
    canvas.pack()


x1, y1, x2, y2 = None, None, None, None
penColor = "black"
penWidth = 5

window = Tk()
window.title("My Paint")
canvas = Canvas(window, height=300, width=300)

mainMenu = Menu(window)
window.config(menu=mainMenu)
fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Adjust", menu=fileMenu)
fileMenu.add_command(label="Adjust Color", command=getColor)
fileMenu.add_command(label="Adjust Thickness", command=getWidth)

figureMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Figure", menu=figureMenu)
figureMenu.add_command(label="Add Circle", command=createCircle)
figureMenu.add_command(label="Add Line", command=createLine)

window.mainloop()
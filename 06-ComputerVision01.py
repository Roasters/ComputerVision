from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

import math
import os

# ============= Functions ===========================================================

# Allocate memory and return list
def malloc(h, w):
    retMemory = [[0 for _ in range(w)] for _ in range(h)]
    return retMemory

def loadImage(fname):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    fsize = os.path.getsize(fname)  # File size (byte)
    inH = inW = int(math.sqrt(fsize))

    # Prepare empty memory for input image
    inImage = malloc(inH, inW)

    # File --> Memory
    with open(fname, "rb") as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))

# Select a file and load it into memory
def openImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window, filetypes=(("RAW File", "*.raw"), ("All File", "*.*")))
    loadImage(filename)
    equalImage()

def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    pass

def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    if canvas != None: # If executed before
        canvas.destroy()

    window.geometry("{}x{}".format(outH, outW))      # Empty wall
    canvas = Canvas(window, height=outH, width=outW) # Empty board
    paper = PhotoImage(height=outH, width=outW)      # Empty paper
    canvas.create_image((outH//2, outW//2), image=paper, state="normal") # First arg: the middle point

    # Display by painting dot by dot
    for i in range(outH):
        for k in range(outW):
            r = g = b = outImage[i][k]
            paper.put("#%02x%02x%02x"%(r, g, b), (k, i)) # if (i, k), the image gets turned
    canvas.pack(expand=1, anchor=CENTER)

# ============= Functions for Computer Vision(Image Processing) Algorithm ===========

def equalImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]

    displayImage()

# ============= Global Variables ====================================================

inImage, outImage = [], []
inW, inH, outW, outH = [0] * 4
window, canvas, paper =[None] * 3
filename = ""

# =============  Main Code ==========================================================

if __name__ == '__main__':
    window = Tk()
    window.title('Computer Vision (DeepLearning) v0.01')
    window.geometry("500x500")

    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Open", command=openImage)
    fileMenu.add_separator()
    fileMenu.add_command(label="Save", command=saveImage)

    comVisionMenu1 = Menu(mainMenu)
    mainMenu.add_cascade(label="Algorithm A", menu=comVisionMenu1)
    comVisionMenu1.add_command(label="Algorithm 1", command=None)
    comVisionMenu1.add_command(label="Algorithm 2", command=None)

    window.mainloop()
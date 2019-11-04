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

def addImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    value = askinteger("Brightening", "Enter the value", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            tmp = inImage[i][k] + value
            outImage[i][k] = 255 if tmp > 255 else tmp

    displayImage()

def subImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    value = askinteger("Brightening", "Enter the value", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            tmp = inImage[i][k] - value
            outImage[i][k] = 0 if tmp < 0 else tmp

    displayImage()

def mulImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    value = askinteger("Brightening", "Enter the value", minvalue=2, maxvalue=10)
    for i in range(inH):
        for k in range(inW):
            tmp = inImage[i][k] * value
            outImage[i][k] = 255 if tmp > 255 else tmp

    displayImage()

def divImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    value = askinteger("Brightening", "Enter the value", minvalue=2, maxvalue=10)
    for i in range(inH):
        for k in range(inW):
            tmp = inImage[i][k] // value
            outImage[i][k] = tmp

    displayImage()

def conImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 - inImage[i][k]

    displayImage()

def binImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    mean = int(sum(k for i in inImage for k in i) / (inH * inW))
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 if inImage[i][k] > mean else 0

    displayImage()

def meanImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    # Main Code
    inMean = 0
    outMean = 0
    for i in range(inH):
        for k in range(inW):
            inMean += inImage[i][k]
            outMean += outImage[i][k]
    inMean /= inW * inH
    outMean /= outW * outH

    messagebox.showinfo("Pixel Mean", "Input Image: {:.1f}\nOutput Image: {:.1f}".format(inMean, outMean))

def posterImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    for i in range(inH):
        for k in range(inW):
            pixel = inImage[i][k]
            if pixel > 200:
                outImage[i][k] = 225
            elif pixel > 150:
                outImage[i][k] = 175
            elif pixel > 100:
                outImage[i][k] = 125
            elif pixel > 50:
                outImage[i][k] = 75
            else:
                outImage[i][k] = 25

    displayImage()

def stretchImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    low = min(k for i in inImage for k in i)
    high = max(k for i in inImage for k in i)
    for i in range(inH):
        for k in range(inW):
            tmp = 0 if (inImage[i][k] - low < 0) else (inImage[i][k] - low)
            outImage[i][k] = int(( tmp / (high - low)) * 255)

    displayImage()

def gammaImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    gamma = askfloat("Gamma Adjust", "Enter the value", minvalue=0.1, maxvalue=10)
    for i in range(inH):
        for k in range(inW):
            tmp = int(inImage[i][k] * (1.0 / gamma))
            outImage[i][k] = 255 if tmp > 255 else tmp

    displayImage()

def updownImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    for i in range(inH):
        for k in range(inW):
            outImage[inH-i-1][k] = inImage[i][k]

    displayImage()

# def paraImage():
#     global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
#     # Attention: display size required!!
#     outH = inH; outW = inW
#
#     # Memory Allocation
#     outImage = malloc(outH, outW)
#
#     # Main Code
#     for i in range(inH):
#         for k in range(inW):
#             # outImage[i][k] = int(255 - 255 * (inImage[i][k] / 128 - 1)**2) # Cap
#             outImage[i][k] = int(255 * (inImage[i][k] / 128 - 1) ** 2) # Cup
#     displayImage()

def paraImage(): # with look-up table
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    LUT = [0 for _ in range(256)]
    for i in range(256):
        LUT[i] = int(255 * i / 128 - 1) ** 2)
    for i in range(inH):
        for k in range(inW):
            # outImage[i][k] = int(255 - 255 * (inImage[i][k] / 128 - 1)**2) # Cap
            outImage[i][k] = LUT[image[i][k]]
    displayImage()

# ============= Global Variables ====================================================

inImage, outImage = [], []
inW, inH, outW, outH = [0] * 4
window, canvas, paper =[None] * 3
filename = ""

# =============  Main Code ==========================================================

if __name__ == '__main__':
    window = Tk()
    window.title('Computer Vision (DeepLearning) v0.02')
    window.geometry("500x500")

    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Open", command=openImage)
    fileMenu.add_separator()
    fileMenu.add_command(label="Save", command=saveImage)

    comVisionMenu1 = Menu(mainMenu)
    mainMenu.add_cascade(label="Pixel", menu=comVisionMenu1)
    comVisionMenu1.add_command(label="Brighten", command=addImage)
    comVisionMenu1.add_command(label="Darken", command=subImage)
    comVisionMenu1.add_command(label="Brighten(scale)", command=mulImage)
    comVisionMenu1.add_command(label="Darken(scale)", command=divImage)
    comVisionMenu1.add_command(label="Contrast", command=conImage)
    comVisionMenu1.add_command(label="Black&White", command=binImage)
    comVisionMenu1.add_command(label="Average", command=meanImage)
    comVisionMenu1.add_command(label="Posterize", command=posterImage)
    comVisionMenu1.add_command(label="Stretch", command=stretchImage)
    comVisionMenu1.add_command(label="Gamma", command=gammaImage)
    comVisionMenu1.add_command(label="Parabola", command=paraImage)

    geoMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="Geometry", menu=geoMenu)
    geoMenu.add_command(label="UpsideDown", command=updownImage)
    geoMenu.add_command(label="Save", command=saveImage)

    window.mainloop()
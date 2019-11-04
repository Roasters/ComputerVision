from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

import math
import os
import tempfile  # Get the temporary folder directory
import datetime
import matplotlib.pyplot as plt

import struct
import pymysql
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import PIL

# In[2]:

R, G, B = 0, 1, 2
inImage, outImage = [], []  # 3-dimensional list
inW, inH, outW, outH = [0] * 4
window, canvas, paper = [None] * 3
filename = ""
VIEW_X, VIEW_Y = 512, 512 # Actual display size

# In[3]:


# Allocate memory and return list
def malloc(h, w, initValue=0):  # Leave malloc as it is for assigning 2d list
    retMemory = [[initValue for _ in range(w)] for _ in range(h)]
    return retMemory

def loadImageColor(fname):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    inImage = []   # Initialize

    photo = Image.open(fname) # PIL Object (for metadata)
    inH = photo.height
    inW = photo.width
    for _ in range(3):
        inImage.append(malloc(inH, inW))

    photoRGB = photo.convert("RGB")
    for i in range(inH):
        for k in range(inW):
            r, g, b = photoRGB.getpixel((k, i))
            inImage[R][i][k] = r
            inImage[G][i][k] = g
            inImage[B][i][k] = b

# Select a file and load it into memory
def openImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window, filetypes=(("Color File", "*.jpg;*.png;*.bmp;*.tif"), ("All File", "*.*")))
    if filename == '' or filename == None:
        return

    loadImageColor(filename)
    equalImageColor()

    displayImageColor()


def saveImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension="*.jpg",
                           filetypes=(("JPG File", "*.jpg"), ("All file", "*.*")))
    if outImage == None:
        return
    if saveFp == '' or saveFp == None:
        return
    outImage.save(saveFp.name)
    print("Saved")


def displayImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    VIEW_X = outW
    VIEW_Y = outH
    step = 1

    if canvas != None:  # If executed before
        canvas.destroy()

    window.geometry("{}x{}".format(str(int(VIEW_Y*1.2)), str(int(VIEW_X*1.2))))  # Empty wall
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)  # Empty board
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)  # Empty paper
    import numpy as np

    rgbStr = ""  # Assign the string of the whole pixels
    for i in np.arange(0, outH, step):
        tmpStr = ""
        for k in np.arange(0, outW, step):
            i = int(i); k = int(k)
            r , g , b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += " #%02x%02x%02x" % (r, g, b)  # Need a space to separate each string
        rgbStr += "{" + tmpStr + "} "  # Same here
    paper.put(rgbStr)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state="normal")  # First arg: the middle point

    canvas.pack(expand=1, anchor=CENTER)

    status.configure(text="Image Info: " + str(outH) + "x" + str(outW))

# In[4]:

def equalImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = inImage[RGB][i][k]

    displayImageColor()

def addImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    value = askinteger("Brightness", "Negative : Darken\nPositive : Brighten", minvalue=-255, maxvalue=255)
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] + value > 255:
                    outImage[RGB][i][k] = 255
                elif inImage[RGB][i][k] + value < 0:
                    outImage[RGB][i][k] = 0
                else:
                    outImage[RGB][i][k] = inImage[RGB][i][k] + value

    displayImageColor()

def revImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = 255 - inImage[RGB][i][k]

    displayImageColor()

def paraImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    LUT = [0 for _ in range(256)]
    for i in range(256):
        LUT[i] = int(255 - (255 * i / 128 - 1) ** 2) ############################### Needs fixing

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = LUT[inImage[RGB][i][k]]

    displayImageColor()

def morphImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    filename2 = askopenfilename(parent=window, filetypes=(("Color File", "*.jpg;*.png;*.bmp;*.tif"), ("All File", "*.*")))
    if filename2 == '' or filename2 == None:
        return

    # Prepare empty memory for input image

    photo = Image.open(filename2)  # PIL Object (for metadata)
    inH2 = photo.height
    inW2 = photo.width
    inImage2 = []
    for _ in range(3):
        inImage2.append(malloc(inH2, inW2))

    photoRGB = photo.convert("RGB")
    for i in range(inH):
        for k in range(inW):
            r, g, b = photoRGB.getpixel((k, i))
            inImage2[R][i][k] = r
            inImage2[G][i][k] = g
            inImage2[B][i][k] = b

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # Main Code
    w1 = askinteger("Original Image Weight", "Enter the Weight (%)", minvalue=0, maxvalue=100)
    w1 /= 100
    w2 = 1 - w1
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                newVal = int(inImage[RGB][i][k] * w1 + inImage2[RGB][i][k] * w2)
                if newVal > 255:
                    newVal = 255
                elif newVal < 0:
                    newVal = 0
                outImage[RGB][i][k] = newVal
    displayImageColor()

# ========= Functions for Statistical Operations

def bwImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = []
    # Main Code

    sum = 0
    tmpImage = malloc(outH, outW)
    for i in range(inH):
        for k in range(inW):
            tmpImage[i][k] = int((inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]) / 3 )
            sum += inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]
    outImage = [tmpImage, tmpImage, tmpImage]

    mean = int(sum / (3 * inH * inW))

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = 255 if outImage[RGB][i][k] > mean else 0

    displayImageColor()

def histoImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    inCountList = [[0 for _ in range(256)] for _ in range(3)]

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                inCountList[RGB][inImage[RGB][i][k]] += 1

    fig = plt.figure()
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 2)
    ax3 = fig.add_subplot(3, 1, 3)

    ax1.plot(inCountList[0], 'r')
    ax2.plot(inCountList[1], 'g')
    ax3.plot(inCountList[2], 'b')

    plt.show()

def stretchImageColor():  # Equalization
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # Main Code
    inCountList = [[0 for _ in range(256)] for _ in range(3)]
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                inCountList[RGB][inImage[RGB][i][k]] += 1

    cumCount = [[0 for _ in range(256)] for _ in range(3)]

    for RGB in range(3):
        cumCount[RGB][0] = inCountList[RGB][0]

    for RGB in range(3):
        for i in range(1, 256):
            cumCount[RGB][i] += cumCount[RGB][i - 1] + inCountList[RGB][i]

    normalCount = [[0 for _ in range(256)] for _ in range(3)]
    for RGB in range(3):
        for i in range(256):
            normalCount[RGB][i] = int(cumCount[RGB][i] * (1 / (inH * inW)) * 255)
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] = normalCount[RGB][inImage[RGB][i][k]]

    displayImageColor()


def upDownImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # Main Code
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][inH - i - 1][k] = inImage[RGB][i][k]

    displayImageColor()

def zoomoutImageColor():

    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom Out", "Enter the value", minvalue=2, maxvalue=16)
    outH = inH // scale
    outW = inW // scale

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # For better performance
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] = inImage[RGB][i * scale][k * scale]

    displayImageColor()

def zoominImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom In", "Enter the value", minvalue=2, maxvalue=4)
    outH = inH * scale
    outW = inW * scale

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # Backwarding
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] = inImage[RGB][i // scale][k // scale]

    displayImageColor()

def zoominImageColor2():  # Bilinear Interpolation
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom In", "Enter the value", minvalue=2, maxvalue=4)
    outH = inH * scale
    outW = inW * scale

    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    rH, rW, iH, iW = [0] * 4  # Real Position, Integer Position
    x, y = 0, 0  # Difference between real val and integer val
    C1, C2, C3, C4 = [0] * 4  # Base pixels for the target position(N)
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                rH = i / scale;
                rW = k / scale
                iH = int(rH);
                iW = int(rW)
                x = rW - iW;
                y = rH - iH
                if 0 <= iH < (inH - 1) and 0 <= iW < (inW - 1):
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW + 1]
                    C3 = inImage[RGB][iH + 1][iW + 1]
                    C4 = inImage[RGB][iH + 1][iW]
                    newValue = C1 * (1 - y) * (1 - x) + C2 * (1 - y) * x + C3 * y * x + C4 * y * (1 - x)
                    outImage[RGB][i][k] = int(newValue)

    displayImageColor()


def emboImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    # Main Code
    MSize = 3
    mask = [[-1, 0, 0],
            [0, 0, 0],
            [0, 0, 1]]

    # Allocate empty memory for temp input image
    tmpInImage = []
    for _ in range(3):
        tmpInImage.append(malloc(inH + (MSize - 1), inW + (MSize - 1), 128))
    tmpOutImage = []
    for _ in range(3):
        tmpOutImage.append(malloc(outH, outW))
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[RGB][i + (MSize // 2)][k + (MSize // 2)] = inImage[RGB][i][k]

    # Mask Operation
    for RGB in range(3):
        for i in range(MSize // 2, inH + MSize // 2):
            for k in range(MSize // 2, inW + MSize // 2):
                # Deal with each pixel
                S = 0.0
                for m in range(MSize):
                    for n in range(MSize):
                        S += mask[m][n] * tmpInImage[RGB][i + m - MSize // 2][k + n - MSize // 2]
                tmpOutImage[RGB][i - MSize // 2][k - MSize // 2] = int(S)
    # Add 128
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                tmpOutImage[RGB][i][k] += 128

    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                outImage[RGB][i][k] = value

    displayImageColor()
# In[10]:


window = Tk()
window.title('Computer Vision (Color) v0.01')
status = Label(window, text="Image Info: ", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
window.geometry("500x500")

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="Save", command=saveImageColor)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="Pixel", menu=comVisionMenu1)
comVisionMenu1.add_command(label="Brightness", command=addImageColor)
comVisionMenu1.add_command(label="Reverse", command=revImageColor)
comVisionMenu1.add_command(label="Parabola", command=paraImageColor)
comVisionMenu1.add_command(label="Morphing", command=morphImageColor)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="Stats", menu=comVisionMenu2)
comVisionMenu2.add_command(label="Black&White", command=bwImageColor)
comVisionMenu2.add_command(label="Histogram", command=histoImageColor)
comVisionMenu2.add_command(label="Stretch", command=stretchImageColor)


comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="Geometric", menu=comVisionMenu3)
comVisionMenu3.add_command(label="Upside Down", command=upDownImageColor)
comVisionMenu3.add_command(label="Zoom In", command=zoominImageColor)
comVisionMenu3.add_command(label="Zoom In(BiInterpolation)", command=zoominImageColor2)
comVisionMenu3.add_command(label="Zoom Out", command=zoomoutImageColor)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="Area", menu=comVisionMenu4)
comVisionMenu4.add_command(label="Embossing", command=emboImageColor)

window.mainloop()

# In[ ]:





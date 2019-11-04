from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

import math
import os


# ============= Functions ===========================================================

# Allocate memory and return list
def malloc(h, w, initValue=0):
    retMemory = [[initValue for _ in range(w)] for _ in range(h)]
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
    if filename == '' or filename == None:
        return
    loadImage(filename)
    equalImage()

import struct
def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    saveFp = asksaveasfile(parent=window, mode='rb', defaultextension="*.raw",
                           filetypes=(("RAW File", "*.raw"), ("All File", "*.*")))
    if saveFp == '' or saveFp == None :
        return
    for i in range(outH):
        for k in range(outW):
            saveFp.write(struct.pack("B", outImage[i][k]))
    saveFp.close()

def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    if canvas != None:  # If executed before
        canvas.destroy()

    window.geometry("{}x{}".format(outH, outW))  # Empty wall
    canvas = Canvas(window, height=outH, width=outW)  # Empty board
    paper = PhotoImage(height=outH, width=outW)  # Empty paper

    # For better performance
    rgbStr = "" # Assign the string of the whole pixels
    for i in range(outH):
        tmpStr = ""
        for k in range(outW):
            r = g = b = outImage[i][k]
            tmpStr += " #%02x%02x%02x" %(r, g, b)  # Need a space to separate each string
        rgbStr += "{" + tmpStr + "} " # Same here
    paper.put(rgbStr)
    canvas.create_image((outH // 2, outW // 2), image=paper, state="normal")  # First arg: the middle point

    # Mouse Event
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)

    canvas.pack(expand=1, anchor=CENTER)

# ============= Functions for Computer Vision(Image Processing) Algorithm ===========

def equalImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    low = min(k for i in inImage for k in i)
    high = max(k for i in inImage for k in i)
    for i in range(inH):
        for k in range(inW):
            # tmp = 0 if ( inImage[i][k] - low< 0) else (inImage[i][k] - low)
            outImage[i][k] = int(((inImage[i][k] - low)/ (high - low)) * 255)

    displayImage()

def stretchImage2(): # End-In
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    low = min(k for i in inImage for k in i)
    high = max(k for i in inImage for k in i)

    lowAdd = askinteger("End-In", "Addition to Low", minvalue=0, maxvalue=255)
    highSub = askinteger("End-In", "Subtraction from High", minvalue=0, maxvalue=255)

    low += lowAdd
    high -= highSub
    for i in range(inH):
        for k in range(inW):
            value = int(((inImage[i][k] - low)/ (high - low)) * 255)
            if value < 0 :
                value = 0
            elif value > 255:
                value = 255
            outImage[i][k] = value

    displayImage()


def stretchImage3(): # Equalization
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    inCountList = [0] * 256

    for i in range(inH):
        for k in range(inW):
            inCountList[inImage[i][k]] += 1

    cumCount = [0] * 256
    cumCount[0] = inCountList[0]
    for i in range(1, 256):
        cumCount[i] += cumCount[i-1] + inCountList[i]

    normalCount = [0] * 256
    for i in range(256):
        normalCount[i] = int(cumCount[i] * (1 / (inH * inW)) * 255)

    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = normalCount[inImage[i][k]]

    displayImage()

def gammaImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

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
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    for i in range(inH):
        for k in range(inW):
            outImage[inH - i - 1][k] = inImage[i][k]

    displayImage()


def rotateImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    angle = askinteger("Rotate", "Enter the degree", minvalue=1, maxvalue=360)
    radian = angle * math.pi / 180

    outW = inW
    outH = inH

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    cx = inW // 2; cy = inH//2
    for i in range(outH):
        for k in range(outW):
            xs = i ; ys = k
            xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
            yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
            if 0 <= xd < outW and 0 <= yd < outH:
                outImage[xs][ys] = inImage[xd][yd]

    displayImage()

def zoomOutImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom Out", "Enter the value", minvalue=2, maxvalue=16)
    outH = inH // scale
    outW = inW // scale

    # Memory Allocation
    outImage = malloc(outH, outW)

    # For better performance
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i * scale][k * scale]

    displayImage()

def zoomOutImage2():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom Out", "Enter the value", minvalue=2, maxvalue=16)
    outH = inH // scale
    outW = inW // scale

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    for i in range(0, inH):
        for k in range(0, inW):
            outImage[i//scale][k//scale] += inImage[i][k]
    for i in range(0, outH):
        for k in range(0, outW):
            outImage[i][k] //= (scale * scale)

    displayImage()

def zoomInImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom In", "Enter the value", minvalue=2, maxvalue=4)
    outH = inH * scale
    outW = inW * scale

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    # Forwarding
    # for i in range(inH):
    #     for k in range(inW):
    #         outImage[i*scale][k*scale] = inImage[i][k]

    # Backwarding
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i//scale][k//scale]

    displayImage()

def zoomInImage2(): # Bilinear Interpolation
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom In", "Enter the value", minvalue=2, maxvalue=4)
    outH = inH * scale
    outW = inW * scale

    rH, rW, iH, iW = [0] * 4 # Real Position, Integer Position
    x, y = 0, 0 # Difference between real val and integer val
    C1, C2, C3, C4 = [0] * 4 # Base pixels for the target position(N)

    for i in range(outH):
        for k in range(outW):
            rH = i / scale ; rW = k / scale
            iH = int(rH) ; iW = int(rW)
            x = rW - iW ; y = rH - iH
            if 0 <= iH < (inH - 1) and 0 <= iW < (inW - 1):
                C1 = inImage[iH][iW]
                C2 = inImage[iH][iW+1]
                C3 = inImage[iH+1][iW+1]
                C4 = inImage[iH+1][iW]
                newValue = C1*(1-y)*(1-x) + C2*(1-y)*x\
                    + C3*y*x + C4*y*(1-x)
                outImage[i][k] = int(newValue)

    displayImage()

import matplotlib.pyplot as plt

def histImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    inCountList = [0] * 256
    outCountList = [0] * 256

    for i in range(inH):
        for k in range(inW):
            inCountList[inImage[i][k]] += 1
    for i in range(outH):
        for k in range(outW):
            outCountList[outImage[i][k]] += 1

    plt.plot(inCountList)
    plt.plot(outCountList)
    plt.show()



def emboImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    MSize = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]

    # Allocate empty memory for temp input image
    tmpInImage = malloc(inH+(MSize-1), inW+(MSize-1), 128)
    tmpOutImage = malloc(outH, outW)

    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+(MSize//2)][k+(MSize//2)] = inImage[i][k]

    # Mask Operation
    for i in range(MSize//2, inH+MSize//2):
        for k in range(MSize//2, inW+MSize//2):
            # Deal with each pixel
            S = 0.0
            for m in range(MSize):
                for n in range(MSize):
                    S += mask[m][n] * tmpInImage[i+m-MSize//2][k+n-MSize//2]
            tmpOutImage[i-MSize//2][k-MSize//2] = int(S)
    # Add 128
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 128

    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = value

    displayImage()

def morphImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Select an Additional Image
    filename2 = askopenfilename(parent=window, filetypes=(("RAW File", "*.raw"), ("All File", "*.*")))
    if filename2 == '' or filename2 == None:
        return
    fsize = os.path.getsize(filename2)  # File size (byte)
    inH2 = inW2 = int(math.sqrt(fsize))

    # Prepare empty memory for input image
    inImage2 = malloc(inH2, inW2)

    # File --> Memory
    with open(filename2, "rb") as rFp:
        for i in range(inH2):
            for k in range(inW2):
                inImage2[i][k] = int(ord(rFp.read(1)))

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    w1 = askinteger("Original Image Weight", "Enter the Weight (%)", minvalue=0, maxvalue=100)
    w1 /= 100
    w2 = 1 - w1
    for i in range(inH):
        for k in range(inW):
            newVal = int(inImage[i][k]*w1 + inImage2[i][k]*w2)
            if newVal > 255:
                newVal = 255
            elif newVal < 0:
                newVal = 0
            outImage[i][k] = newVal
    displayImage()

# Image Moving Algorithm
def moveImage():
    global panYN
    panYN = True
    canvas.configure(cursor='mouse')

def mouseClick(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH, sx,sy, ex, ey, panYN
    if panYN == False:
        return
    sx = event.x
    sy = event.y

def mouseDrop(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH, sx,sy, ex, ey, panYN
    if panYN == False:
        return
    ex = event.x
    ey = event.y

    # Attention: display size required!!
    outH = inH; outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    mx = sx - ex; my = sy - ey
    for i in range(inH):
        for k in range(inW):
            if 0 <= i - my < outH  and 0 <= k - mx < outW:
                outImage[i-my][k-mx] = inImage[i][k]

    displayImage()

def paraImage():  # with look-up table
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    LUT = [0 for _ in range(256)]
    for i in range(256):
        LUT[i] = int((255 * i / 128 - 1) ** 2)
    for i in range(inH):
        for k in range(inW):
            # outImage[i][k] = int(255 - 255 * (inImage[i][k] / 128 - 1)**2) # Cap
            outImage[i][k] = LUT[inImage[i][k]]
    displayImage()


# ============= Global Variables ====================================================

inImage, outImage = [], []
inW, inH, outW, outH = [0] * 4
window, canvas, paper = [None] * 3
filename = ""
panYN = False
sx,sy, ex, ey = [0] * 4

# =============  Main Code ==========================================================

if __name__ == '__main__':
    window = Tk()
    window.title('Computer Vision (DeepLearning) v0.03')
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
    comVisionMenu1.add_command(label="", command=)
    comVisionMenu1.add_command(label="Average", command=meanImage)
    comVisionMenu1.add_command(label="Posterize", command=posterImage)

    comVisionMenu1.add_command(label="Gamma", command=gammaImage)
    comVisionMenu1.add_command(label="Parabola", command=paraImage)
    comVisionMenu1.add_command(label="", command=)
    comVisionMenu1.add_command(label="Morphing", command=morphImage)

    comVisionMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="Stats", menu=comVisionMenu2)
    comVisionMenu2.add_command(label="Black&White", command=binImage)
    comVisionMenu2.add_command(label="Rotate", command=rotateImage)
    comVisionMenu2.add_command(label="Zoom Out(Mean)", command=zoomOutImage2)
    comVisionMenu2.add_command(label="Zoom In(BI)", command=zoomInImage2)
    comVisionMenu2.add_separator()
    comVisionMenu2.add_command(label="Histogram", command=histImage)
    comVisionMenu2.add_command(label="Stretch", command=stretchImage)
    comVisionMenu2.add_command(label="Stretch(EndIn)", command=stretchImage2)
    comVisionMenu2.add_command(label="Stretch(Equalized)", command=stretchImage3)

    comVisionMenu3 = Menu(mainMenu)
    mainMenu.add_cascade(label="Geometric", menu=comVisionMenu3)
    comVisionMenu3.add_command(label="Upside Down", command=updownImage)
    comVisionMenu3.add_command(label="Rotate", command=rotateImage)
    comVisionMenu3.add_command(label="Zoom Out", command=zoomOutImage)
    comVisionMenu3.add_command(label="Zoom In", command=zoomInImage)
    comVisionMenu3.add_command(label="Move", command=moveImage)

    comVisionMenu4 = Menu(mainMenu)
    mainMenu.add_cascade(label="Area", menu=comVisionMenu4)
    comVisionMenu4.add_command(label="Embossing", command=emboImage)

    window.mainloop()
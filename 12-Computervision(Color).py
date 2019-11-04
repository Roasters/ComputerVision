from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

import math
import os
import tempfile  # Get the temporary folder directory
import datetime

import struct
import pymysql
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

# In[2]:

inImage, outImage = None, None  # Object, not list
inW, inH, outW, outH = [0] * 4
window, canvas, paper = [None] * 3
filename = ""
VIEW_X, VIEW_Y = 512, 512 # Actual display size

# In[3]:


# Allocate memory and return list
def malloc(h, w, initValue=0):
    retMemory = [[initValue for _ in range(w)] for _ in range(h)]
    return retMemory


# Select a file and load it into memory
def openImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window, filetypes=(("Color File", "*.jpg;*.png;*.bmp;*.tif"), ("All File", "*.*")))
    if filename == '' or filename == None:
        return

    inImage = Image.open(filename)
    inW = inImage.width
    inH = inImage.height

    outImage = inImage.copy()
    outW = outImage.width
    outH = outImage.height

    displayImagePIL()


def saveImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension="*.jpg",
                           filetypes=(("JPG File", "*.jpg"), ("All file", "*.*")))
    if outImage == None:
        return
    if saveFp == '' or saveFp == None:
        return
    outImage.save(saveFp.name)
    print("Saved")


def displayImagePIL():
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
    # For better performance
    rgbImage = outImage.convert("RGB")
    rgbStr = ""  # Assign the string of the whole pixels
    for i in np.arange(0, outH, step):
        tmpStr = ""
        for k in np.arange(0, outW, step):
            i = int(i); k = int(k)
            r , g , b = rgbImage.getpixel((k, i))
            tmpStr += " #%02x%02x%02x" % (r, g, b)  # Need a space to separate each string
        rgbStr += "{" + tmpStr + "} "  # Same here
    paper.put(rgbStr)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state="normal")  # First arg: the middle point
    # Mouse Event

    canvas.pack(expand=1, anchor=CENTER)

    status.configure(text="Image Info: " + str(outH) + "x" + str(outW))

# In[4]:



def addImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    value = askfloat("Brightness", "0 ~ 1 : Darken\n1 ~ 16 : Brighten", minvalue=0.0, maxvalue=16.0)
    outImage = inImage.copy()
    outImage = ImageEnhance.Brightness(outImage).enhance(value)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def blurImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    outImage = inImage.copy()
    outImage = outImage.filter(ImageFilter.BLUR)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def zoominImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    scale = askinteger("Zoom In", "Scale(0 ~ 8)", minvalue=2, maxvalue=8)
    outImage = inImage.copy()
    outImage = outImage.resize((inH*scale, inW*scale))

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def zoomoutImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    scale = askinteger("Zoom Out", "Scale(0 ~ 8)", minvalue=2, maxvalue=8)
    outImage = inImage.copy()
    outImage = outImage.resize((inH//scale, inW//scale))

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def contrastImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    value = askfloat("Contrast", "Enter the value", minvalue=0.0, maxvalue=8.0)

    outImage = inImage.copy()
    outImage = ImageEnhance.Contrast(outImage).enhance(value)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def sharpImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    value = askfloat("Sharpness", "Enter the value", minvalue=0.0, maxvalue=8.0)

    outImage = inImage.copy()
    outImage = ImageEnhance.Sharpness(outImage).enhance(value)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()


def colorImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    value = askfloat("Color", "Enter the value", minvalue=0.0, maxvalue=8.0)

    outImage = inImage.copy()
    outImage = ImageEnhance.Color(outImage).enhance(value)

    outW = outImage.width
    outH = outImage.height

    displayImagePIL()

def stretchImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    outImage = inImage.copy()
    outImage = ImageOps.equalize(outImage)
    outW = outImage.width
    outH = outImage.height

    displayImagePIL()


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
fileMenu.add_command(label="Open", command=openImagePIL)
fileMenu.add_separator()
fileMenu.add_command(label="Save", command=saveImagePIL)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="Pixel", menu=comVisionMenu1)
comVisionMenu1.add_command(label="Brightness", command=addImagePIL)
comVisionMenu1.add_command(label="Contrast", command=contrastImagePIL)
comVisionMenu1.add_command(label="Sharpness", command=sharpImagePIL)
comVisionMenu1.add_command(label="Color", command=colorImagePIL)
comVisionMenu1.add_command(label="Stretch", command=stretchImagePIL)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="Area", menu=comVisionMenu2)
comVisionMenu2.add_command(label="Blurring", command=blurImagePIL)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="Geometric", menu=comVisionMenu3)
comVisionMenu3.add_command(label="Zoom In", command=zoominImagePIL)
comVisionMenu3.add_command(label="Zoom Out", command=zoomoutImagePIL)

window.mainloop()

# In[ ]:





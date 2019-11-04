from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

import math
import os
import tempfile  # Get the temporary folder directory
import datetime

import struct
import pymysql

import numpy as np

# In[2]:

inImage, outImage = [], []
inW, inH, outW, outH = [0] * 4
window, canvas, paper = [None] * 3
filename = ""
panYN = False
sx, sy, ex, ey = [0] * 4
VIEW_X, VIEW_Y = 512, 512 # Actual display size

# In[3]:


# Allocate memory and return list
def malloc(h, w, initValue= 0, dataType=np.uint8):
    retMemory = np.zeros((h, w), dtype=dataType)
    retMemory += initValue
    return retMemory


def loadImage(fname):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    fsize = os.path.getsize(fname)  # File size (byte)
    inH = inW = int(math.sqrt(fsize))

    inImage = np.fromfile(fname, dtype=np.uint8).reshape(inH, inW)

# Select a file and load it into memory
import time
def openImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window, filetypes=(("RAW File", "*.raw"), ("All File", "*.*")))
    if filename == '' or filename == None:
        return
    start = time.time()
    loadImage(filename)
    equalImage()
    print(time.time()-start)


def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    saveFp = asksaveasfile(parent=window, mode='rb', defaultextension="*.raw",
                           filetypes=(("RAW File", "*.raw"), ("All File", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    for i in range(outH):
        for k in range(outW):
            saveFp.write(struct.pack("B", outImage[i][k]))
    saveFp.close()


def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global VIEW_X, VIEW_Y
    if outH < VIEW_Y or outW < VIEW_X:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else:
        VIEW_X = VIEW_Y = 512
        step = outW / VIEW_X

    if canvas != None:  # If executed before
        canvas.destroy()

    window.geometry("{}x{}".format(str(int(VIEW_Y*1.2)), str(int(VIEW_X*1.2))))  # Empty wall
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)  # Empty board
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)  # Empty paper
    # For better performance
    rgbStr = ""  # Assign the string of the whole pixels
    for i in np.arange(0, outH, step):
        tmpStr = ""
        for k in np.arange(0, outW, step):
            i = int(i); k = int(k)
            r = g = b = outImage[i][k]
            tmpStr += " #%02x%02x%02x" % (r, g, b)  # Need a space to separate each string
        rgbStr += "{" + tmpStr + "} "  # Same here
    paper.put(rgbStr)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state="normal")  # First arg: the middle point
    # Mouse Event
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)

    canvas.pack(expand=1, anchor=CENTER)

    status.configure(text="Image Info: " + str(outH) + "x" + str(outW))

# In[4]:


def equalImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = inImage[:]

    displayImage()


def addImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Main Code
    value = askinteger("Brightening", "Enter the value", minvalue=-255, maxvalue=255)
    outImage = inImage + value
    outImage[outImage > 255] = 255
    outImage[outImage < 0] = 0

    displayImage()

def conImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = 255 - inImage

    displayImage()


def binImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Main Code
    mean = np.mean(inImage)
    outImage = np.where(inImage > mean, 255, 0, inImage)

    displayImage()

def meanImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    inMean = np.mean(inImage)
    outMean = np.mean(outImage)

    messagebox.showinfo("Pixel Mean", "Input Image: {:.1f}\nOutput Image: {:.1f}".format(inMean, outMean))


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

    inImage2 = np.fromfile(fname, dtype=np.uint8).reshape(inH2, inW2)

    # Main Code
    w1 = askinteger("Original Image Weight", "Enter the Weight (%)", minvalue=0, maxvalue=100)
    w1 /= 100
    w2 = 1 - w1

    outImage = inImage * w1 + inImage2 * w2
    outImage = outImage.astype(np.uint8)
    outImage[outImage > 255] = 255
    outImage[outImage < 0] = 0

    displayImage()


def paraImage():  # with look-up table
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    outImage = 255 - 255 * (inImage / 128 - 1)**2 # Cap
    outImage = outImage.astype(np.uint8)

    displayImage()


# In[5]:


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
            outImage[i][k] = int(((inImage[i][k] - low) / (high - low)) * 255)

    displayImage()


def stretchImage2():  # End-In
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
            value = int(((inImage[i][k] - low) / (high - low)) * 255)
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
            outImage[i][k] = value

    displayImage()


def stretchImage3():  # Equalization
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
        cumCount[i] += cumCount[i - 1] + inCountList[i]

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


def histImage2():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH

    outCountList = [0] * 256
    normalCountList = [0] * 256

    # Get frequency
    for i in range(outH):
        for k in range(outW):
            outCountList[outImage[i][k]] += 1
    # Normalization  (count - min) * high / (max - min)
    maxVal = max(outCountList)
    minVal = min(outCountList)
    high = 256
    for i in range(len(outCountList)):
        normalCountList[i] = (outCountList[i] - minVal) * high / (maxVal - minVal)

    # Create a subwindow
    subWindow = Toplevel(window) # sub-level of window
    subWindow.geometry("256x256")
    subCanvas = Canvas(subWindow, width=256, height=256)
    subPaper = PhotoImage(width=256, height=256)
    subCanvas.create_image((256//2, 256//2), image=subPaper, state="normal")

    for i in range(len(normalCountList)):
        for k in range(int(normalCountList[i])):
            data = 0
            subPaper.put("#%02x%02x%02x"% (data, data, data), (i, 255-k))

    subCanvas.pack(expand=1, anchor=CENTER)
    subWindow.mainloop()

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
            outImage[i // scale][k // scale] += inImage[i][k]
    for i in range(0, outH):
        for k in range(0, outW):
            outImage[i][k] //= (scale * scale)

    displayImage()


def zoomInImage2():  # Bilinear Interpolation
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom In", "Enter the value", minvalue=2, maxvalue=4)
    outH = inH * scale
    outW = inW * scale

    rH, rW, iH, iW = [0] * 4  # Real Position, Integer Position
    x, y = 0, 0  # Difference between real val and integer val
    C1, C2, C3, C4 = [0] * 4  # Base pixels for the target position(N)

    for i in range(outH):
        for k in range(outW):
            rH = i / scale;
            rW = k / scale
            iH = int(rH);
            iW = int(rW)
            x = rW - iW;
            y = rH - iH
            if 0 <= iH < (inH - 1) and 0 <= iW < (inW - 1):
                C1 = inImage[iH][iW]
                C2 = inImage[iH][iW + 1]
                C3 = inImage[iH + 1][iW + 1]
                C4 = inImage[iH + 1][iW]
                newValue = C1 * (1 - y) * (1 - x) + C2 * (1 - y) * x + C3 * y * x + C4 * y * (1 - x)
                outImage[i][k] = int(newValue)

    displayImage()


# In[6]:


# Image Moving Algorithm
def moveImage():
    global panYN
    panYN = True
    canvas.configure(cursor='mouse')


def mouseClick(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH, sx, sy, ex, ey, panYN
    if panYN == False:
        return
    sx = event.x
    sy = event.y


def mouseDrop(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH, sx, sy, ex, ey, panYN
    if panYN == False:
        return
    ex = event.x
    ey = event.y

    # Attention: display size required!!
    outH = inH;
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    mx = sx - ex;
    my = sy - ey
    for i in range(inH):
        for k in range(inW):
            if 0 <= i - my < outH and 0 <= k - mx < outW:
                outImage[i - my][k - mx] = inImage[i][k]

    displayImage()


# In[7]:


def emboImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    outH = inH
    outW = inW

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Main Code
    MSize = 3
    mask = [[-1, 0, 0],
            [0, 0, 0],
            [0, 0, 1]]

    # Allocate empty memory for temp input image
    tmpInImage = malloc(inH + (MSize - 1), inW + (MSize - 1), 128)
    tmpOutImage = malloc(outH, outW)

    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + (MSize // 2)][k + (MSize // 2)] = inImage[i][k]

    # Mask Operation
    for i in range(MSize // 2, inH + MSize // 2):
        for k in range(MSize // 2, inW + MSize // 2):
            # Deal with each pixel
            S = 0.0
            for m in range(MSize):
                for n in range(MSize):
                    S += mask[m][n] * tmpInImage[i + m - MSize // 2][k + n - MSize // 2]
            tmpOutImage[i - MSize // 2][k - MSize // 2] = int(S)
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


# In[8]:


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
    cx = inW // 2;
    cy = inH // 2
    for i in range(outH):
        for k in range(outW):
            xs = i;
            ys = k
            xd = int(math.cos(radian) * (xs - cx) - math.sin(radian) * (ys - cy)) + cx
            yd = int(math.sin(radian) * (xs - cx) + math.cos(radian) * (ys - cy)) + cy
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


def zoomInImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Attention: display size required!!
    scale = askinteger("Zoom In", "Enter the value", minvalue=2, maxvalue=4)
    outH = inH * scale
    outW = inW * scale

    # Memory Allocation
    outImage = malloc(outH, outW)

    # Backwarding
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i // scale][k // scale]

    displayImage()


# In[9]:


# =============  Global Variables ===================================================
IP_ADDR = '192.168.56.110';
USER_NAME = 'root';
USER_PASSWORD = '1234'
DB_NAME = 'BigData_DB';
CHAR_SET = "utf8"
page = 0

# =============  Functions ==========================================================
def selectFolder() :
    global rawFileList
    foldername = askdirectory(parent=window)
    if foldername == '' or foldername == None:
        return
    edt1.insert(0, str(foldername))
    # 파일 목록 뽑기
    rawFileList = []
    for dirName, subDirList, fnames in os.walk(foldername) :
        for fname in fnames :
            filename, extname = os.path.basename(fname).split(".")
            if extname.upper().strip() == 'RAW' :
                rawFileList.append(os.path.join(dirName,fname))

def uploadData() :
    global rawFileList
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try :
        sql = '''
            CREATE TABLE rawImage_TBL (
            raw_id INT AUTO_INCREMENT PRIMARY KEY,
            raw_fname VARCHAR(30),
            raw_extname CHAR(5),
            raw_height SMALLINT, raw_width SMALLINT,
            raw_avg  TINYINT UNSIGNED , 
            raw_max  TINYINT UNSIGNED,  raw_min  TINYINT UNSIGNED,
            raw_data LONGBLOB);
        '''
        cur.execute(sql)
    except :
        pass

    for fullname in rawFileList :
        with open(fullname, 'rb') as rfp :
            binData = rfp.read()

        fname, extname = os.path.basename(fullname).split(".")
        fsize = os.path.getsize(fullname)
        height = width = int(math.sqrt(fsize))
        avgVal, maxVal, minValue = findStat(fullname) # 평균,최대,최소
        sql = "INSERT INTO rawImage_TBL(raw_id , raw_fname,raw_extname,"
        sql += "raw_height,raw_width,raw_avg,raw_max,raw_min,raw_data) "
        sql += " VALUES(NULL,'" + fname + "','" + extname +"',"
        sql += str(height) + "," + str(width) + ","
        sql += str(avgVal)+ "," + str(maxVal) + "," + str(minValue)
        sql += ", %s )"
        tupleData = (binData,)
        cur.execute(sql, tupleData)
        con.commit()
        print("업로드 OK -->" + fullname)

    cur.close()
    con.close()
    print("끝~~~")


# def uploadFolder():
#     con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASSWORD, db=DB_NAME, charset=CHAR_SET)
#     cur = con.cursor()
#     fnameList = []
#     folder = askdirectory(parent=window)
#     for dirName, subDirList, fnames in os.walk(folder):
#         for fname in fnames:
#             if os.path.splitext(fname)[1].upper() == ".RAW":
#                 fnameList.append(os.path.join(dirName, fname))
#     for fullname in fnameList:
#         with open(fullname, 'rb') as rfp:
#             binData = rfp.read()
#         fname = os.path.basename(fullname)
#         fsize = os.path.getsize(fullname)
#         height = width = int(math.sqrt(fsize))
#         now = datetime.datetime.now()
#         upDate = now.strftime("%Y-%m-%d")
#         upUser = USER_NAME
#         minval, maxval, meanval = statsImage(binData)
#         sql = "INSERT INTO rawImage_TBL(raw_id, raw_height, raw_width, raw_fname,                 raw_avg, raw_min, raw_max, raw_update, raw_uploader, raw_data)                 VALUES(NULL, {}, {}, '{}', {}, {}, {}, '{}', '{}', ".format(
#             height, width, fname, meanval, minval, maxval, upDate, upUser) + "%s)"
#         tupleData = (binData,)
#         cur.execute(sql, tupleData)
#         con.commit()  # To save the changed data
#     cur.close()
#     con.close()


def statsImage(fname):
    fsize = os.path.getsize(fname)
    inH = inW = int(math.sqrt(fsize))

    ## 입력영상 메모리 확보 ##

    inImage = malloc(inH, inW)
    # 파일 --> 메모리
    with open(fname, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum // (inW * inH)
    maxVal = minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]
    return avg, maxVal, minVal


def downloadData():
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASSWORD, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    sql = "SELECT raw_fname, raw_data FROM rawImage_TBL WHERE raw_id = 1"
    cur.execute(sql)
    fname, binData = cur.fetchone()

    fullPath = tempfile.gettempdir() + '/' + fname
    with open(fullPath, "wb") as wfp:
        wfp.write(binData)

    cur.close()
    con.close()

def loadImageDB(fname):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    inH = inW = int(math.sqrt(os.path.getsize(fname)))

    # Prepare empty memory for input image
    inImage = malloc(inH, inW)

    # File --> Memory
    with open(fname, "rb") as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))

def clickNext():
    global page
    if page + 10 < len(fileList):
        page += 10
    makeList()

def clickPrev():
    global page
    if page - 10 >= 0:
        page -= 10
    makeList()

def loadMysql():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASSWORD,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT raw_id, raw_fname, raw_extname, raw_height, raw_width FROM rawImage_TBL"

    cur.execute(sql)

    queryList = cur.fetchall()
    rowList = [' : '.join(map(str, row)) for row in queryList]

    import tempfile
    def selectRecord():
        global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
        selIndex = listbox.curselection()[0]
        subWindow.destroy()

        raw_id = queryList[selIndex][0]

        sql = "SELECT raw_fname, raw_extname, raw_data FROM rawImage_TBL WHERE raw_id = %d"%raw_id
        cur.execute(sql)
        fname, extname, binData = cur.fetchone()

        fullPath = tempfile.gettempdir() + '/' + fname + "." + extname
        with open(fullPath, "wb") as wfp:
            wft.write(binData)
        cur.close()
        con.close()

        loadImageDB(fullPath)
        equalImage()

    # Create a subwindow to show the list
    subWindow = Toplevel(window)
    # subWindow.geometry("")
    listbox = Listbox(subWindow)
    button = Button(subWindow, text="Select", command=selectRecord)
    for rowStr in rowList:
        listbox.insert(END, rowStr)

    listbox.pack(expand=1, anchor=CENTER)
    button.pack()
    cur.close()
    con.close()


import random
def saveTempImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000, 99999)) + ".raw"
    if saveFp == '' or saveFp == None:
        return
    saveFp = open(saveFp, 'wb')
    for i in range(outH):
        for k in range(outW):
            saveFp.write(struct.pack("B", outImage[i][k]))
    saveFp.close()
    return saveFp.name


def saveMysql():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASSWORD,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    try :
        sql = '''
            CREATE TABLE rawImage_TBL (
            raw_id INT AUTO_INCREMENT PRIMARY KEY,
            raw_fname VARCHAR(30),
            raw_extname CHAR(5),
            raw_height SMALLINT, raw_width SMALLINT,
            raw_avg  TINYINT UNSIGNED , 
            raw_max  TINYINT UNSIGNED,  raw_min  TINYINT UNSIGNED,
            raw_data LONGBLOB);
        '''
        cur.execute(sql)
    except :
        pass

    # Save outImage at temp folder, and assign to full name

    fullname = saveTempImage()
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    avgVal, maxVal, minValue = statsImage(fullname)  # 평균,최대,최소
    sql = "INSERT INTO rawImage_TBL(raw_id , raw_fname,raw_extname,"
    sql += "raw_height,raw_width,raw_avg,raw_max,raw_min,raw_data) "
    sql += " VALUES(NULL,'" + fname + "','" + extname + "',"
    sql += str(height) + "," + str(width) + ","
    sql += str(avgVal) + "," + str(maxVal) + "," + str(minValue)
    sql += ", %s )"
    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()

    cur.close()
    con.close()

    os.remove(fullname)
    print("Upload Done: ", fullname)

# In[10]:


window = Tk()
window.title('Computer Vision (DeepLearning) v0.03')
status = Label(window, text="Image Info: ", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
window.geometry("500x500")

edt1 = Entry(window, width=50);
edt1.pack()

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
comVisionMenu1.add_command(label="Contrast", command=conImage)
comVisionMenu1.add_command(label="Average", command=meanImage)

comVisionMenu1.add_command(label="Gamma", command=gammaImage)
comVisionMenu1.add_command(label="Parabola", command=paraImage)
comVisionMenu1.add_command(label="Morphing", command=morphImage)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="Stats", menu=comVisionMenu2)
comVisionMenu2.add_command(label="Black&White", command=binImage)
comVisionMenu2.add_command(label="Rotate", command=rotateImage)
comVisionMenu2.add_command(label="Zoom Out(Mean)", command=zoomOutImage2)
comVisionMenu2.add_command(label="Zoom In(BI)", command=zoomInImage2)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="Histogram", command=histImage)
comVisionMenu2.add_command(label="Histogram(NoMPL)", command=histImage2)
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

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label="DB I/O", menu=comVisionMenu5)
comVisionMenu5.add_command(label="Load from MySQL", command=loadMysql)
comVisionMenu5.add_command(label="Save at MySQL", command=saveMysql)
comVisionMenu5.add_command(label="Select Folder", command=selectFolder)
comVisionMenu5.add_command(label="Open(DB)", command=loadImage)

window.mainloop()

# In[ ]:





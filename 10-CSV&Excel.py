from tkinter import *
from tkinter.filedialog import *

import csv
import math
import os
from tkinter import ttk
import xlrd, xlwt

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
    rgbStr = ""
    for i in range(outH):
        tmpStr = ""
        for k in range(outW):
            r = g = b = outImage[i][k]
            tmpStr += " #%02x%02x%02x"%(r, g, b)
        rgbStr += "{" + tmpStr + "} "
    paper.put(rgbStr)
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

# ============= For CSV Operation ==================================================

def toCsv():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    header = ("Row", "Column", "Value")
    csvList =[]
    for i in range(outH):
        for k in range(outW):
           csvList.append([i, k, outImage[i][k]])
    return csvList, header

def saveCSV():
    csvList, Header = toCsv()

    # Choose save path
    saveFp = asksaveasfile(parent=window, mode='wt', defaultextension="*.csv",
                           filetypes=(("CSV File", "*.csv"), ("All File", "*.*")))
    with open(saveFp.name, "w", newline='') as wFp:
        writer = csv.writer(wFp)
        writer.writerow(Header)
        for row in csvList:
            writer.writerow(row)

def openCSV():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    openFp = askopenfilename(parent=window, filetypes=(("CSV File", "*.csv"), ("All File", "*.*")))
    with open(openFp) as rFp:
        reader = csv.reader(rFp)
        next(reader)  # Header can be ignored

        tmpList = []
        numRow = 0  # To get inH
        for row in reader:
            i, k, v = map(int, row)  # CSV file is basically formed as strings
            tmpList.append([i, k, v])
            if numRow < i:
                numRow = i

    inH = inW = numRow + 1
    inImage = malloc(inH, inW)

    for i, k, v in tmpList:
        inImage[i][k] = v

    equalImage()

def openExcel():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    openFp = askopenfilename(parent=window, filetypes=(("Excel File", "*.xlsx"), ("All File", "*.*")))
    workbook = xlrd.open_workbook(openFp)

    wsList = workbook.sheets()

    # Extract header
    headerList = []
    for i in range(wsList[0].ncols):
        headerList.append(wsList[0].cell_value(0, i))

    # Fill in values
    csvList = []
    for wsheet in wsList:
        rowCount = wsheet.nrows
        colCount = wsheet.ncols
        for i in range(1, rowCount):
            tmpList = []
            for k in range(colCount):
                tmpList.append(wsheet.cell_value(i, k))
            csvList.append(tmpList)

    sheet.delete(*sheet.get_children())
    sheet.column("#0", width=70)
    sheet.heading("#0", text="Index")

    sheet["columns"] = headerList  # Names of columns
    for header in headerList:
        sheet.column(header, width=100);
        sheet.heading(header, text=header)

    for i in range(len(csvList)):
        sheet.insert("", "end", text=str(i + 1), values=csvList[i])

    sheet.pack()

def toExcel():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    header = ("Row", "Column", "Value")
    csvList =[]
    for i in range(outH):
        for k in range(outW):
           csvList.append([i, k, outImage[i][k]])
    return csvList, header

def saveExcel():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Choose save path
    saveFp = asksaveasfile(parent=window, mode='wt', defaultextension="*.xls",
                           filetypes=(("Excel File", "*.xls"), ("All File", "*.*")))

    xlsName = saveFp.name
    sheetName = os.path.basename(filename)
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetName)

    for i in range(outH):
        for k in range(outW):
            ws.write(i, k, outImage[i][k])

    wb.save(xlsName)
    print("Save Complete")

import xlsxwriter as xw
def saveExcelArt():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    # Choose save path
    saveFp = asksaveasfile(parent=window, mode='wt', defaultextension="*.xls",
                           filetypes=(("Excel File", "*.xls"), ("All File", "*.*")))

    xlsName = saveFp.name
    sheetName = os.path.basename(filename)

    wb = xw.Workbook(xlsName)
    ws = wb.add_worksheet(sheetName)

    ws.set_column(0,outW-1, 1.0)   # About 0.34
    for i in range(outH):   # Rows are assigned separately
        ws.set_row(i, 9.5)  # About 0.35

    for i in range(outH):
        for k in range(outW):
            data = outImage[i][k]
            # Adjust background color according to data
            if data > 15:
                hexStr = "#" + hex(data)[2:] * 3
            else:
                hexStr = "#" + ('0' + hex(data)[2:]) * 3
            # Adjust cell format to set color
            cellFormat = wb.add_format()
            cellFormat.set_bg_color(hexStr)

            ws.write(i, k, '', cellFormat) # The image value goes to empty string part
    wb.close()
    print("Save Completed")

def loadExcelImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    openFp = askopenfilename(parent=window, filetypes=(("Excel File", "*.xls"), ("All File", "*.*")))
    workbook = xlrd.open_workbook(openFp)
    ws = workbook.sheets()[0]

    rowCount = ws.nrows
    colCount = ws.ncols
    inH = inW = rowCount
    inImage = malloc(inH, inW)

    for i in range(rowCount):
        for k in range(colCount):
            inImage[i][k] = int(ws.cell_value(i, k))

    equalImage()

# ============= Global Variables ====================================================

inImage, outImage = [], []
inW, inH, outW, outH = [0] * 4
window, canvas, paper =[None] * 3
filename = ""


# =============  Main Code ==========================================================

if __name__ == '__main__':
    window = Tk()
    window.title('Computer Vision (CSV) v0.01')
    window.geometry("500x500")
    sheet = ttk.Treeview(window)

    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Open", command=openImage)
    fileMenu.add_separator()
    fileMenu.add_command(label="Save", command=saveImage)

    comVisionMenu1 = Menu(mainMenu)
    mainMenu.add_cascade(label="CSV", menu=comVisionMenu1)
    comVisionMenu1.add_command(label="Save as CSV", command=saveCSV)
    comVisionMenu1.add_command(label="Open CSV", command=openCSV)

    comVisionMenu2 = Menu(mainMenu)
    mainMenu.add_cascade(label="Excel", menu=comVisionMenu2)
    comVisionMenu2.add_command(label="Save as Excel", command=saveExcel)
    comVisionMenu2.add_command(label="Open Excel", command=openExcel)
    comVisionMenu2.add_command(label="Excel Art", command=saveExcelArt)
    comVisionMenu2.add_command(label="Load Excel Image", command=loadExcelImage)

    window.mainloop()
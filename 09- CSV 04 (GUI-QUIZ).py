import csv
import random
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk

window = Tk()
window.geometry("1500x500")
sheet = ttk.Treeview(window)

sheet.column("#0", width=70)
sheet.heading("#0", text="Index")

filename = askopenfilename(parent=None, filetypes=(("CSV File", "*.csv"), ("All File", "*.*")))
csvList = []
with open(filename) as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader)
    for cList in reader:
        csvList.append(cList)

sheet["columns"] = headerList  # Names of columns
for header in headerList:
    sheet.column(header, width=100); sheet.heading(header, text=header)

for i in range(len(csvList)):
    sheet.insert("", "end", text=str(i+1), values=csvList[i])

sheet.pack()
window.mainloop()
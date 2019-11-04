import csv
import random
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk

window = Tk()
window.geometry("800x500")
sheet = ttk.Treeview(window)

# Create a header for first column

sheet.column("#0", width=70)
sheet.heading("#0", text="Title1")


# Create headers for columns from the second column

sheet["columns"] = ("A", "B", "C")  # Names of columns
sheet.column("A", width=70); sheet.heading("A", text="Title2")
sheet.column("B", width=70); sheet.heading("B", text="Title3")
sheet.column("C", width=70); sheet.heading("C", text="Title4")

# Fill in the contents

sheet.insert("", "end", text="Col1Val1", values=("Col2Val1", "Col3Val1", "Col4Val1"))
sheet.insert("", "end", text="Col1Val2", values=("Col2Val2", "Col3Val2", "Col4Val2"))
sheet.insert("", "end", text="Col1Val3", values=("Col2Val3", "Col3Val3", "Col4Val3"))

sheet.pack()
window.mainloop()
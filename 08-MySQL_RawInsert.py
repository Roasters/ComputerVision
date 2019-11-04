from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
import pymysql

import math
import os

# =============  Global Variables ===================================================
IP_ADDR = '192.168.56.108'; USER_NAME = 'root'; USER_PASSWORD = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = "utf8"

# =============  Functions ==========================================================
def selectFile():
    filename = askopenfilename(parent=window, filetypes=(("RAW File", "*.raw"), ("All File", "*.*")))
    if filename == '' or filename == None:
        return
    edt1.insert(0, filename)

import datetime
def uploadData():
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASSWORD, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    fullname = edt1.get()
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()
    fname = os.path.basename(fullname)
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    now = datetime.datetime.now()
    upDate = now.strftime("%Y-%m-%d")
    upUser = USER_NAME
    sql = "INSERT INTO rawImage_TBL(raw_id, raw_height, raw_width, raw_fname, \
            raw_avg, raw_update, raw_uploader, raw_data) \
            VALUES(NULL, {}, {}, '{}', {}, '{}', '{}', ".format(height, width, fname, 0, upDate, upUser) + "%s)"
    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()  # To save the changed data
    cur.close()
    con.close()

import tempfile   # Get the temporary folder directory
def downloadData():
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASSWORD, db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    sql = "SELECT raw_fname, raw_data FROM rawImage_TBL WHERE raw_id = 1"
    cur.execute(sql)
    fname, binData = cur.fetchone()

    fullPath = tempfile.gettempdir() + '/' + fname
    with open(fullPath, "wb") as wfp:
        wfp.write(binData)
    print(fullPath)

    cur.close()
    con.close()

# =============  Main Code ==========================================================

window = Tk()
window.title('Raw to DB v0.02')
window.geometry("500x500")

edt1 = Entry(window, width=50); edt1.pack()
btnFile = Button(window, text="File Select", command=selectFile); btnFile.pack()
btnUpload = Button(window, text="Data Upload", command=uploadData); btnUpload.pack()
btnDownload = Button(window, text="Data Download", command=downloadData); btnDownload.pack()

window.mainloop()

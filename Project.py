from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

import hgtk
import re
import random
import pyperclip

def selectOps():
    global inText, outText, window, subWindow
    inText = textPad.get(1.0, END)
    outText = inText

    subWindow = Toplevel(window)
    subWindow.title("처리 방식을 고르세요")
    btnOriginal = Button(subWindow, text="텍스트복원", command=makeOriginal)
    
    btn1 = Button(subWindow, text="캠릿브지 연결구과", command=reorderText)
    btn2 = Button(subWindow, text="위불이 도로오", command=vowelTrans1)
    btn3 = Button(subWindow, text="넌 참 밥오야", command=consoTrans1)
    btn4 = Button(subWindow, text="난 널 따랑해", command=unaspText)
    # btn5 = Button(subWindow, text="박휘벌레", command=consoTrans2)

    btn6 = Button(subWindow, text="아빠가방에들어가신다", command=noSpace)
    btn7 = Button(subWindow, text="완전 별로네여^^", command=sarcasticText)

    btn1.pack()
    btn2.pack()
    btn3.pack()
    btn4.pack()
    # btn5.pack()
    btn6.pack()
    btn7.pack()

def koreanLetters(text):
    global inText, outText, window, subWindow
    textLetter = hgtk.text.decompose(text)
    return textLetter

def showText():
    global inText, outText, window, subWindow
    subWindow2 = Toplevel(subWindow)
    subWindow2.geometry("300x400")
    subWindow2.title("처리 결과")
    textLabel = Message(subWindow2, text=outText)
    btnCopy = Button(subWindow2, text="클립보드에 복사", command=textCopy)
    btnCopy.place(x=100, y=380)
    textLabel.pack()

def textCopy():
    global inText, outText, window, subWindow
    pyperclip.copy(outText)
    messagebox.showinfo("복사완료", "Ctrl+v 를 사용해 필요한 곳에 붙이세요")

def openText():
    global filename
    if textPad.get(1.0, END) != "":
        textPad.delete(1.0, END)
    
    filename = askopenfilename(parent=window, filetypes=(("Text File", "*.txt"), ("All File", "*.*")))
    window.title(os.path.split(filename)[1])
    with open(filename, "r") as f:
        text = f.read()

    textPad.insert("1.0", text, "a")

def saveText():
    global filename
    with open(filename, "w") as f:
        f.write(textPad.get(1.0, END))
    status.configure(text="저장됨")

def saveAsText():
    saveTxt = asksaveasfile(parent=window, mode="w", defaultextension=".txt",
                            filetypes=(("Text File", "*.txt;*.raw"), ("All File", "*.*")))

    if saveTxt == None or saveTxt == "":
        return

    saveTxt.write(textPad.get(1.0, END)) # 1.0 -> (1, 0)
    saveTxt.close()
    status.configure(text="저장됨")

# ======= Text Transformation Functions

def makeOriginal():
    global inText, outText, window, subWindow
    outText = inText

def unaspText():
    global inText, outText, window, subWindow
    textDecom = koreanLetters(inText)
    tmpStr = ""
    for l in textDecom:
        try:
            tmpStr += UNASP[l]
        except:
            tmpStr += l
    outText = hgtk.text.compose(tmpStr)
    showText()

def reorderText():
    global inText, outText, window, subWindow
    wordList = re.sub(r"\W", " ", inText).split()
    for i in range(len(wordList)):
        word = wordList[i]
        if len(word) == 4:
            wordList[i] = word[0] + word[2] + word[1] + word[3]
        if len(word) >= 5:
            randIdx = list(range(1, len(word)-1))
            random.shuffle(randIdx)
            tmp = word[0]
            for Idx in randIdx:
                tmp += word[Idx]
            wordList[i] = tmp + word[-1]
    outText = " ".join(wordList)
    
    showText()

def vowelTrans1():
    global inText, outText, window, subWindow
    textDecom = koreanLetters(inText)

    tmpStr = ""
    for l in textDecom:
        try:
            tmpStr += vowelTran1[l]
        except:
            tmpStr += l
    outText = hgtk.text.compose(tmpStr)
    
    showText()

def consoTrans1():
    global inText, outText, window, subWindow
    textDecom = koreanLetters(inText)

    tmpStr = textDecom[:2]
    for i in range(2, len(textDecom)-2):
        l = textDecom[i]
        if l == "ㅇ":
            tmpStr += l
        elif l == "ㅎ":
            tmpStr += l
        elif textDecom[i-2] in vowel and textDecom[i+1] in vowel:
            tmp = tmpStr[-1]
            tmpStr = tmpStr[:-1]
            tmpStr += consoTran1[l][0] + tmp + consoTran1[l][-1]
        else:
            tmpStr += l
    tmpStr += textDecom[-2:]

    outText = hgtk.text.compose(tmpStr)

    showText()

### Additional Operations

def noSpace():
    global inText, outText, window, subWindow
    outText = outText.replace(" ", "")

def sarcasticText():
    global inText, outText, window, subWindow

    symbols = ["^^", "XD", ":)","^o^", "★.★", "♥♥♥"]
    tmpStr = ""
    for s in outText:
        idx = random.randrange(0, len(symbols))
        if s == ".":
            tmpStr += symbols[idx]
        else:
            tmpStr += s
    outText = tmpStr

    showText()

# Keyboard Shortcuts Functions

def openCut(event):
    openText()
def saveCut(event):
    saveText()
def saveAsCut(event):
    saveAsText()
def countLetter(event):
    global status, textPad, window
    status.configure(text="글자 수: {}".format(len(textPad.get(1.0, END).replace("\n", ""))))

# ======= Global Variables
inText, outText = "", ""

# ======= Korean Letters
consonant = hgtk.letter.CHO
vowel = hgtk.letter.JOONG

UNASP = {"ㄱ" : "ㄲ", "ㅋ" : "ㄲ", "ㅅ" : "ㄸ", "ㄷ" : "ㄸ", "ㅌ" : "ㄸ", "ㅂ" : "ㅃ", "ㅍ" : "ㅃ", "ㅅ" : "ㅆ", "ㅈ" : "ㅉ"}
ASP = {"ㅊ" : "ㅈㅎ","ㅋ" : "ㄱㅎ","ㅌ" : "ㄷㅎ","ㅍ" : "ㅂㅎ"}

vowelTran1 = {"ㅗ" : "ㅓ", "ㅓ" : "ㅗ", "ㅏ" : "ㅑ", "ㅓ" : "ㅕ", "ㅜ" : "ㅡ", "ㅡ" : "ㅜ", "ㅣ" : "ㅟ", "ㅐ" : "ㅔ", "ㅔ" : "ㅖ", "ㅟ" : "ㅢ"}
consoTran1 = {letter : letter + "ㅇ" for letter in consonant}  # 바보 -> 밥오

oneByOne = {"이": "2", "더럽" : "the love"}
# ======= Main Code

window = Tk()
window.title("Text Transformer")
window.geometry("400x300")
textPad = Text(window, width=100, height=80)
textPad.insert("1.1", "", "a")

scrollbar = Scrollbar(window, jump = 1)
scrollbar.configure(command=textPad.yview)
scrollbar.pack(side=RIGHT, fill=BOTH)

status = Label(window, text="", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="열기", command=openText)
fileMenu.add_command(label="저장", command=saveText)
fileMenu.add_command(label="다른이름으로 저장", command=saveAsText)

# Keyboard Shorcuts
window.bind("<Control-o>", openCut)
window.bind("<Control-s>", saveCut)
window.bind("<Control-S>", saveAsCut)
window.bind("<Key>", countLetter)

transButton = Button(window, text="변환하기", command=selectOps)

transButton.pack()
textPad.pack()
window.mainloop()
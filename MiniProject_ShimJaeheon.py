from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter import font

import hgtk
import re
import random
import pyperclip
import gensim

def selectOps():
    global inText, outText, window, subWindow
    inText = textPad.get(1.0, END)

    if inText.strip() == "":
        messagebox.showinfo("주의", "텍스트를 입력한 뒤에 실행해 주세요")
        return

    subWindow = Toplevel(window)
    subWindow.title("처리 방식을 고르세요")
    btnOriginal = Button(subWindow, text="텍스트복원", command=makeOriginal)
    ##################################################################
    Message(subWindow, text="기본 작업", width=100, bg="#B9B9B9").pack(fill=X)

    Button(subWindow, text="캠릿브지 연결구과", command=reorderText).pack(fill=X)
    Button(subWindow, text="위불이 도로오", command=vowelTrans1).pack(fill=X)
    Button(subWindow, text="넌 참 밥오야", command=consoTrans1).pack(fill=X)
    Button(subWindow, text="난 널 따랑해", command=unaspText).pack(fill=X)
    Button(subWindow, text="뭄좀건 핑항셈용", command=consoTrans2).pack(fill=X)

    Message(subWindow, text="추가 작업", width=100, bg="#B9B9B9").pack(fill=X)

    Button(subWindow, text="아빠가방에들어가신다", command=noSpace).pack(fill=X)
    Button(subWindow, text="완전 별로네여^^", command=sarcasticText).pack(fill=X)
    ###################################################################
    subWindow.mainloop()

def koreanLetters(text):
    global inText, outText, window, subWindow
    textLetter = hgtk.text.decompose(text)
    return textLetter

def showText():
    global inText, outText, window, subWindow
    subWindow2 = Toplevel(subWindow)
    subWindow2.geometry("300x150")
    subWindow2.title("처리 결과")
    textLabel = Message(subWindow2, text=outText, font=((Font, fontSize)), width=300, justify=CENTER)
    btnCopy = Button(subWindow2, text="클립보드에 복사", command=textCopy)
    btnCopy.pack(side=BOTTOM)
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
    if filename == None or filename == "":
        return

    window.title("Reviewer's Text | " + os.path.split(filename)[1])
    with open(filename, "r") as f:
        text = f.read()

    textPad.insert("1.0", text, "a")

def saveText():
    global filename
    if filename == "":
        saveAsText()
        return

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
        if l in ["ㅇ", "ㅎ", "ㅈ", "ㅊ", "ㅌ", "ㅍ"]:
            tmpStr += l
        elif textDecom[i-2] in nucleus and textDecom[i+1] in nucleus:
            tmp = tmpStr[-1]
            tmpStr = tmpStr[:-1]
            tmpStr += consoTran1[l][0] + tmp + consoTran1[l][-1]
        else:
            tmpStr += l
    tmpStr += textDecom[-2:]

    outText = hgtk.text.compose(tmpStr)
    showText()

def consoTrans2():
    global inText, outText, window, subWindow
    textDecom = koreanLetters(inText)
    syllables = textDecom.split("ᴥ")
    om = ["ㅇ", "ㅁ"]
    for i in range(len(syllables)):
        if len(syllables[i]) == 2:
            idx = random.randrange(0, 2)
            syllables[i] += om[idx] 

    tmpStr = "ᴥ".join(syllables)
    outText = hgtk.text.compose(tmpStr)

    showText()

### Additional Operations

def noSpace():
    global inText, outText, window, subWindow
    if outText == "":
        messagebox.showinfo("주의", "기본 작업을 처리한 후에 실행해 주십시오.")
        return

    outText = outText.replace(" ", "")
    showText()

def sarcasticText():
    global inText, outText, window, subWindow
    if outText == "":
        messagebox.showinfo("주의", "기본 작업을 처리한 후에 실행해 주십시오.")
        return

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

def fontSelect():
    global textPad, window, inText, outText

    subWindow3 = Toplevel(window)
    subWindow3.title("폰트 선택")
    scrollbar2 = Scrollbar(subWindow3, jump = 1)
    scrollbar2.pack(side=RIGHT, fill=Y, expand=NO)

    fonts=list(font.families())
    fonts.sort()

    display = Listbox(subWindow3)
    display.pack(fill=BOTH, expand=YES, side=TOP)

    display.configure(yscrollcommand=scrollbar2.set)

    for item in fonts:
        display.insert(END, item)

    def selectFont():
        global Font, textPad, fontSize
        Idx = display.curselection()[0]
        subWindow3.destroy()
        Font = fonts[Idx]
        textPad.configure(font=((Font, fontSize)))

    button = Button(subWindow3, text='선택', command = selectFont)
    button.pack(side=BOTTOM)
    subWindow3.mainloop()
    
def fontSizeSelect():
    global Font, textPad, fontSize
    fontSize = askinteger("폰트 크기", "값을 입력하세요(1~100)", minvalue=1, maxvalue=100)
    textPad.configure(font=((Font, fontSize)))

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

def featureCatch(event):
    global status, textPad, window, textLabel2, josas
    feature_list = []
    text = re.sub("|".join(josas), "", textPad.get(1.0, END))
    words = text.split()
    for word in words:
        for feature in feature_dict.keys():
            if word in feature_dict[feature]:
                feature_list.append(feature)
    if feature_list == []:
        textLabel2.configure(text="아직 뭔지 잘..ㅋㅋ..ㅎㅎ;ㅈㅅ!")
    else:
        textLabel2.configure(text="{}에 관한 리뷰이군욧~~~ 우효~!★".format(", ".join(feature_list)))

# ======= Global Variables

inText, outText = "", ""
Font = "Arial"; fontSize = 10
filename = ""
# ======= Korean Letters

onset = hgtk.letter.CHO
nucleus = hgtk.letter.JOONG
coda = hgtk.letter.JONG
josas = list(hgtk.josa.JOSAS.keys()) + ["도", "랑", "에", "에서"]

UNASP = {"ㄱ" : "ㄲ", "ㅋ" : "ㄲ", "ㅅ" : "ㄸ", "ㄷ" : "ㄸ", "ㅌ" : "ㄸ", "ㅂ" : "ㅃ", "ㅍ" : "ㅃ", "ㅅ" : "ㅆ", "ㅈ" : "ㅉ"}
ASP = {"ㅊ" : "ㅈㅎ","ㅋ" : "ㄱㅎ","ㅌ" : "ㄷㅎ","ㅍ" : "ㅂㅎ"}

vowelTran1 = {"ㅗ" : "ㅓ", "ㅓ" : "ㅗ", "ㅏ" : "ㅑ", "ㅓ" : "ㅕ", "ㅣ" : "ㅟ", "ㅐ" : "ㅔ", "ㅔ" : "ㅖ", "ㅟ" : "ㅢ", "ㅚ" : "ㅙ"}
consoTran1 = {letter : letter + "ㅇ" for letter in onset}  # 바보 -> 밥오

# ======= Language Model

model = gensim.models.Word2Vec.load("C:/ko/ko.bin")
features = ["인테리어", "시설", "교통"]
feature_dict = {f : [f] + [w for w, p in model.wv.most_similar(f, topn=30)] for f in features}
feature_dict.update({"위생":["위생"] + [w for w, p in model.wv.most_similar("청소", topn=30)]})
feature_dict.update({"서비스":["서비스"] + [w for w, p in model.wv.most_similar("친절", topn=30)]})

# ======= Main Code

window = Tk()
window.title("Reviewer's Text")
window.geometry("600x400")
textPad = Text(window)
textPad.insert("1.0", "", "a")

scrollbar = Scrollbar(window, jump = 1)
scrollbar.configure(command=textPad.yview)
scrollbar.pack(side=RIGHT, fill=Y, expand=NO)

status = Label(window, text="", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="열기", command=openText)
fileMenu.add_command(label="저장", command=saveText)
fileMenu.add_command(label="다른이름으로 저장", command=saveAsText)

editMenu = Menu(mainMenu)
mainMenu.add_cascade(label="편집", menu=editMenu)
editMenu.add_command(label="폰트", command=fontSelect)
editMenu.add_command(label="폰트 크기", command=fontSizeSelect)

# Keyboard Shorcuts
window.bind("<Control-o>", openCut)
window.bind("<Control-s>", saveCut)
window.bind("<Control-S>", saveAsCut)
window.bind("<Key>", countLetter)
window.bind("<space>", featureCatch)
window.bind("<BackSpace>", featureCatch)

transButton = Button(window, text="변환하기", command=selectOps)
transButton.pack(side=BOTTOM, fill=X)

textLabel2 = Message(window, text="아직 뭔지 잘..ㅋㅋ..ㅎㅎ;ㅈㅅ!", 
                        font=("나눔바른고딕 Light", 12), bg="#FFFFFF",
                        relief="groove", width=600)

textLabel2.pack(side=BOTTOM, fill=X)

textPad.pack()
window.mainloop()


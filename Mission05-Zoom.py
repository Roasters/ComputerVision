from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

def func_open():
    global photo
    filename = askopenfilename(parent=window, filetypes=(("GIF File", "*.gif;*.raw"),("All File", "*.*")))
    photo = PhotoImage(file=filename)
    pLabel.configure(image=photo)
    pLabel.image = photo

def func_exit():
    window.quit()
    window.destroy()

def zoom(x):
    global photo
    scale = askinteger("Scale", "Enter the Scale")
    if x == "in":
        photo = photo.zoom(scale, scale)
        pLabel.configure(image=photo)
        pLabel.image = photo
    else:
        photo = photo.subsample(scale, scale)
        pLabel.configure(image=photo)
        pLabel.image = photo

window = Tk()
window.geometry("400x400")
window.title("Viewing Artworks")

photo = PhotoImage()
pLabel = Label(window, image=photo)
pLabel.pack(expand=1, anchor=CENTER)

mainMenu = Menu(window)
window.config(menu=mainMenu)
fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open File", command=func_open)
fileMenu.add_command(label="Exit", command=func_exit)

zoomMenu = Menu(mainMenu)
mainMenu.add_cascade(label="Zoom", menu=zoomMenu)
zoomMenu.add_command(label="Zoom In", command=lambda: zoom("in"))
zoomMenu.add_command(label="Zoom Out", command=lambda: zoom("out"))

window.mainloop()
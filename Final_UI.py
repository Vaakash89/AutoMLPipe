from tkinter import *
from PIL import ImageTk,Image

def show_UI():
    root = Toplevel()
    image = Image.open("output.png")
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)
    label.image = photo
    label.grid(row=2, column=0)
    root.mainloop()

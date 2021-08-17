from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import tkinter as tk

final_split = 0.01

def build_UI(root, score, train_msg):
    train_msg.config(text = "Training Done")

    accuracy_lable = Label(root, text="Accuracy: "+str(score), font=("Arial", 12), anchor='w', width=30)
    accuracy_lable.grid(row=8, column=2, pady=10)

    image = Image.open("output.png")
    photo = ImageTk.PhotoImage(image, master=root)
    label_pic = Label(root, image=photo)
    label_pic.image = photo
    label_pic.grid(row=9, column=0)

def set_split(value):
    print(value)

def show_UI(score):
    print(score)
    root = Tk()
    root.geometry("700x700")

    current_value = tk.DoubleVar()

    progress = Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
    progress.grid(row=4, column=0, columnspan=3, padx=30, pady=20)

    train_msg = Label(root, text="Training in Progress!", font=("Arial", 15), width=30)
    train_msg.grid(row=7, column=1, columnspan=2, pady=10)

    import time
    progress['value']=20
    tk.Tk.update(root)
    time.sleep(1)
    progress['value']=50
    tk.Tk.update(root)
    time.sleep(1)
    progress['value']=80
    tk.Tk.update(root)
    time.sleep(1)
    progress['value']=100

    build_UI(root, score, train_msg)

    button_exit = Button(root, text='Exit',
                    command=root.destroy, width=30)
    button_exit.grid(row=6, column=0, columnspan=3, pady=10)
    root.mainloop()

    '''   
    root = TopLevel()
     #image = Image.open("output.png")
     #photo = ImageTk.PhotoImage(image)
 
     progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
 
     button = Button(root, text='Train Model',
                     command=lambda: bar(root, progress),
                     anchor='center', width=30)
     button.grid(row=1, columnspan=2)
     root.mainloop()
 
 
     label = Label(root, image=photo)
     label.image = photo
     label.grid(row=2, column=0)
    '''


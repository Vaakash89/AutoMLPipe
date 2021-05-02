from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

def build_UI(root, score):
    train_msg = Label(root, text="Training Done!", font=("Arial", 15), width=30)
    train_msg.grid(row=3, column=2, pady=10)

    accuracy_lable = Label(root, text="Accuracy: "+str(score), font=("Arial", 12), anchor='w', width=30)
    accuracy_lable.grid(row=4, column=2, pady=10)

    image = Image.open("output.png")
    photo = ImageTk.PhotoImage(image, master=root)
    label_pic = Label(root, image=photo)
    label_pic.image = photo
    label_pic.grid(row=5, column=0)

def bar(tk, progress, score):
    import time
    progress['value']=20
    tk.update_idletasks()
    time.sleep(1)
    progress['value']=50
    tk.update_idletasks()
    time.sleep(1)
    progress['value']=80
    tk.update_idletasks()
    time.sleep(1)
    progress['value']=100

    build_UI(tk, score)

def show_UI(score):
    print(score)
    root = Tk()
    root.geometry("700x700")

    progress = Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
    progress.grid(row=1, column=0, columnspan=3, padx=30, pady=20)

    button = Button(root, text='Generate Training Result',
                    command=lambda: bar(root, progress, score), width=30)
    button.grid(row=2, column=0, columnspan=3, pady=10)
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


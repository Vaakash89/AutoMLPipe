from tkinter import *
from tkinter import filedialog
from ml_operations import add
from tkinter import ttk

filename = ""
sel_ml_learning_val = ""
model = ""
sel_ml_class_val = ""
column_pred =""

def UploadAction(event=None):
    global filename
    filename = filedialog.askopenfilename()
    filename_label = Label(root, text=filename, font=("Arial", 8), anchor='w', justify=LEFT)
    filename_label.grid(row=2, column=1)
    return

def sel_ml_learning():
   global sel_ml_learning_val
   if str(var.get()) == "1":
       sel_ml_learning_val = "supervised"
       ml_learn_label = Label(root, text="ML Learning Classification:", font=("Arial", 15))
       ml_learn_label.grid(row=5)


       R1 = Radiobutton(root, text="Regression", variable=var_class, value=1, command=sel_ml_class, justify=LEFT)
       R1.grid(row=5, column=1)
       R2 = Radiobutton(root, text="Classification", variable=var_class, value=2, command=sel_ml_class, justify=LEFT)
       R2.grid(row=6, column=1)

   elif str(var.get()) == "2":
       sel_ml_learning_val = "unsupervised"
       ml_model_label = Label(root, text="Sorry, We dont support Unsupervised Learning yet!", font=("Arial", 8))
       ml_model_label.grid(row=7, column=1)

def sel_ml_class():
   global sel_ml_class_val
   if str(var_class.get()) == "1":
       sel_ml_class_val = "regression"
       ml_model_label = Label(root, text="ML Model:", font=("Arial", 15))
       ml_model_label.grid(row=7)

       clicked = StringVar()
       clicked.set("Linear Regression")

       options = [
           "Linear Regression",
           "Logistic Regression"
       ]

       ml_model_drop = OptionMenu(root, clicked, *options, command=set_model)
       ml_model_drop.grid(row=7, column=1)
   elif str(var_class.get()) == "2":
       sel_ml_class_val = "classification"
       ml_model_label = Label(root, text="Sorry, We dont support Unsupervised Learning yet!", font=("Arial", 8))
       ml_model_label.grid(row=7, column=1)

def set_model(value):
    global model
    model = value
    col_label = Label(root, text="Choose the Prediction Label:", font=("Arial", 8))
    col_label.grid(row=8)

    pred_col = StringVar()
    pred_col.set("Choose column")

    column_names = [
        "Column1",
        "Column2"
    ]

    ml_model_drop = OptionMenu(root, pred_col, *column_names, command=set_column)
    ml_model_drop.grid(row=8, column=1)

def set_column(value):
    global column_pred
    column_pred = value


root = Tk()
root.geometry("700x1000")
line_dummy = Label(root, text="---------------------------------------------------------------", font=("Arial", 25))
line_dummy.grid(row=0, columnspan=4)

import_label_file = Label(root, text="Upload File:", font=("Arial", 15))
import_label_file.grid(row=1)

button = Button(root, text='Select File', command=UploadAction, anchor='n')
button.grid(row=1, column=1)

#ML Methodology

ml_learn_label = Label(root, text="ML Learning Algorithm:", font=("Arial", 15))
ml_learn_label.grid(row=3)

var = IntVar()
var_class = IntVar()
R1 = Radiobutton(root, text="Supervised Learning", variable=var, value=1, command=sel_ml_learning, justify=LEFT)
R1.grid(row=3, column=1)
R2 = Radiobutton(root, text="Unsupervised Learning", variable=var, value=2, command=sel_ml_learning, justify=LEFT)
R2.grid(row=4, column=1)

button = Button(root, text='Train Model', command=lambda: add(filename, sel_ml_learning_val, sel_ml_class_val, model, column_pred), anchor='n')
button.grid(row=10, column=1, columnspan=3)

root.mainloop()
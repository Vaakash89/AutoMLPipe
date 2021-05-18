from tkinter import *
from tkinter import filedialog
from ml_operations import add
import tkinter as tk
import csv

filename = ""
sel_ml_learning_val = ""
model = ""
sel_ml_class_val = ""
columns_name_list = []
column_pred = ""


def UploadAction(event=None):
    global filename
    global columns_name_list
    filename = filedialog.askopenfilename()
    filename_label = Label(root, text=filename, font=("Arial", 7), justify=LEFT, anchor="w", width=40)
    filename_label.grid(row=2, column=1, padx=30)
    with open(filename, "r") as f:
        reader = csv.reader(f)
        columns_name_list = next(reader)
    return


def sel_ml_learning():
    global sel_ml_learning_val
    if str(var.get()) == "1":
        sel_ml_learning_val = "supervised"
        ml_learn_label = Label(root, text="ML Learning Classification:", font=("Arial", 13), anchor="e", width=30)
        ml_learn_label.grid(row=5)

        R1 = Radiobutton(root, text="Regression", variable=var_class, value=1, command=sel_ml_class, justify=LEFT)
        R1.grid(row=5, column=1, padx=30, sticky=tk.W)
        R2 = Radiobutton(root, text="Classification", variable=var_class, value=2, command=sel_ml_class, justify=LEFT)
        R2.grid(row=6, column=1, padx=30, sticky=tk.W)

    elif str(var.get()) == "2":
        sel_ml_learning_val = "unsupervised"
        ml_model_label = Label(root, text="Sorry, We dont support Unsupervised Learning yet!", font=("Arial", 8))
        ml_model_label.grid(row=7, column=1)


def sel_ml_class():
    global sel_ml_class_val
    dummy_label.grid(row=7, column=1, padx=30, sticky=tk.W)
    if str(var_class.get()) == "1":
        sel_ml_class_val = "regression"
        clicked = StringVar()
        clicked.set("Choose one")

        options = [
            "Linear Regression",
            "XGBoost"
        ]

        ml_model_drop = OptionMenu(root, clicked, *options, command=set_model)
        ml_model_drop.grid(row=7, column=1, padx=30, sticky=tk.W)

    elif str(var_class.get()) == "2":
        sel_ml_class_val = "classification"
        clicked = StringVar()
        clicked.set("Choose one")

        options = [
            "Logistic Regression",
            "Naive Bayes"
        ]

        ml_model_drop = OptionMenu(root, clicked, *options, command=set_model)
        ml_model_drop.grid(row=7, column=1, padx=30, sticky=tk.W)

    ml_model_label = Label(root, text="ML Model:", font=("Arial", 13), anchor="e", width=30)
    ml_model_label.grid(row=7, pady=20)




def set_model(value):
    global model
    model = value
    col_label = Label(root, text="Choose the Prediction Label:", font=("Arial", 13), anchor="e", width=30)
    col_label.grid(row=8)

    dummy_label.grid(row=8, column=1, padx=30, sticky=tk.W)
    pred_col = StringVar()
    pred_col.set("Choose column")

    column_names = columns_name_list

    ml_model_drop = OptionMenu(root, pred_col, *column_names, command=set_column)
    ml_model_drop.grid(row=8, column=1, padx=30, sticky=tk.W)


def set_column(value):
    global column_pred
    column_pred = value


root = Tk()
root.geometry("700x1000")

dummy_label = Label(root, text="")

line_dummy = Label(root, text="---------------------------------------------------------------", font=("Arial", 15), anchor="e", width=30)
line_dummy.grid(row=0, columnspan=4)

import_label_file = Label(root, text="Upload File:", font=("Arial", 13), anchor="e", width=30)
import_label_file.grid(row=1, pady=20)

button = Button(root, text='Select File', command=UploadAction, anchor='center', width=30, justify=CENTER)
button.grid(row=1, column=1, padx=30)

#ML Methodology

ml_learn_label = Label(root, text="ML Learning Algorithm:", font=("Arial", 13), anchor="e", width=30)
ml_learn_label.grid(row=3)

var = IntVar()
var_class = IntVar()
R1 = Radiobutton(root, text="Supervised Learning", variable=var, value=1, command=sel_ml_learning, anchor="w")
R1.grid(row=3, column=1, padx=30, sticky=tk.W)
R2 = Radiobutton(root, text="Unsupervised Learning", variable=var, value=2, command=sel_ml_learning, anchor="w")
R2.grid(row=4, column=1, padx=30, sticky=tk.W)

button = Button(root, text='Train Model', command=lambda: add(filename, sel_ml_learning_val, sel_ml_class_val, model, column_pred, root),  anchor='center', width=30)
button.grid(row=15, column=1, columnspan=3, pady=30, sticky=tk.W)

root.mainloop()
from tkinter import *
from tkinter import filedialog
from ml_operations import add
import tkinter as tk
import csv
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import ImageTk, Image
from sklearn import preprocessing

filename = ""
sel_ml_learning_val = ""
model = ""
sel_ml_class_val = ""
columns_name_list = []
column_pred = ""
split = ""


def UploadAction(event=None):
    global filename
    global columns_name_list
    filename = filedialog.askopenfilename()
    filename_label = Label(root, text=filename, font=("Arial", 7), justify=LEFT, anchor="w", width=40)
    filename_label.grid(row=4, column=1, padx=30)
    with open(filename, "r") as f:
        reader = csv.reader(f)
        columns_name_list = next(reader)
    return

def UploadModelAction(event=None):
    global filename
    global columns_name_list
    filename = filename + ',' + filedialog.askopenfilename()
    filename_label = Label(root, text=filename, font=("Arial", 7), justify=LEFT, anchor="w", width=40)
    filename_label.grid(row=4, column=1, padx=30)
    return


def sel_ml_learning():
    global sel_ml_learning_val
    if str(var.get()) == "1":
        sel_ml_learning_val = "supervised"
        ml_learn_label = Label(root, text="ML Learning Classification:", font=("Arial", 13), anchor="e", width=30)
        ml_learn_label.grid(row=7)

        R1 = Radiobutton(root, text="Regression", variable=var_class, value=1, command=sel_ml_class, justify=LEFT)
        R1.grid(row=7, column=1, padx=30, sticky=tk.W)
        R2 = Radiobutton(root, text="Classification", variable=var_class, value=2, command=sel_ml_class, justify=LEFT)
        R2.grid(row=8, column=1, padx=30, sticky=tk.W)

    elif str(var.get()) == "2":
        sel_ml_learning_val = "unsupervised"
        #ml_model_label = Label(root, text="Sorry, We dont support Unsupervised Learning yet!", font=("Arial", 8))
        #ml_model_label.grid(row=9, column=1)
        ml_learn_label = Label(root, text="Type of Unsupervised:", font=("Arial", 13), anchor="e", width=30)
        ml_learn_label.grid(row=7)

        R1 = Radiobutton(root, text="Clustering", variable=var_class, value=1, command=sel_ml_class, justify=LEFT)
        R1.grid(row=7, column=1, padx=30, sticky=tk.W)


def sel_ml_class():
    global sel_ml_class_val
    dummy_label.grid(row=9, column=1, padx=30, sticky=tk.W)
    if(sel_ml_learning_val == "supervised"):
        if str(var_class.get()) == "1":
            sel_ml_class_val = "regression"
            clicked = StringVar()
            clicked.set("Choose one")

            options = [
                "Linear Regression",
                "XGBoost"
            ]
        elif str(var_class.get()) == "2":
            sel_ml_class_val = "classification"
            clicked = StringVar()
            clicked.set("Choose one")

            options = [
                "Logistic Regression",
                "SGDClassifier"
            ]

        ml_model_drop = OptionMenu(root, clicked, *options, command=set_model)
        ml_model_drop.grid(row=9, column=1, padx=30, sticky=tk.W)

    if (sel_ml_learning_val == "unsupervised"):
        if str(var_class.get()) == "1":
            sel_ml_class_val = "clustering"
            clicked = StringVar()
            clicked.set("Choose one")

            options = [
                "Hierarchical"
            ]
        ml_model_drop = OptionMenu(root, clicked, *options, command=set_model)
        ml_model_drop.grid(row=9, column=1, padx=30, sticky=tk.W)
    ml_model_label = Label(root, text="ML Model:", font=("Arial", 13), anchor="e", width=30)
    ml_model_label.grid(row=9, pady=20)




def set_model(value):
    global model
    model = value
    if(sel_ml_learning_val == "supervised"):
        col_label = Label(root, text="Choose the Prediction Label:", font=("Arial", 13), anchor="e", width=30)
        col_label.grid(row=10)

        dummy_label.grid(row=10, column=1, padx=30, sticky=tk.W)
        pred_col = StringVar()
        pred_col.set("Choose column")

        column_names = columns_name_list

        ml_model_drop = OptionMenu(root, pred_col, *column_names, command=set_column)
        ml_model_drop.grid(row=10, column=1, padx=30, sticky=tk.W)

    if (sel_ml_learning_val == "unsupervised"):
        col_label = Label(root, text="Choose number of clusters:", font=("Arial", 13), anchor="e", width=30)
        col_label.grid(row=10)

        dummy_label.grid(row=10, column=1, padx=30, sticky=tk.W)
        pred_col = StringVar()
        pred_col.set("Choose clusters")

        options = [
            "1","2","3","4","5","6","7","8","9","10"
        ]

        ml_model_drop = OptionMenu(root, pred_col, *options, command=set_column)
        ml_model_drop.grid(row=10, column=1, padx=30, sticky=tk.W)

        button_dendogram = Button(root, text='Check Elbow Curve', command=lambda: createdendogram(filename), anchor='e', width=15)
        button_dendogram.grid(row=11, column=1, padx=30, sticky=tk.W)

def createdendogram(filename):
    newWindow = Toplevel(root)
    newWindow.title("Dendogram")
    newWindow.geometry("600x400")

    df = pd.read_csv(filename)
    le = preprocessing.LabelEncoder()
    cat_features = [x for x in df.columns if df[x].dtype == "object"]
    if len(cat_features) > 0:
        for i in cat_features:
            df[i] = le.fit_transform(df[i])

    distortions = []
    K = range(1, 10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k)
        kmeanModel.fit(df)
        distortions.append(kmeanModel.inertia_)
    plt.figure(figsize=(6, 3))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.title('The Elbow Graph')
    plt.savefig("elbow.png")

    image = Image.open("elbow.png")
    photo = ImageTk.PhotoImage(image, master=newWindow)
    label_pic = Label(newWindow, image=photo)
    label_pic.image = photo
    label_pic.grid(row=1, column=0, padx=10)

def set_column(value):
    global column_pred
    column_pred = value
    if(sel_ml_learning_val == "supervised"):
        train_split_label = Label(root, text="Enter Test Split:", font=("Arial", 13), anchor="e", width=30)
        train_split_label.grid(row=16)

        dummy_label.grid(row=16, column=1, padx=30, sticky=tk.W)
        options = [
            "0.1",
            "0.2",
            "0.3",
            "0.4",
            "0.5",
            "0.6",
            "0.7",
            "0.8",
            "0.9",
        ]
        clicked = StringVar()
        clicked.set("Choose one")
        train_split = OptionMenu(root, clicked, *options, command=set_split)
        train_split.grid(row=16, column=1, padx=30, sticky=tk.W)

    if(sel_ml_learning_val == "unsupervised"):
        print("Aakash")

def set_split(value):
    global split
    split = value

root = Tk()
root.geometry("700x1000")

dummy_label = Label(root, text="")

line_dummy = Label(root, text="---------------------------------------------------------------", font=("Arial", 15), anchor="e", width=30)
line_dummy.grid(row=0, columnspan=4)

import_label_file = Label(root, text="Train new model:", font=("Arial", 13), anchor="e", width=30)
import_label_file.grid(row=1, pady=20)

button = Button(root, text='Upload File', command=UploadAction, anchor='center', width=30, justify=CENTER)
button.grid(row=1, column=1, padx=30)

retrain_model_label = Label(root, text="Retrain existing Model(optional):", font=("Arial", 13), anchor="e", width=30)
retrain_model_label.grid(row=3, pady=20)

button_retrain= Button(root, text='Upload Old Model', command=UploadModelAction, anchor='center', width=30, justify=CENTER)
button_retrain.grid(row=3, column=1, padx=30)

#ML Methodology

ml_learn_label = Label(root, text="ML Learning Algorithm:", font=("Arial", 13), anchor="e", width=30)
ml_learn_label.grid(row=5)

var = IntVar()
var_class = IntVar()
R1 = Radiobutton(root, text="Supervised Learning", variable=var, value=1, command=sel_ml_learning, anchor="w")
R1.grid(row=5, column=1, padx=30, sticky=tk.W)
R2 = Radiobutton(root, text="Unsupervised Learning", variable=var, value=2, command=sel_ml_learning, anchor="w")
R2.grid(row=6, column=1, padx=30, sticky=tk.W)

button = Button(root, text='Train Model', command=lambda: add(filename, sel_ml_learning_val, sel_ml_class_val, model, column_pred, split, root),  anchor='center', width=30)
button.grid(row=17, column=1, columnspan=3, pady=30, sticky=tk.W)



root.mainloop()
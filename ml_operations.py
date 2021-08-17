import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression, SGDClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
import pickle
from Final_UI import show_UI
import numpy
import xgboost as xgb

def download_data(filename):
    df = pd.read_csv(filename)
    return df

def create_model_object(algo):
    if algo == "Logistic Regression":
        model = LogisticRegression()
    elif algo == "Linear Regression":
        model = LinearRegression()
    elif algo == "SGDClassifier":
        model = SGDClassifier()
    elif algo == "XGBoost":
        model = xgb.XGBRegressor(objective="reg:linear", random_state=42)
    return model

def fit_model(algo, model, x_train, y_train):
    if algo == "SGDClassifier":
        print("hello aakash")
        model.partial_fit(x_train, y_train, classes=numpy.unique(y_train))
    else:
        model.fit(x_train, y_train)
    return model

def save_model(model):
    pickle.dump(model, open("model.pkl", 'wb'))

def add(filename, sel_ml_learning_val, sel_ml_class_val, algo, column_pred, split, root):

    root.destroy()
    files = filename.split(',')
    file_name = files[0]
    if(len(files) == 2):
        model_file = files[1]
    #Download Data
    df = download_data(file_name)
    X = df.drop(column_pred, axis=1)
    y = df[column_pred]

    #Split Data
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=float(split), random_state=0)

    #Create Model
    if (len(files) == 2):
        model = pickle.load(open(model_file, 'rb'))
    else:
        model = create_model_object(algo)

    #Fit Model
    model = fit_model(algo, model, x_train, y_train)

    score = model.score(x_test, y_test)
    
    #Get Prediction
    predictions = model.predict(x_test)

    if algo == "Logistic Regression" or "SGDClassifier":
        # Confusion Matrix
        print("aakash Log")
        cm = metrics.confusion_matrix(y_test, predictions)
        plt.figure(figsize=(3, 3))
        plt.rcParams.update({'font.size': 5})
        sns_plot = sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square=True, cmap='Blues_r')
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')
        all_sample_title = 'Accuracy Score: {0}'.format(score)
        plt.title(all_sample_title, size=8)
        plt.savefig("output.png")
    elif algo == "Linear Regression" or "XGBoost":
        print("aakash Lin")
        plt.figure(figsize=(3, 3))
        plt.rcParams.update({'font.size': 5})
        plt.plot(range(1, len(y_train) + 1), y_train, color="red", label="Real Values")
        plt.plot(range(1, len(y_train) + 1), model.predict(x_train), color="green",
                                  label="Predicted Values")
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig("output.png")
    #Save Model
    save_model(model)

    show_UI(score)

    print("Done")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
import pickle
from Final_UI import show_UI

def download_data(filename):
    df = pd.read_csv(filename)
    return df

def create_model_object(algo):
    if algo == "Logistic Regression":
        model = LogisticRegression()
    elif algo == "Linear Regression":
        model = LinearRegression()
    return model

def fit_model(model, x_train, y_train):
    model.fit(x_train, y_train)
    return model

def save_model(model):
    pickle.dump(model, open("model.pkl", 'wb'))

def add(filename, sel_ml_learning_val, sel_ml_class_val, algo, column_pred, root):

    root.destroy()
    #Download Data
    df = download_data(filename)
    X = df.drop(column_pred, axis=1)
    y = df[column_pred]

    #Split Data
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    #Create Model
    model = create_model_object(algo)

    #Fit Model
    model = fit_model(model, x_train, y_train)

    score = model.score(x_test, y_test)

    #Get Prediction
    predictions = model.predict(x_test)

    if algo == "Logistic Regression":
        # Confusion Matrix
        cm = metrics.confusion_matrix(y_test, predictions)
        plt.figure(figsize=(3, 3))
        plt.rcParams.update({'font.size': 5})
        sns_plot = sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square=True, cmap='Blues_r')
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')
        all_sample_title = 'Accuracy Score: {0}'.format(score)
        plt.title(all_sample_title, size=8)
        plt.savefig("output.png")
    elif algo == "Linear Regression":
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
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
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from sklearn import preprocessing

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
        model.partial_fit(x_train, y_train, classes=numpy.unique(y_train))
    else:
        model.fit(x_train, y_train)
    return model

def save_model(model):
    pickle.dump(model, open("model.pkl", 'wb'))

def add(filename, sel_ml_learning_val, sel_ml_class_val, algo, column_pred, split, root):
    print(algo)
    root.destroy()
    files = filename.split(',')
    file_name = files[0]
    if(len(files) == 2):
        model_file = files[1]
    #Download Data
    df = download_data(file_name)
    le = preprocessing.LabelEncoder()
    cat_features = [x for x in df.columns if df[x].dtype == "object"]
    if len(cat_features) > 0:
        for i in cat_features:
            df[i] = le.fit_transform(df[i])

    if (sel_ml_learning_val == "supervised"):

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
        print(algo)
        if algo == "Logistic Regression" or algo == "SGDClassifier":
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
        elif algo == "Linear Regression" or algo == "XGBoost":
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
        show_UI(sel_ml_learning_val, score)

    if(sel_ml_learning_val == "unsupervised"):
        cluster = AgglomerativeClustering(n_clusters=int(column_pred), affinity='euclidean', linkage='ward')
        cluster_values = cluster.fit_predict(df)
        df["cluster"] = cluster_values
        df.to_csv('clusters.csv')

        plt.figure(figsize=(3, 3))
        plt.scatter(df.iloc[:, 0], df.iloc[:, 1], c=cluster.labels_, cmap='rainbow')
        plt.savefig("output.png")
        save_model(cluster)
        show_UI(sel_ml_learning_val, 0.5)

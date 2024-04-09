from sklearn.svm import OneClassSVM
import pandas as pd
#do the dataframe country and financial
#df.to_csv("outliers.csv")

def detect_outliers_country(data_frame,name):
    #since we don't know what database gets passed in we might need to do preprocessing.filter_data(df)
    df = data_frame.copy()
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df = df.drop(columns=['code', 'country', 'interpolated', 'date'])
    X = df.to_numpy()  

    # Initialize One-Class SVM
    oc_svm = OneClassSVM(nu=0.05, kernel='rbf', gamma='scale')  # nu is an upper bound on the fraction of training errors rdf = radial basis function and gamma = scale (1/(n_features * X.var()))

    # Fit the model
    oc_svm.fit(X)

    # Predict outliers (-1 for outliers, 1 for inliers)
    df['outlier'] = oc_svm.predict(X)
    outliers = df[df['outlier'] == -1]
    outliers.to_csv(name)

def detect_outliers_fiancial(data_frame,name):
    df = data_frame.copy()
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df = df.drop(columns=['ticker', 'date','sector'])
    X = df.to_numpy()  

    # Initialize One-Class SVM
    oc_svm = OneClassSVM(nu=0.05, kernel='rbf', gamma='scale')  # nu is an upper bound on the fraction of training errors

    # Fit the model
    oc_svm.fit(X)

    # Predict outliers (-1 for outliers, 1 for inliers)
    df['outlier'] = oc_svm.predict(X)
    outliers = df[df['outlier'] == -1]
    outliers.to_csv(name)

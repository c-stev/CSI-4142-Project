import time
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import preprocessing
import pandas as pd


# Combines all staged dataframes into one "super" dataframe, and splits it for the classification task
def split_data():
    # Getting all pre-processed dataframes
    df_country, df_company, df_date, df_financial, df_fact = preprocessing.get_processed_data()
    # Merging all dataframes
    df = df_fact.merge(df_country, on='country_id').drop(columns=['year', 'month', 'day', 'interpolated',
                                                                  'country_Ireland', 'country_Switzerland',
                                                                  'country_United Kingdom', 'country_United States'])
    df = df.merge(df_company, on='company_id').drop(columns=['ticker'])
    df = df.merge(df_financial, on='financial_data_id').drop(columns=['year', 'month', 'day'])
    df = df.merge(df_date, on='date_id').drop(columns=['weekday'])
    # Adding a new column to serve as our target variable (will be stored numerically)
    df['target'] = (df['open'] < df['close']).astype(int)
    # Adding some lag columns since model is too accurate with current date (also unrealistic)
    df['lag_1_close'] = df['close'].shift(1)
    df['lag_1_high'] = df['high'].shift(1)
    df['lag_1_low'] = df['low'].shift(1)
    df['lag_1_volume'] = df['volume'].shift(1)
    df['lag_1_returns'] = df['returns'].shift(1)
    df['lag_1_volatility'] = df['volatility'].shift(1)
    # Removing the current-day cheat code data from the row
    df = df.drop(['close', 'high', 'low', 'volume', 'returns', 'volatility'], axis=1)
    # Since the very last row is now null, we just remove it
    df = df.dropna()
    # Splitting up the data by company (since mixing companies would only detract from accuracy)
    grouped = df.groupby('ticker')
    train_dfs, test_dfs, validation_dfs = [], [], []
    for ticker, group_df in grouped:
        total_rows = len(group_df)
        train_end = int(total_rows * 0.7)
        validation_end = int(total_rows * 0.9)
        # Splitting up the data by date (since date transitions are crucial in this predictive model)
        temp_train_df = group_df.iloc[:train_end]
        temp_validation_df = group_df.iloc[train_end:validation_end]
        temp_test_df = group_df.iloc[validation_end:]
        train_dfs.append(temp_train_df)
        test_dfs.append(temp_test_df)
        validation_dfs.append(temp_validation_df)
    train_df = pd.concat(train_dfs, axis=0, ignore_index=True)
    test_df = pd.concat(test_dfs, axis=0, ignore_index=True)
    validation_df = pd.concat(validation_dfs, axis=0, ignore_index=True)
    return train_df, test_df, validation_df


def construct_models():
    train_df, test_df, validation_df = split_data()
    # Preparing the training sets
    x_train = train_df.drop('target', axis=1)
    y_train = train_df['target']
    # Preparing the target sets
    x_test = test_df.drop('target', axis=1)
    y_test = test_df['target']
    # Preparing the validation sets
    x_validation = validation_df.drop('target', axis=1)
    y_validation = validation_df['target']
    # Running the classification algorithms
    decision_tree(x_train, y_train, x_test, y_test, x_validation, y_validation)
    gradient_boosting(x_train, y_train, x_test, y_test, x_validation, y_validation)
    random_forest(x_train, y_train, x_test, y_test, x_validation, y_validation)


def decision_tree(x_train, y_train, x_test, y_test, x_validation, y_validation):
    print("Training Decision Tree...")
    classifier = DecisionTreeClassifier()
    start_time = time.time()
    classifier.fit(x_train, y_train)
    training_time = time.time() - start_time
    print("Evaluating Decision Tree on validation data...")
    prediction_validation = classifier.predict(x_validation)
    accuracy_validation = accuracy_score(y_validation, prediction_validation)
    precision_validation = precision_score(y_validation, prediction_validation, zero_division=0)
    recall_validation = recall_score(y_validation, prediction_validation, zero_division=0)
    # Displaying the validation data set's results
    print("Decision Tree Validation Accuracy: " + str(round(accuracy_validation, 4)))
    print("Decision Tree Validation Precision: " + str(round(precision_validation, 4)))
    print("Decision Tree Validation Recall: " + str(round(recall_validation, 4)))
    print("Evaluating Decision Tree on test data...")
    prediction_test = classifier.predict(x_test)
    accuracy_test = accuracy_score(y_test, prediction_test)
    precision_test = precision_score(y_test, prediction_test, zero_division=0)
    recall_test = recall_score(y_test, prediction_test, zero_division=0)
    # Displaying the test data set's results
    print("Decision Tree Test Accuracy: " + str(round(accuracy_test, 4)))
    print("Decision Tree Test Precision: " + str(round(precision_test, 4)))
    print("Decision Tree Test Recall: " + str(round(recall_test, 4)))
    print("Decision Tree Training Time: " + str(round(training_time, 4)))
    print("\n")


def gradient_boosting(x_train, y_train, x_test, y_test, x_validation, y_validation):
    print("Training Gradient Boosting...")
    classifier = GradientBoostingClassifier()
    start_time = time.time()
    classifier.fit(x_train, y_train)
    training_time = time.time() - start_time
    print("Evaluating Gradient Boosting on validation data...")
    prediction_validation = classifier.predict(x_validation)
    accuracy_validation = accuracy_score(y_validation, prediction_validation)
    precision_validation = precision_score(y_validation, prediction_validation, zero_division=0)
    recall_validation = recall_score(y_validation, prediction_validation, zero_division=0)
    # Displaying the validation data set's results
    print("Gradient Boosting Validation Accuracy: " + str(round(accuracy_validation, 4)))
    print("Gradient Boosting Validation Precision: " + str(round(precision_validation, 4)))
    print("Gradient Boosting Validation Recall: " + str(round(recall_validation, 4)))
    print("Evaluating Gradient Boosting on test data...")
    prediction_test = classifier.predict(x_test)
    accuracy_test = accuracy_score(y_test, prediction_test)
    precision_test = precision_score(y_test, prediction_test, zero_division=0)
    recall_test = recall_score(y_test, prediction_test, zero_division=0)
    # Displaying the test data set's results
    print("Gradient Boosting Test Accuracy: " + str(round(accuracy_test, 4)))
    print("Gradient Boosting Test Precision: " + str(round(precision_test, 4)))
    print("Gradient Boosting Test Recall: " + str(round(recall_test, 4)))
    print("Gradient Boosting Training Time: " + str(round(training_time, 4)))
    print("\n")


def random_forest(x_train, y_train, x_test, y_test, x_validation, y_validation):
    print("Training Random Forest...")
    classifier = RandomForestClassifier()
    start_time = time.time()
    classifier.fit(x_train, y_train)
    training_time = time.time() - start_time
    print("Evaluating Random Forest on validation data...")
    prediction_validation = classifier.predict(x_validation)
    accuracy_validation = accuracy_score(y_validation, prediction_validation)
    precision_validation = precision_score(y_validation, prediction_validation, zero_division=0)
    recall_validation = recall_score(y_validation, prediction_validation, zero_division=0)
    # Displaying the validation data set's results
    print("Random Forest Validation Accuracy: " + str(round(accuracy_validation, 4)))
    print("Random Forest Validation Precision: " + str(round(precision_validation, 4)))
    print("Random Forest Validation Recall: " + str(round(recall_validation, 4)))
    print("Evaluating Random Forest on test data...")
    prediction_test = classifier.predict(x_test)
    accuracy_test = accuracy_score(y_test, prediction_test)
    precision_test = precision_score(y_test, prediction_test, zero_division=0)
    recall_test = recall_score(y_test, prediction_test, zero_division=0)
    # Displaying the test data set's results
    print("Random Forest Test Accuracy: " + str(round(accuracy_test, 4)))
    print("Random Forest Test Precision: " + str(round(precision_test, 4)))
    print("Random Forest Test Recall: " + str(round(recall_test, 4)))
    print("Random Forest Training Time: " + str(round(training_time, 4)))
    print("\n")


construct_models()

# Imports

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


class EmailDetection:
    def __init__(self, data_path: str):
        # Load the dataset
        raw_mail_data = pd.read_csv(data_path)
        
        # Replace null values with empty strings
        self.mail_data = raw_mail_data.where((pd.notnull(raw_mail_data)), '')

        # Encode labels: spam as 0, ham as 1
        self.mail_data.loc[self.mail_data['Category'] == 'spam', 'Category'] = 0
        self.mail_data.loc[self.mail_data['Category'] == 'ham', 'Category'] = 1

        # Separate the dataset into features and labels
        X = self.mail_data['Message']
        Y = self.mail_data['Category'].astype('int')

        # Split the data into training and testing sets
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)

        # Initialize the TfidfVectorizer
        self.feature_extraction = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)

        # Transform the text data into feature vectors
        self.X_train_features = self.feature_extraction.fit_transform(self.X_train)
        self.X_test_features = self.feature_extraction.transform(self.X_test)

        # Initialize and train the Logistic Regression model
        self.model = LogisticRegression()
        self.model.fit(self.X_train_features, self.Y_train)

    def get_training_accuracy(self) -> float:
        # Predict on training data and calculate accuracy
        predictions = self.model.predict(self.X_train_features)
        accuracy = accuracy_score(self.Y_train, predictions)
        return accuracy * 100

    def get_testing_accuracy(self) -> float:
        # Predict on test data and calculate accuracy
        predictions = self.model.predict(self.X_test_features)
        accuracy = accuracy_score(self.Y_test, predictions)
        return accuracy * 100

    def is_phishing(self, email_message: str) -> bool:
        # Convert the input email message to feature vectors
        input_data_features = self.feature_extraction.transform([email_message])
        
        # Make a prediction
        prediction = self.model.predict(input_data_features)
        
        # Return True for phishing (0) and False for good mail (1)
        return prediction[0] == 0

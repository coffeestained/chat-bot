
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from threading import Lock
import numpy as np

class CustomModel:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
        self.lock = Lock()

    def update_model(self, messages, labels):
        with self.lock:
            X = self.vectorizer.fit_transform(messages)
            self.model.partial_fit(X, labels, classes=np.unique(labels))

    def predict(self, message):
        with self.lock:
            X = self.vectorizer.transform([message])
            return self.model.predict(X)

custom_model = CustomModel()

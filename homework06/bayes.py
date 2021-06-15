from collections import defaultdict
from math import log
import csv
import string


class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.dict = defaultdict(lambda: defaultdict(lambda: 0))
        self.uwdict = defaultdict(lambda: False)
        self.uw = 0
        self.dictall = defaultdict(lambda: 0)
        self.classes = defaultdict(lambda: 0)
        self.n = 0
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.n += len(X)
        for n in range(0, len(X)):
            x = X[n]
            c = y[n]
            self.classes[c] += 1
            for i in str(x).split():
                self.dict[i][c] += 1
                self.dictall[c] += 1
                if self.uwdict[i] is False:
                    self.uwdict[i] = True
                    self.uw += 1

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        f = None
        C = None
        c: str
        for c in self.classes.keys():
            t = log(self.classes[c] / self.n)
            for x in X.split():
                if self.uwdict[x] is True:
                    t += log((self.dict[x][c] + self.alpha) / (self.dictall[c] + self.alpha * self.uw))
            if f is None:
                f = t
                C = c
            elif t >= f:
                f = t
                C = c
        return C, f

    def score(self, X_test, y_test):
        n = 0
        for n1 in range(0, len(X_test)):
            x, y = X_test[n1], y_test[n1]
            if self.predict(x) == y:
                n += 1
        return n / len(X_test)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()

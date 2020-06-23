import numpy as np
import cv2
import glob
import time
import sys
import os
from sklearn.model_selection import train_test_split

class neuralnetwork(object):
    def __init__(self):
        self.model = None

    def loadData(self, inputSize, path):
        x = np.empty([0, inputSize])
        y = np.empty([0, 4])
        training_data = glob.glob(path)

        if not training_data:
            sys.exit()

        for file in training_data:
            with np.load(file) as data:
                train = data['train']
                train_labels = data['train_labels']
            x = np.vstack((x, train))
            y = np.vstack((y, train_labels))

        print("image", x.shape)
        print("labels", y.shape)

        x = x / 255.0
        return train_test_split(x, y, test_size = 0.3, shuffle = False)

    def create(self, layer_sizes):
        self.model = cv2.ml.ANN_MLP_create()
        self.model.setLayerSizes(np.int32(layer_sizes))
        self.model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
        self.model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)
        self.model.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 0.01))

    def train(self, x, y):
        start = time.time()

        print("Training ...")
        self.model.train(np.float32(x), cv2.ml.ROW_SAMPLE, np.float32(y))

        # set end time
        end = time.time()
        print("Training duration: %.2fs" % (end - start))

    def evaluate(self, x, y):
        ret, resp = self.model.predict(x)
        prediction = resp.argmax(-1)
        true_labels = y.argmax(-1)
        accuracy = np.mean(prediction == true_labels)
        return accuracy

    def save_model(self, path):
        directory = "saved_model"
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.model.save(path)
        print("Model saved to: " + "'" + path + "'")

    def load_model(self, path):
        if not os.path.exists(path):
            print("Model does not exist, exit")
            sys.exit()
        self.model = cv2.ml.ANN_MLP_load(path)

    def predict(self, x):
        resp = None
        try:
            ret, resp = self.model.predict(x)
        except Exception as e:
            print(e)
        return resp.argmax(-1)

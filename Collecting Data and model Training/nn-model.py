import numpy as np
import keras
import glob
import time
import sys
import os
import sklearn

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

    def create(self, layer_sizes):
        self.model = keras.sequential()
        self.model.add()
        self.model

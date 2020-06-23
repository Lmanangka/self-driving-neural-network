import numpy as np
import glob

training_data = glob.glob("training_data/*.npz")

for file in training_data:
    with np.load(file) as data:
        train = data['train']
        labels = data['train_labels']
    # x = print("x= ", train)
    y = print("y= ", labels)
    # z = train / 255.0
    # norm = print("norm= ", z)

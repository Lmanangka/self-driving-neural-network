from nn_model import neuralnetwork as nn

inputSize = 120 * 320
path = "training_data/*.npz"

x_train, x_valid, y_train, y_valid = nn.loadData(inputSize, path)

layer_sizes = [inputSize, 32, 4]
# nn = neuralnetwork()
nn.create(layer_sizes)
nn.train(x_train, y_train)

train_accuracy = nn.evaluate(x_train, y_train)
print("Train accuracy: ", "{0:.2f}%".format(train_accuracy * 100))

validation_accuracy = nn.evaluate(x_valid, y_valid)
print("Validation accuracy: ", "{0:.2f}%".format(validation_accuracy * 100))

model_path = "saved_model/nn_model.xml"
nn.save_model(model_path)

from keras.models import Sequential
from keras.layers import Dense

class Model:
    def __init__(self, input_size, output_size):
        self.model = Sequential()
        self.model.add(Dense(units=32, activation="relu", input_dim=input_size))
        self.model.add(Dense(units=32, activation="relu"))
        self.model.add(Dense(units=32, activation="relu"))
        self.model.add(Dense(units=output_size, activation="sigmoid"))
        self.model.compile(loss="mean_squared_error", optimizer="adam")

    def load_from_file(self, file):
        self.model.load_weights(file)

    def save_to_file(self, file):
        self.model.save_weights(file)

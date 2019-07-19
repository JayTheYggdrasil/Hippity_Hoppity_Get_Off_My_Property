from model import Model
from data.get_hops import get_data
import numpy as np

model = Model(30, 4)
x, y = get_data()
print(np.array(y))

model.model.fit(np.array(x), np.array(y), epochs=100, batch_size=32)

model.save_to_file("TheModel.h5")

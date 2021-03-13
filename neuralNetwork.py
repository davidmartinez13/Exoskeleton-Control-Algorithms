from ann_visualizer.visualize import ann_viz
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
import numpy

dataset = numpy.loadtxt("exoskeletonDataAI.csv", dtype=float, delimiter="," )
X = dataset[:,:3]
Y = dataset[:,3:]

model = Sequential()
model.add(Dense(3, input_dim=3, activation='relu')) # input layer requires input_dim param
model.add(Dense(20, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dropout(.2))
model.add(Dense(3, activation='softmax')) # softmax instead of relu for final class probability

# compile the neural network, adam gradient descent (optimized) (lr=0.005)
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

# call the function to fit to the data (training the network)
model.fit(X, Y, epochs = 1000, batch_size=10)
scores= model.evaluate(X,Y)
print("\n%s: %.2f%%"% (model.metrics_names[1],scores[1]*100))
model.save('weights3.h5')
# ann_viz(model,title="Neural Network")

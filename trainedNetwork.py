from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy


model = Sequential()
model.add(Dense(3, input_dim=3, activation='relu')) # input layer requires input_dim param
model.add(Dense(20, activation='relu'))
model.add(Dense(10, activation='relu'))

model.add(Dropout(.2))
model.add(Dense(3, activation='softmax')) # softmax instead of relu for final class probability

model.load_weights('weights2.h5')
while 1 :
 input_p1=input('insert input1 ')
 input_p2=input('insert input2 ')
 input_p3=input('insert input3 ')
 array1=numpy.array([[input_p1,input_p2,input_p3]])
 print(array1)
 predictions = model.predict(array1)
 # Print our model's predictions.
 print(predictions)



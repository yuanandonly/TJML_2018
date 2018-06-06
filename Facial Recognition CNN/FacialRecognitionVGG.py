from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.optimizers import RMSprop, SGD
from keras.datasets import mnist
import numpy as np
import csv

# INPUT
#training data
rows = []
with open('train.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        rows.append(row)
X = []
Y = []
for i in range(len(rows)):
    if i == 0:  # Skip header!
        continue
    pre = (rows[i][30].split(" "))
    X.append(np.array(pre).reshape(96, 96, 1))
    #X.append(row[30].split(" "))
    Y.append(rows[i][0:30])
percent = 100
portion = int(0.01*percent*len(X))
X_train, Y_train = np.array(X[:portion]), np.array(Y[:portion])
X_test, Y_test = np.array(X[portion:]), np.array(Y[portion:])
print(X_train.shape)

#testing data
rowsTest = []
with open('test.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        rowsTest.append(row)
x = []
for i in range(len(rowsTest)):
    if i == 0:  # Skip header!
        continue
    #x.append(rowsTest[i][1].split(" "))
    pre = (rowsTest[i][1].split(" "))
    x.append(np.array(pre).reshape(96, 96, 1))

#CNN
model = Sequential()
model.add(Conv2D(4, kernel_size=(5, 5), strides=(1, 1), activation='relu', input_shape=(96, 96, 1)))
model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
model.add(Dropout(.2))

model.add(Conv2D(8, kernel_size=(3, 3), strides=(1, 1), activation='relu', data_format='channels_last'))
model.add(Conv2D(8, kernel_size=(3, 3), strides=(1, 1), activation='relu', data_format='channels_last'))
model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
model.add(Dropout(.2))

model.add(Conv2D(16, kernel_size=(3, 3), strides=(1, 1), activation='relu', data_format='channels_last'))
model.add(Conv2D(16, kernel_size=(3, 3), strides=(1, 1), activation='relu', data_format='channels_last'))
model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
model.add(Dropout(.2))

model.add(Conv2D(32, kernel_size=(3, 3), strides=(1, 1), activation='relu', data_format='channels_last'))
model.add(Conv2D(32, kernel_size=(3, 3), strides=(1, 1), activation='relu', data_format='channels_last'))
model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
model.add(Dropout(.2))

model.add(Flatten())
model.add(Dense(2048, activation='relu'))
model.add(Dropout(.4))
model.add(Dense(30, activation='linear'))
#model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.SGD(lr=0.01), metrics=['accuracy'])
model.compile(loss='mean_squared_error', optimizer=RMSprop(), metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=32, epochs=8 , verbose=1)
#model.fit(X_train, Y_train, batch_size=100, epochs=15, verbose=1, validation_data=(X_test, Y_test))

y_test = model.predict(np.array(x))
output = []
header = []
header.append("ImageID.FeatureID")
header.append("Value")
output.append(header)
for i in range(2049):
    for x in range(30):
        row = []
        row.append(str(i + 1) + "." + str(x + 1))  # We start Ids at 1, so we need to add 1 to each value
        row.append(y_test[i][x])
        output.append(row)
print("here")
with open('submission.csv', 'w', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(output)

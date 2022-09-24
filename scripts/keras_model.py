
#from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.layers import Dense, Input, Dropout
from tensorflow.keras.models import Sequential
# Defining Keras model creator function
def create_model(optimizer="adam", dropout=0.1, n_features=60, n_units=64):
    model = Sequential()
    model.add(Dense(n_units, activation='relu', input_shape=(n_features,)))
    model.add(Dropout(dropout), )
    model.add(Dense(n_units, activation='relu'))
    model.add(Dropout(dropout), )          
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=optimizer,metrics=["accuracy"])
    return model
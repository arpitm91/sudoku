import tensorflow as tf
import numpy as np


def create_model():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(28, kernel_size=(3, 3), input_shape=(28, 28, 1)))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


class Recognizer:
    def __init__(self):
        self.model = create_model()
        self.model.load_weights("model.weights.h5")

    def predict(self, image):
        image = image.reshape(1, 28, 28, 1)
        result = self.model.predict(image, verbose=0)
        index = np.argmax(result, axis=1)[0]
        return index

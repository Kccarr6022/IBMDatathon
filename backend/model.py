import os
import tensorflow as tf
from tensorflow import keras

# print(tf.version.VERSION)

def create_model():
  model = tf.keras.Sequential([
    keras.layers.Dense(512, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10)
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

  return model

def load_model(model, checkpoint_path) {
    model = create_model()
    model.load_weights(checkpoint_path)
    return model
}

def infer(symptoms) {
    model = load_model()
    ## add code for model inference, 
    ## return result.
}
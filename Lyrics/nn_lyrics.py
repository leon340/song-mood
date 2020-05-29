"""
File: nn_lyrics.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Provide functions to load and use machine learning
models saved in JSON and their associated weights in h5

Predict and add_padding functions based on the TensorFlow text classification tutorial:
https://www.tensorflow.org/tutorials/text/text_classification_rnn
"""

import tensorflow_datasets as tfds
import tensorflow as tf
import os

dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)

train_data, test_data = dataset['train'], dataset['test']

encoder = info.features['text'].encoder


def add_padding(vec, size):
    zeros = [0] * (size - len(vec))
    vec.extend(zeros)
    return vec


def predict(text, pad, model_to_predict):
    encoded_text = encoder.encode(text)
    if pad:
        encoded_text = add_padding(encoded_text, 64)
    encoded_text = tf.cast(encoded_text, tf.float32)
    predictions = model_to_predict.predict(tf.expand_dims(encoded_text, 0))
    print("\nModel prediction: ", predictions)
    return predictions


def loadNN():
    cwd = os.getcwd()
    print(cwd)
    json_file = open('Lyrics/Models/modelIMDB.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = tf.keras.models.model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("Lyrics/Models/modelIMDB.h5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_model


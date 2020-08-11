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
import Lyrics.basic_lyrics as basic_lyrics

# Load the data set to obtain an encoder to make predictions

def createEncoder(dataset):
    """
    Creates and returns a word encoder for a given data set
    Currently only the imdb_reviews and yelp_polarity_reviews
    data sets are supported
    :param dataset: The data set that an encoder is being made for
    :return: encoder for the data set
    """
    if dataset == "IMDB":
        dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)
    elif dataset == "Yelp":
        dataset, info = tfds.load('yelp_polarity_reviews/subwords8k', with_info=True, as_supervised=True)
    else:
        print("Invalid data set!")
        return

    encoder = info.features['text'].encoder

    return encoder


def addPadding(vec, size):
    """
    Pads an array to a given size with zeros
    :param vec: The array/vector to be padded
    :param size: Size to pad to
    :return: The padded array
    """
    zeros = [0] * (size - len(vec))
    vec.extend(zeros)
    return vec


def lineByLinePrediction(weight_map, pad, model_to_predict, encoder):
    """
    Computes a weighted average prediction of the sentiment of the
    lyrics in the weight map
    :param weight_map: python dictionary with (Lyric line, weight) pairs.
    The weight is how frequently the line occurs in the lyrics
    :param pad: Weather or not to pad the text before prediction
    :param model_to_predict: Keras model used to predict the sentiment
    :param encoder: encoder used for the data set to allow words to be
    represented and used in the model
    :return: The sentiment of the lyrics 0 to 1 (1 being happy 0 being sad)
    """
    # weighted avg = (weight1 x sentiment1) + (weight2 x sentiment2) + .. + (weightN x sentimentN)
    print(weight_map)
    w_avg = 0
    for key in weight_map:
        prediction = predict(key, pad, model_to_predict, encoder, prepro=True)
        print("Key: " + key + " Prediction: " + str(prediction) + " Weight: " + str(weight_map[key]))
        w_avg += prediction * weight_map[key]
    return w_avg


def predict(text, pad, model_to_predict, encoder, prepro):
    """
    Predicts the sentiment of text given a Keras model
    :param text: Text to be analyzed
    :param pad: Weather or not to pad the text before prediction
    :param model_to_predict: Keras model used to predict the sentiment
    :param encoder: encoder used for the data set to allow words to be
    represented and used in the model
    :param prepro: whether or not the text should be pre-processed before prediction
    :return: The sentiment of the text 0 to 1 (1 being happy 0 being sad)
    """
    if prepro:
        text = basic_lyrics.preProcess(text)
    encoded_text = encoder.encode(text)
    if pad:
        encoded_text = addPadding(encoded_text, 64)
    encoded_text = tf.cast(encoded_text, tf.float32)
    predictions = model_to_predict.predict(tf.expand_dims(encoded_text, 0))
    return predictions[0][0]


def loadModel(name):
    """
    Loads the IMDB Keras model from a JSON, loads the weights into it
    compiles it, and returns it
    :param name: name of the model to load
    Only the 'IMDB' and 'Yelp' models are currently supported
    :return: the compiled and loaded model
    """
    json_file = open('Lyrics/Models/model' + name + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = tf.keras.models.model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights('Lyrics/Models/model' + name + '.h5')
    print("Loaded model from disk")

    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_model

"""
File: nn_lyrics.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Build and train a machine learning based
model to preform sentiment analysis on lyrics

Model based on TensorFlow text classification tutorial:
https://www.tensorflow.org/tutorials/text/text_classification_rnn
"""

import tensorflow_datasets as tfds
import tensorflow as tf

dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)

train_data, test_data = dataset['train'], dataset['test']

encoder = info.features['text'].encoder

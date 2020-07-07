"""
File: dataset_preprocess.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Extract the data from the MER lyrics
sentences dataset to be used for model fitting

The dataset contains lyrics associated with one of 4 quadrants
from the Russell emotion model:
Q1: Happy (can be excited or pleased)
Q2: Tense
Q3: Melancholy
Q4 Serene Joy (peaceful, relaxed)

Based on this tutorial https://www.tensorflow.org/tutorials/load_data/text
"""
import tensorflow as tf
import tensorflow_datasets as tfds

DATADIR = "../../data sets/MER_lyrics_sentences_dataset-ED/"
BUFFER_SIZE = 150
BATCH_SIZE = 10
TAKE_SIZE = 50
encoder = None


def getData():
    """
    Pulls the MER Lyrics Sentences Dataset and prepares it for
    use in training a model
    :return: training data, test data, and the size of the vocabulary
    used for the embedding
    """
    train_lyrics = tf.data.TextLineDataset(DATADIR + "Dataset-129_Sentences_condensed.txt")
    train_labels = tf.data.TextLineDataset(DATADIR + "Dataset-129_Sentences-Classes.txt")
    train_labels = train_labels.map(lambda string: converter(string))
    train_dataset = tf.data.Dataset.zip((train_lyrics, train_labels))

    test_lyrics = tf.data.TextLineDataset(DATADIR + "Dataset-239_Sentences_condensed.txt")
    test_labels = tf.data.TextLineDataset(DATADIR + "Dataset-239_Sentences-Classes.txt")
    test_labels = test_labels.map(lambda string: converter(string))
    test_dataset = tf.data.Dataset.zip((test_lyrics, test_labels))

    all_labeled_data = train_dataset.concatenate(test_dataset)
    all_labeled_data = all_labeled_data.shuffle(BUFFER_SIZE, reshuffle_each_iteration=False)

    vocab_set, vocab_size = createVocab(all_labeled_data)

    # Create the encoder using the vocabulary
    global encoder
    encoder = tfds.features.text.TokenTextEncoder(vocab_set)

    # Encode all of the lyrics in the dataset
    all_encoded_data = all_labeled_data.map(encode_map)

    train_data = all_encoded_data.skip(TAKE_SIZE).shuffle(BUFFER_SIZE)
    train_data = train_data.padded_batch(BATCH_SIZE)

    test_data = all_encoded_data.take(TAKE_SIZE).shuffle(BUFFER_SIZE)
    test_data = test_data.padded_batch(BATCH_SIZE)

    vocab_size += 1  # Because padding introduces a new token

    return train_data, test_data, vocab_size


def createVocab(all_labeled_data):
    """
    Creates a vocabulary set for a given text dataset
    :param all_labeled_data: text dataset
    :return: vocabulary set and its size
    """
    tokenizer = tfds.features.text.Tokenizer()
    vocab_set = set()
    for text, _ in all_labeled_data:
        tokens = tokenizer.tokenize(text.numpy())
        vocab_set.update(tokens)

    vocab_size = len(vocab_set)

    return vocab_set, vocab_size


def encode(text, label):
    """
    Encodes text using the global encoder
    :param text: text to be encoded
    :param label: label associated with the text
    :return: encoded text and label
    """
    encoded_text = encoder.encode(text.numpy())

    return encoded_text, label


def encode_map(text, label):
    """
    Map function used to encode text in a dataset
    :param text: text to be encoded
    :param label: label associated with the text
    :return: encoded text and label
    """
    encoded_text, label = tf.py_function(encode,
                                         inp=[text, label],
                                         Tout=(tf.int64, tf.int64))
    encoded_text.set_shape([None])
    label.set_shape([])

    return encoded_text, label


def converter(text):
    """
    Converts the quartile label to an integer
    :param text: quartile label (Q1-4)
    :return: The label as an integer tensor (1-4)
    """
    text = tf.strings.regex_replace(text, "Q", "")

    return tf.strings.to_number(text, out_type=tf.dtypes.int64)

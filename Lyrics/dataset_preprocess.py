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
"""
import random
import tensorflow as tf
import tensorflow_datasets as tfds

DATADIR = "../data sets/MER_lyrics_sentences_dataset-ED/"


def getData(type):
    if type == "Train":
        type = "129"
    elif type == "Test":
        type = "239"
    else:
        print("Invalid data type, please choose 'Train' or 'Test'")
        return

    # Each element of the array is another array: [sentence, Quartile (Q1-Q4)]
    data = []
    sentences = open(DATADIR + "Dataset-" + type + "_Sentences_condensed.txt")
    classes = open(DATADIR + "Dataset-" + type + "_Sentences-Classes.txt")

    for sentence, cls in zip(sentences, classes):
        data.append([sentence.strip("\n"), cls.strip("\n").strip("Q")])

    random.shuffle(data)

    sentences.close()
    classes.close()

    return data


# TODO: Using this tutorial https://www.tensorflow.org/tutorials/load_data/text


def converter(text):
    """
    Converts the quartile label to an integer
    :param text: quartile label (Q1-4)
    :return: The label as an integer tensor (1-4)
    """
    text = tf.strings.regex_replace(text, "Q", "")
    return tf.strings.to_number(text, out_type=tf.dtypes.int64)


BUFFER_SIZE = 50
BATCH_SIZE = 64
TAKE_SIZE = 100

train_lyrics = tf.data.TextLineDataset(DATADIR + "Dataset-" + "129" + "_Sentences_condensed.txt")
train_labels = tf.data.TextLineDataset(DATADIR + "Dataset-" + "129" + "_Sentences-Classes.txt")
train_labels = train_labels.map(lambda string: converter(string))
train_dataset = tf.data.Dataset.zip((train_lyrics, train_labels))

test_lyrics = tf.data.TextLineDataset(DATADIR + "Dataset-" + "239" + "_Sentences_condensed.txt")
test_labels = tf.data.TextLineDataset(DATADIR + "Dataset-" + "239" + "_Sentences-Classes.txt")
test_labels = test_labels.map(lambda string: converter(string))
test_dataset = tf.data.Dataset.zip((test_lyrics, test_labels))

# TODO: Don't forget to shuffle!

print(train_dataset)
print(list(train_dataset.as_numpy_iterator()))
print("train: ", type(train_dataset))
print("size: ", len(list(train_dataset.as_numpy_iterator())))

print("================")

print(test_dataset)
print(list(test_dataset.as_numpy_iterator()))
print("test: ", type(test_dataset))
print("size: ", len(list(test_dataset.as_numpy_iterator())))

print("================")

all_labeled_data = train_dataset.concatenate(test_dataset)
all_labeled_data = all_labeled_data.shuffle(BUFFER_SIZE, reshuffle_each_iteration=True)

print(all_labeled_data)
print(list(all_labeled_data.as_numpy_iterator()))
print("test: ", type(all_labeled_data))
print("size: ", len(list(all_labeled_data.as_numpy_iterator())))

print("================")

tokenizer = tfds.features.text.Tokenizer()
vocab_set = set()
for text, _ in all_labeled_data:
    tokens = tokenizer.tokenize(text.numpy())
    vocab_set.update(tokens)

vocab_size = len(vocab_set)

print(vocab_size)
print(vocab_set)

encoder = tfds.features.text.TokenTextEncoder(vocab_set)

example_text = next(iter(all_labeled_data))[0].numpy()
print(example_text)
encoded_example = encoder.encode(example_text)
print(encoded_example)


print("================")


def encode(text, label):
    encoded_text = encoder.encode(text.numpy())
    return encoded_text, label


def encode_map(text, label):
    encoded_text, label = tf.py_function(encode,
                                         inp=[text, label],
                                         Tout=(tf.int64, tf.int64))
    encoded_text.set_shape([None])
    label.set_shape([])

    return encoded_text, label


all_encoded_data = all_labeled_data.map(encode_map)
print(all_encoded_data)

print("================")

train_data = all_encoded_data.skip(TAKE_SIZE).shuffle(BUFFER_SIZE)
train_data = train_data.padded_batch(BATCH_SIZE)

test_data = all_encoded_data.take(TAKE_SIZE)
test_data = test_data.padded_batch(BATCH_SIZE)

# TODO: This errors since the label is a string (Q1-4)
# TODO: Should change the label to just a number 1-4
print(test_data)
sample_text, sample_labels = next(iter(test_data))

print(sample_text[0])
print(sample_labels[0])

vocab_size += 1  # Because padding introduces a new token

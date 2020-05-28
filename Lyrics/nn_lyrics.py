"""
File: nn_lyrics.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Build and train a machine learning based
model to preform sentiment analysis on lyrics

Model based on TensorFlow text classification tutorial:
https://www.tensorflow.org/tutorials/text/text_classification_rnn

Utilizing the IMDB Reviews dataset provided by tensorflow
"""

import tensorflow_datasets as tfds
import tensorflow as tf

dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)

train_data, test_data = dataset['train'], dataset['test']

encoder = info.features['text'].encoder

BUFFER_SIZE = 1000
BATCH_SIZE = 64

padded_shapes = ([None], ())

train_data = train_data.shuffle(BUFFER_SIZE).padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)

test_data = test_data.padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(encoder.vocab_size, 64),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history = model.fit(train_data, epochs=5, validation_data=test_data,
                    validation_steps=30)

test_loss, test_acc = model.evaluate(test_data)

print('Test Loss: {}'.format(test_loss))
print('Test Accuracy: {}'.format(test_acc))

# Save model as JSON
model_json = model.to_json()
with open("modelIMDB.json", "w") as json_file:
    json_file.write(model_json)

# Save weights as h5
model.save_weights("modelIMDB.h5")
print("Saved model to disk")


def add_padding(vec, size):
    zeros = [0] * (size - len(vec))
    vec.extend(zeros)
    return vec


def predict(text, pad):
    encoded_text = encoder.encode(text)
    if pad:
        encoded_text = add_padding(encoded_text, 64)
    encoded_text = tf.cast(encoded_text, tf.float32)
    predictions = model.predict(tf.expand_dims(encoded_text, 0))
    return (predictions)


# neutral_sample = "Here's a little song I wrote You might want to sing it note for note Don't worry, " \
#               "be happy In every life we have some trouble But when you worry you make it double " \
#               "Don't worry, be happy Don't worry, be happy now"
#
# predictions = predict(neutral_sample, pad=False)
# print("Neutral no pad: ", predictions)
#
# padded_predictions = predict(neutral_sample, pad=True)
# print(predictions)

happy_sample = "Because I'm happy Clap along if you feel like a room without a roof " \
               "Because I'm happy " \
               "Clap along if you feel like happiness is the truth"

predictions = predict(happy_sample, pad=False)
print("Happy no pad: ", predictions)

padded_predictions = predict(happy_sample, pad=True)
print("Happy with pad: ", predictions)
"""
File: modelIMDB.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Build, train, and save a machine learning based
model to preform sentiment analysis on lyrics

Model based on the TensorFlow text classification tutorial:
https://www.tensorflow.org/tutorials/text/text_classification_rnn

Utilizing the Yelp polarity reviews data set provided by tensorflow
"""

import tensorflow_datasets as tfds
import tensorflow as tf

# Load the data set
dataset, info = tfds.load('yelp_polarity_reviews/subwords8k', with_info=True, as_supervised=True)

train_data, test_data = dataset['train'], dataset['test']

encoder = info.features['text'].encoder

BUFFER_SIZE = 1000
BATCH_SIZE = 64

padded_shapes = ([None], ())

train_data = train_data.shuffle(BUFFER_SIZE).padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)

test_data = test_data.padded_batch(BATCH_SIZE, padded_shapes=padded_shapes)

# Create the recurrent model
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

# Calculate model accuracy
test_loss, test_acc = model.evaluate(test_data)

print('Test Loss: {}'.format(test_loss))
print('Test Accuracy: {}'.format(test_acc))

# Save model as JSON
model_json = model.to_json()
with open("modelYelp.json", "w") as json_file:
    json_file.write(model_json)

# Save weights as h5
model.save_weights("modelYelp.h5")
print("Saved model to disk")

# Test Loss: 0.13942851126194
# Test Accuracy: 0.9471579194068909

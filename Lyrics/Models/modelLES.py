"""
File: modelIMDB.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Build, train, and save a machine learning based
model to preform sentiment analysis on lyrics

Model based on the TensorFlow text classification tutorial:
https://www.tensorflow.org/tutorials/text/text_classification_rnn

Utilizing the IMDB Reviews data set provided by tensorflow
"""
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_hub as hub
from Lyrics.dataset_preprocess import getData

embedding = "https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"

# Get one of the tf encoders or the universal encoder
dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)

encoder = info.features['text'].encoder


# Split train_data into x (the text) and y (the Q1-4 label) for x and y parameters in fit
################
x, Y = zip(*getData("Train"))
x = list(x)
Y = list(Y)
test_data = getData("Test")


# Last layer should be a dense layer with 4 outputs for the 4 quadrants
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(encoder.vocab_size, 64),  # TODO: Change this line depending on encoder
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')  # Softmax for prob dist?
])

# model.compile(loss='binary_crossentropy',
#               optimizer=tf.keras.optimizers.Adam(1e-4),
#               metrics=['accuracy'])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Use test_data for validation data parameter in fit
# Use the split train_data, x (the text) and y (the Q1-4 label), for x and y parameters in fit
history = model.fit(x=x, y=Y, epochs=5, validation_data=test_data,
                    validation_steps=30)

# Calculate model accuracy
test_loss, test_acc = model.evaluate(test_data)

print('Test Loss: {}'.format(test_loss))
print('Test Accuracy: {}'.format(test_acc))

# Save model as JSON
model_json = model.to_json()
with open("modelLES.json", "w") as json_file:
    json_file.write(model_json)

# Save weights as h5
model.save_weights("modelLES.h5")
print("Saved model to disk")
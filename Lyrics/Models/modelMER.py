"""
File: modelMER.py
Language: python3
Author: Ethan David Howes <edh5623@rit.edu>
Purpose: Build, train, and save a machine learning based
model to preform sentiment analysis on lyrics

Model based on the TensorFlow Load Text/Text Classification tutorial:
https://www.tensorflow.org/tutorials/load_data/text
"""
import tensorflow as tf
from Lyrics.dataset_preprocess import getData

train_data, test_data, vocab_size = getData()

print(train_data)

# Last layer should be a dense layer with 4 outputs for the 4 quadrants
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 64),  # Change this line depending on encoder
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])
# clip value of 1.0 gives .2200 accuracy but still nan loss
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0000001, clipvalue=1),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Use test_data for validation data parameter in fit
# Use the split train_data, x (the text) and y (the Q1-4 label), for x and y parameters in fit
history = model.fit(train_data, epochs=3, validation_data=test_data)

# Calculate model accuracy
test_loss, test_acc = model.evaluate(test_data)
print('Test Loss: {}'.format(test_loss))
print('Test Accuracy: {}'.format(test_acc))

# Save model as JSON
model_json = model.to_json()
with open("modelMER.json", "w") as json_file:
    json_file.write(model_json)

# Save weights as h5
model.save_weights("modelMER.h5")
print("Saved model to disk")
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
    train_data = []
    sentences = open(DATADIR + "Dataset-" + type + "_Sentences.txt")
    condensed_sentences = []  # used to remove the whitespace in the sentences file
    classes = open(DATADIR + "Dataset-" + type + "_Sentences-Classes.txt")

    for line in sentences:
        if not line.isspace():
            condensed_sentences.append(line)

    for sentence, cls in zip(condensed_sentences, classes):
        train_data.append([sentence.strip("\n"), cls.strip("\n")])

    return train_data


print(getData("Train"))
print(getData("Test"))

# Songtiment-Analysis
Advanced sentiment analysis of music.

# Lyrical Analysis

**Overview**

Using the lyricsgenius API, searches for the song 
lyrics requested by the user via command line
arguments and performs a sentiment analysis of
those lyrics displaying the result.

**Pre-processing**

Using the Natural Language Toolkit (NLTK) the 
program first tokenizes the lyrics so pre-processing
can begin. Then, stop words are filtered out of the
tokenized lyrics to remove extra noise and unnecessary
words that have little effect on overall sentiment.
Next, each word is reduced to its base form via
lemmatization. Finally, the lyrics are detokenized
back into a string so sentiment analysis can begin.

**Lexicon Based Sentiment Analysis**

Using both NLTK's SentimentIntensityAnalyzer
and textblob's sentiment polarity a sentiment
analysis is performed on the pre-processed lyrics.
An average is taken between the result of the textblob
analysis and the SentimentIntensityAnalyzer. The
average gives a good middle ground between the two
analyzers as sometimes one provides a better assessment
of sentiment depending on the lyrics.

**Machine Learning Based Sentiment Analysis**

Two models were created using the Yelp polarity reviews data set 
and the IMDB reviews data set from the provided data sets in Tensorflow.
Both models used the same recurrent structure, see code for specific details.
The "Yelp model" achieved 94.7% test accuracy after training while the
"IMDB model" achieved 86% test accuracy. Despite the high accuracy achieved
by the Yelp model and the moderately high accuracy achieved by the IMDB model
both were inconsistent in determining the sentiment of lyrics during manual
testing. Perhaps these are not the correct data sets to use for this problem.
Movie or restaurant reviews are quite different from song lyrics.
A data set containing lyrics and their associated sentiment may be more appropriate.

An attempt was made to create a model using the MER data set which contained lyrics 
associated with one of 4 quadrants
from the Russell emotion model:
Q1: Happy (can be excited or pleased)
Q2: Tense
Q3: Melancholy
Q4 Serene Joy (peaceful, relaxed). However, the model achieved very low
accuracy as well as a consistent loss of nan. Many different solutions were attempted
to fix these issues to no avail. This model should be revisited in the future.

_Notes:_

After testing a plethora of songs, lyrical analysis 
is not always indicative of the general mood of the
song. Though it gives a good baseline there are 
other factors impacting the sentiment of the song.
Factors such as tempo, mode, loudness, and how 
reliant the song is on its lyrics will be also investigated.

The IMDB and Yelp models should be sufficient to continue research
into the other factors impacting song sentiment however the MER model
should be revisited to improve accuracy in the future.

# Tempo Analysis

**Overview:**

Predict the sentiment of a song based on its tempo.

# Loudness Analysis 

**Overview:**

Predict the sentiment of a song based on its loudness.

# Final Sentiment Equation

**Overview:**

Something must tie together the various factors impacting song sentiment to be explored.
Currently, an average of the lyrical and title sentiment is taken between the IMDB model,
Yelp model, Text blob, and NLTK's SentimentIntensityAnalyzer to produce
a final sentiment score from 0 to 1. This does not yet take into account
the other factors contributing to a song's sentiment and must be expanded upon.

**Equation Inputs:** Mode, Lyric Sentiment, Title Sentiment, Loudness, Tempo

**Equation Outputs:** Scale of how happy or sad the song is

Reliance on lyrics still to be investigated

# Resources
Inspiration: https://kvsingh.github.io/lyrics-sentiment-analysis.html

Guideline used for sentiment analysis: https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk

NLTK Vader: Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious 
Rule-based Model for Sentiment Analysis of Social Media Text. 
Eighth International Conference on Weblogs and Social Media (ICWSM-14). 
Ann Arbor, MI, June 2014.

MER dataset: Ricardo Malheiro (2017). 
“Emotion-based Analysis and Classification of Music Lyrics“. Doctoral 
Program in Information Science and Technology. University of Coimbra.

TensorFlow Load Text/Text Classification tutorial:
https://www.tensorflow.org/tutorials/load_data/text

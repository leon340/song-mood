# Songtiment-Analysis
Advanced sentiment analysis of music analyzing
the sentiment of lyrics and acoustic features.

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

# Tempo and Loudness Analysis 

**Overview**

Attempt to predict the sentiment of a song based on its average loudness and tempo.

**Data Set**

In order to associate these measures with sentiment, a dataset was compiled in order
to study the relationship between song sentiment and tempo and loudness. Using 
Spotipy, a Python library for the Spotify API, a diverse dataset containing over
1,000 Spotify tracks from multiple genres was complied. Each track has various 
attributes including Spotify's assessment of the track's sentiment (valence), average loudness in dB,
and tempo in BPM.

**Data Analysis**

The goal of this analysis was to find the average tempo/loudness of average songs, sad songs, and happy songs.
The average tempo over all tracks in the dataset as well as the average loudness served as a middle ground for
the sentiment prediction. Then, averages of the same measures were taken over tracks only above or below
certain valences in order to assess the average tempo and loudness of happy and sad songs. A regression 
analysis was conducted on the resulting (valence, average tempo) and (valence, average loudness) pairs. The two regression
equations obtained from this analysis each provide estimates of the sentiment of the song given its tempo or average loudness.

<img src="https://github.com/edh5623/Songtiment-Analysis/blob/master/Song_Stats/tempo_valence_relationship.jpg" alt="Tempo" width="49%"> <img src="https://github.com/edh5623/Songtiment-Analysis/blob/master/Song_Stats/loudness_valence_relationship.jpg" alt="Loudness" width="49%">

_Notes:_

Both regression lines extend beyond valence values of 1.0, however, for this application, the valence will be capped at 1.0 to keep a
consistent 0-1 sentiment scale. This means that though a tempo of 160 may be projected to have a valence of 13.0 by the regression equation
it will be represented as a 1.0 valence when being used in the final equation.

# Final Sentiment Equation

**Overview**

Something must tie together the various factors impacting song sentiment to be explored.
An average of the lyrical and title sentiment between the IMDB model,
Yelp model, Text blob, and NLTK's SentimentIntensityAnalyzer does not 
take into account the other factors contributing to a song's sentiment 
and must be expanded upon.

**Equation Inputs:** Mode, Lyric Sentiment, Title Sentiment, Loudness, Tempo

**Equation Outputs:** The Final Sentiment, a measure of how sad or happy the song is (0-1)

The equation is a weighted average of the sentiments predicted by each input:

```
Final Sentiment = ((Mode Weight * mode sentiment) + 
                   (Text Weight * combined sentiment of the lyrics and title) +
                   (Loudness Weight * sentiment predicted by the loudness regression equation) + 
                   (Tempo Weight * sentiment predicted by the tempo regression equation)) / Sum of the weights
```

The mode of the song is extracted using Spotipy and is represented as a 1 for major and 0 for minor. A major mode is usually 
associated with happier feelings while a minor often evokes a more somber mood. The combined sentiment of the lyrics and title 
is calculated by another weighted average of their sentiments. This average weighs the lyric sentiment by 0.75 and the title 
sentiment by 0.25. The loudness and tempo of the song are also extracted via Spotipy and used with the regression equations 
created in the tempo and loudness analysis to produce their predictions of the song's sentiment.

**Equation Weights**

The weights used in the final sentiment equation were taken from a study conducted in 2015 by Jamdar, 
Abraham, Khanna, and Dubey which proposed a method to detect the emotion of music using lyrical and audio features 
with a k-Nearest neighbors classifier. Jamdar et al. used weights for the features to better categorize the song 
into an emotion. These weights worked well for this analysis in the final sentiment equation as well.

_Notes:_

Though this equation proved to be slightly more accurate in initial testing than a purely lyrical analysis, 
the acoustic features of the song may vary widely depending on the genre of the song. This along with
improved lyrical assessment will be investigated to increase the accuracy of this evolving system.

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

Python library for Spotify API: https://github.com/plamere/spotipy

Regression calculator used: https://keisan.casio.com/exec/system/14059932387562

Study used for weights in final equation: https://arxiv.org/ftp/arxiv/papers/1506/1506.05012.pdf             
Jamdar, A., Abraham, J., Khanna, K., &amp; Dubey, R. (2015). Emotion Analysis of Songs Based on Lyrical 
and Audio Features. International Journal of Artificial Intelligence &amp; Applications, 6(3), 35-50. 
doi:10.5121/ijaia.2015.6304

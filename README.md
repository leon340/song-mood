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

**Sentiment Analysis**

Using both NLTK's SentimentIntensityAnalyzer
and textblob's sentiment polarity a sentiment
analysis is performed on the pre-processed lyrics.
An average is taken between the result of the textblob
analysis and the SentimentIntensityAnalyzer. The
average gives a good middle ground between the two
analyzers as sometimes one provides a better assessment
of sentiment depending on the lyrics.

_Notes:_

After testing a plethora of songs, lyrical analysis 
is not always indicative of the general mood of the
song. Though it gives a good baseline there are 
other factors impacting the sentiment of the song.
Factors such as key, loudness, and how 
reliant the song is on its lyrics will be investigated.

# Resources
Inspiration: https://kvsingh.github.io/lyrics-sentiment-analysis.html

Guideline used for sentiment analysis: https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk

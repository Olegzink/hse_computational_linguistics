import nltk
import pandas as pd
import numpy as np
from statistics import mean
import os.path as path
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from sklearn_sentiment.sentiment_ready import trained_sentiment_model
from afinn import Afinn
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer

main_path = path.abspath(path.join(__file__, ".."))

def calculate_sentiment(phrase):

    # Worst hotel ive stayed in. - The lock housing was exposed meaning it wasnt difficult to break into our room. - No safety deposit boxes in rooms. - Hot water constantly running out. -  - Virtually no cooking utensils, making a basic task such as hard boiling an egg extremely difficult.

    df = pd.read_csv(f'{main_path}/data/adjectives_lexicon.csv', delimiter=",", usecols=['word', 'sentiment'])
    print(df)

    tokens = nltk.word_tokenize(phrase.lower())
    print(tokens)

    print()
    print('=====================')
    print('sentiment lexicon - word by word')
    print('=====================')

    sentim_scores = []
    for key in tokens:
        try:
            x = df[df.word.str.contains(r'\b{}\b'.format(key), na=False)]
            print(x)
            print(x.iloc[0])
            sentim_scores.append(list(x.values[0])[1])
        except:
            sentim_scores.append(0.1)
    #
    print(sentim_scores)

    mean_sent_score = mean(sentim_scores)
    print(mean_sent_score)

    if mean_sent_score > 0:
        overall_sentiment = 1
    else:
        overall_sentiment = -1

    print(overall_sentiment)

    tknzr = TweetTokenizer()

    def lemmatize(text):
        '''lemmatizes text for the given pos tags - NN,VB,JJ'''

        wnl = WordNetLemmatizer()
        for word, tag in pos_tag(tknzr.tokenize(text)):

            if tag.startswith("NN"):
                yield wnl.lemmatize(word, pos='n')
            elif tag.startswith('VB'):
                yield wnl.lemmatize(word, pos='v')
            elif tag.startswith('JJ'):
                yield wnl.lemmatize(word, pos='a')
            else:
                yield word

    print()
    print('=====================')
    print('Textblob')
    print('=====================')

    from textblob.sentiments import NaiveBayesAnalyzer
    textblob_sent_score = TextBlob(doc, analyzer=NaiveBayesAnalyzer()).polarity
    print(textblob_sent_score)

    if textblob_sent_score > 1:
        overall_textblob_sentiment = 1
    elif textblob_sent_score < 1:
        overall_textblob_sentiment = -1
    else:
        overall_textblob_sentiment = 0

    print(overall_textblob_sentiment)

    print()
    print('=====================')
    print('Vader Sentiment Intensity Analyzer')
    print('=====================')

    sid = SentimentIntensityAnalyzer()

    vader_sent_score = sid.polarity_scores(doc)
    print(vader_sent_score)

    if vader_sent_score['compound'] > 1:
        overall_vader_sentiment = 1
    elif vader_sent_score['compound'] < 1:
        overall_vader_sentiment = -1
    else:
        overall_vader_sentiment = 0

    print(overall_vader_sentiment)

    print()
    print('=====================')
    print('Afinn Analyzer')
    print('=====================')

    # https://github.com/fnielsen/afinn
    afinn = Afinn()
    afinn_sent_score = afinn.score(doc)
    print(afinn_sent_score)

    if afinn_sent_score > 0:
        overall_afinn_sentiment = 1
    else:
        overall_afinn_sentiment = -1

    print(overall_afinn_sentiment)

    print()
    print('=====================')
    print('ML model')
    print('=====================')

    trained_model_score = trained_sentiment_model([doc])

    if trained_model_score == 'positive':
        overall_model_sentiment = -1
    else:
        overall_model_sentiment = -1

    print('overall_model_sentiment')
    print(overall_model_sentiment)

    prob_sentiment = mean([overall_sentiment, overall_vader_sentiment, overall_afinn_sentiment, overall_textblob_sentiment, overall_model_sentiment])

    print()
    print('prob_sentiment:')
    print(prob_sentiment)

    if prob_sentiment < 0:
        calculated_sentiment = 'neg'
    else:
        calculated_sentiment = 'pos'
    print(calculated_sentiment)


if __name__ == '__main__':

    doc = "No ventilation in bathroom (No window or extractor fan) leaving the bathroom misty after taking a shower and leaving it smelly after using the loo."

    calculate_sentiment(doc)

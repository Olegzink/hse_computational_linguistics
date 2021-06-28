# coding=utf8

import pandas as pd
import nltk
from nltk import RegexpParser, pos_tag
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
import spacy
# from spacy.lemmatizer import Lemmatizer, ADJ, NOUN, VERB
from collections import defaultdict
import io
import os.path as path
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
# pip install pyspellchecker
from spellchecker import SpellChecker
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from statistics import mean
import nltk
import pandas as pd
import numpy as np
from statistics import mean
import os.path as path
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob.sentiments import NaiveBayesAnalyzer
# from sklearn_sentiment.sentiment_ready import trained_sentiment_model
from afinn import Afinn
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import joblib
import pickle
import gensim
from gensim.test.utils import get_tmpfile
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

# todo - in production change model for lg
# nlp = spacy.load('C:/dev/sandbox/brand_aspect/myvenv/Lib/site-packages/en_core_web_sm/en_core_web_sm-2.3.1')
nlp = spacy.load('C:/dev/sandbox/brand_aspect/myvenv/Lib/site-packages/en_core_web_sm/en_core_web_sm-3.0.0/')

main_path = path.abspath(path.join(__file__, ".."))

# load vectorizer
with open(f'{main_path}/data/svc_model/svc_tf_idf_vectorizer.pk', 'rb') as filename:
    vectorizer = pickle.load(filename)
print(vectorizer)

# load model
with open(f'{main_path}/data/svc_model/svc_model_tf_idf.joblib.pkl', 'rb') as filename:
    model = joblib.load(filename)
print(model)

# load doc2vec model
fname = get_tmpfile(f'{main_path}/data/doc2vec_model/doc2vec_model_final_new.mdl')
doc2vec_model = Doc2Vec.load(fname)
print(doc2vec_model)

with open(f'{main_path}/data/doc2vec_model/logistic_reg_doc2vec.joblib.pkl', 'rb') as filename:
    doc2vec_log_reg = joblib.load(filename)
print(doc2vec_log_reg)


# Vader instance
sid = SentimentIntensityAnalyzer()
# https://github.com/fnielsen/afinn
afinn = Afinn()

def intention_finder(text):

    '''intentions_list = []

    # main_path = path.abspath(path.join(__file__, ".."))
    main_path = 'C:/dev/sandbox/brand_aspect/production'

    segments_df = pd.read_csv(f"{main_path}/bootstrap_lexicon/data/thematic_words_norm.csv", delimiter=',')

    doc = nlp(text)
    lemmatizer = nlp.add_pipe("lemmatizer")

    for token in doc:
        if token.dep_ == 'dobj':
            dobj = str(token)
            tverb = token.head
            lemmatizer = nlp.vocab.morphology.lemmatizer
            tverb = lemmatizer(str(tverb), VERB)
            tverb_str = str(tverb[0])
            print()
            print(tverb_str, ' ', dobj)

            categories = []
            try:
                col_name = segments_df.columns[segments_df.isin([dobj]).any()]
                print(col_name)
                categories.append(col_name[0])

                # [{'room': 'extend the space'}, {'food': 'order coffee'}]
                intentions_dict = {}
                intentions_dict[categories[0]] = tverb_str + ' ' + dobj

                intentions_list.append(intentions_dict)
            except:
                pass

            print(categories)

    return intentions_list'''

    return [{'None':'None'}]


def normalize_reviews(review):

    spell = SpellChecker()

    tokenized = word_tokenize(review)
    # delete words less 2 chars
    tokenized = [x for x in tokenized if not len(x) <= 2]
    tokenized = [spell.correction(word) for word in tokenized]


def simple_preprocess(review):

    # sent = review.lower()
    # remove leading whitespace
    sent = review.lstrip()
    # remove trailing whitespace
    sent = sent.rstrip()
    # removing double spaces and more spaces + all special chars
    sent = re.sub("\s\s+", " ", sent)
    # removing special chars and punct
    # sent = re.sub(r"[-()\"#/@;:<>{}[`+=~|.!?,]", "", sent)
    # repr - to see the difference in case of non equality
    # print(repr(sent))
    return sent


def review_sent_tokenize(review, current_db_obj):

    doc = nlp(review)
    tokenized_phrases = [str(sent) for sent in doc.sents]
    spell = SpellChecker()
    word_tokenized = [word_tokenize(word) for word in tokenized_phrases]
    spell_corrected = [[spell.correction(x) for x in group] for group in word_tokenized]
    joined_spell = [' '.join(x).capitalize() for x in spell_corrected]

    phrases_objs = []
    for phrase in joined_spell:
        final_dict = {'phrase': phrase, 'review_id': current_db_obj.review_id}
        phrases_objs.append(final_dict)

    # [{'phrase': 'and i wanted to order some coffee', 'review_id': 12}, {'phrase': 'rooms are two story with narrow steps', 'review_id': 35},]
    return phrases_objs


def preprocess_text(text):
    '''Removes html tags, '\n', double spaces and 'nbsp;', etc.'''

    TAG_RE = re.compile(r'<[^>]+>')
    text = TAG_RE.sub('', text)
    text = re.sub(' +', ' ', text)
    text = text.replace("&nbsp;", " ")
    text = text.replace("\n", " ")
    # Remove all the special characters
    text = re.sub(r'\W', ' ', str(text))
    # remove all single characters
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    # Remove single characters from the start
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    # Substituting multiple spaces with single space
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    # Removing prefixed 'b'
    text = re.sub(r'^b\s+', '', text)
    # Converting to Lowercase
    text = text.lower()

    return text


def lemmatize_tokenize(text, sentiment_stop_words_list):
    '''lemmatizes text for the given pos tags - NN,VB,JJ'''

    wnl = WordNetLemmatizer()
    tknzr = TweetTokenizer()
    spell = SpellChecker()

    for word, tag in pos_tag(tknzr.tokenize(text)):

        word = spell.correction(word)

        if len(word) < 2:
            continue
        elif word not in sentiment_stop_words_list:
            if tag.startswith("NN"):
                yield wnl.lemmatize(word, pos='n')
            elif tag.startswith('VB'):
                yield wnl.lemmatize(word, pos='v')
            elif tag.startswith('JJ'):
                yield wnl.lemmatize(word, pos='a')
            else:
                yield word

def calculate_sentiment(phrase, classification_method):

    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(type(classification_method))
    print(classification_method)

    stop_words_df = pd.read_csv(f'{main_path}/data/stop_words_final.csv', encoding="utf-8")
    sentiment_stop_words_list = stop_words_df.iloc[:,0].tolist()

    phrase = preprocess_text(phrase)
    tokenized_phrase = list(lemmatize_tokenize(phrase, sentiment_stop_words_list))
    phrase = ' '.join(tokenized_phrase)

    if classification_method == 'aggregated':

        print()
        print('=====================')
        print('Using aggregated method for classification')
        print('=====================')

        # Worst hotel ive stayed in. - The lock housing was exposed meaning it wasnt difficult to break into our room. - No safety deposit boxes in rooms. - Hot water constantly running out. -  - Virtually no cooking utensils, making a basic task such as hard boiling an egg extremely difficult.

        # df = pd.read_csv(f'{main_path}/data/adjectives_lexicon.csv', delimiter=",", usecols=['word', 'sentiment'])

        print()
        print('=====================')
        print('sentiment lexicon - word by word')
        print('=====================')

        # sentim_scores = []
        # for key in tokens:
        #     try:
        #         x = df[df.word.str.contains(r'\b{}\b'.format(key), na=False)]
        #         print(x)
        #         print(x.iloc[0])
        #         sentim_scores.append(list(x.values[0])[1])
        #     except:
        #         sentim_scores.append(0.1)
        # #
        # print(sentim_scores)
        #
        # mean_sent_score = mean(sentim_scores)
        # print(mean_sent_score)
        #
        # if mean_sent_score > 0:
        #     overall_sentiment = 1
        # else:
        #     overall_sentiment = -1
        #
        # print(overall_sentiment)

        print()
        print('=====================')
        print('Textblob')
        print('=====================')

        textblob_sent_score = TextBlob(phrase, analyzer=NaiveBayesAnalyzer()).polarity
        print(textblob_sent_score)

        if textblob_sent_score > 0.5:
            overall_textblob_sentiment = 1
        elif textblob_sent_score < 0:
            overall_textblob_sentiment = -1
        else:
            overall_textblob_sentiment = 0

        print(overall_textblob_sentiment)

        print()
        print('=====================')
        print('Vader Sentiment Intensity Analyzer')
        print('=====================')

        vader_sent_score = sid.polarity_scores(phrase)
        print(vader_sent_score)

        if vader_sent_score['compound'] > 0.5:
            overall_vader_sentiment = 1
        elif vader_sent_score['compound'] < 0:
            overall_vader_sentiment = -1
        else:
            overall_vader_sentiment = 0

        print(overall_vader_sentiment)

        print()
        print('=====================')
        print('Afinn Analyzer')
        print('=====================')

        afinn_sent_score = afinn.score(phrase)
        print(afinn_sent_score)

        if afinn_sent_score > 0:
            overall_afinn_sentiment = 1
        else:
            overall_afinn_sentiment = -1

        print(overall_afinn_sentiment)

        print()
        print('=====================')
        print('Using ML model')
        print('=====================')

        processed_features = vectorizer.transform([phrase]).toarray()
        print(processed_features)

        trained_mdl_sentiment = model.predict(processed_features)[0]
        print('trained_mdl_sentiment')
        print(trained_mdl_sentiment)

        # from sklearn_sentiment.sentiment_ready import trained_sentiment_model
        # trained_mdl_sentiment = trained_sentiment_model([phrase])[0]

        all_scores = [(overall_vader_sentiment), overall_afinn_sentiment, overall_textblob_sentiment, trained_mdl_sentiment]
        all_scores = [int(x) for x in all_scores]
        print('all_scores')
        print(all_scores)
        prob_sentiment = mean(all_scores)

        print('prob_sentiment')
        print(prob_sentiment)

        if prob_sentiment < 0:
            calculated_sentiment = 'neg'
        elif prob_sentiment < 0.25:
            calculated_sentiment = 'neu'
        else:
            calculated_sentiment = 'pos'

        print(calculated_sentiment)

    elif classification_method == 'ml_model':

        print()
        print('=====================')
        print('Using ML model for classification')
        print('=====================')

        processed_features = vectorizer.transform([phrase]).toarray()
        print(processed_features)

        trained_mdl_sentiment = model.predict(processed_features)[0]
        print('trained_mdl_sentiment')
        print(trained_mdl_sentiment)

        if trained_mdl_sentiment == 0:
            calculated_sentiment = 'neg'
        else:
            calculated_sentiment = 'pos'

    elif classification_method == 'doc2vec':

        print()
        print('=====================')
        print('Using doc2vec model for classification')
        print('=====================')

        text_new_vec = doc2vec_model.infer_vector(tokenized_phrase, epochs=20)
        print("V1_infer", text_new_vec)

        predicted = doc2vec_log_reg.predict([text_new_vec])

        if predicted == 0:
            calculated_sentiment = 'neg'
        else:
            calculated_sentiment = 'pos'

    return calculated_sentiment


if __name__ == '__main__':

    text = '''In a lower price range accomodations the best in alienate so far where i have stayed ( and i have stayed least at 15 other accomodations ) '''
    # text = '''In a lower price range accomotations the best in Alicante so far where i have stayed ( and i have stayed least at 15 other accomotationes). Good climate ( not moist like half of places). Very cozy. And super pillows. Really the best experiance in Alicante so fat!'''

    # from collections import namedtuple
    #
    # review_db_obj = namedtuple('review_from_db' , ['review_id'])
    # current_db_obj = review_db_obj(12)
    #
    # print(review_sent_tokenize(text, current_db_obj=current_db_obj))
    #
    calculate_sentiment(text)



review = ''' Way overpriced and the deposit for the minibar to which I refused as allergic to alcohol
'''

import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

df = pd.read_csv('C:/dev/datasets/hotel_reviews/hotel_reviews.csv', delimiter=',', nrows=50)

# segments_df = pd.read_csv("C:/dev/datasets/hotel_reviews/sample_segments.csv", delimiter=';')
segments_df = pd.read_csv("data/thematic_words_norm.csv", delimiter=',')

print(segments_df)

def pre_process(text):
    # lowercase
    text = text.lower()

    # remove tags
    text = re.sub("", "", text)

    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    return text


def get_stop_words(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results

class LemmaTokenizer(object):

    def __init__(self):

        self.wnl = WordNetLemmatizer()

    def __call__(self, articles):

        return [self.wnl.lemmatize(t) for t in word_tokenize(articles)]

# load a set of stop words
stopwords = get_stop_words("preprocess/terrier_stops.txt")

df['Negative_Review'] = df['Negative_Review'].apply(lambda x:pre_process(x))

# get the text column
docs = df['Negative_Review'].tolist()

# !!! todo: Turn off lemmatization if performing POS!
# create a vocabulary of words, ignore words that appear in 85% of documents,
cv = CountVectorizer(max_df=0.85, stop_words=stopwords, max_features=10000, tokenizer=LemmaTokenizer())
# fit_transform creates the vocabulary and returns a term-document matrix which is what we want
word_count_vector = cv.fit_transform(docs)

# Now, let’s look at 10 words from our vocabulary.
print(list(cv.vocabulary_.keys())[:10])

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
# invoke large corpora
tfidf_transformer.fit(word_count_vector)

# you only needs to do this once, this is a mapping of index to
feature_names = cv.get_feature_names()

# get the document that we want to extract keywords from
doc=docs[2]

#generate tf-idf for the given document
tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

#sort the tf-idf vectors by descending order of scores
sorted_items = sort_coo(tf_idf_vector.tocoo())

#extract only the top n; n here is 10
keywords = extract_topn_from_vector(feature_names, sorted_items, 10)
print(keywords)


# now print the results
print("\n=====Doc=====")
print(doc)

print("\n===Keywords===")
for k in keywords:
    print(k, keywords[k])

most_likely_key = max(keywords, key=keywords.get)
print()
print('Most likely key:')
print(most_likely_key)

# mask = np.column_stack([segments_df[col].str.contains(key, na=False) for col in segments_df])
# print(segments_df.loc[mask.any(axis=1)])
# print(segments_df.apply(lambda row: row.astype(str).str.contains(key).any(), axis=1))

# # applied only to labels
# df2 = segments_df.filter(regex=most_likely_key)
# # print(df2)

print()
# x = segments_df.columns[segments_df.isin([most_likely_key]).any()]
# print(x)

print('Assigned category:')
try:
    col_name = segments_df.columns[segments_df.isin([most_likely_key]).any()]
    print(col_name[0])
except:
    print('General')


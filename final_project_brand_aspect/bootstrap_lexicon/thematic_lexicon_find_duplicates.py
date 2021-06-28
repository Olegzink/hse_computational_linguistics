import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import RegexpParser, pos_tag
import os.path as path

main_path = path.abspath(path.join(__file__, ".."))

segments_df = pd.read_csv(f"{main_path}/data/thematic_lexicon_prod.csv", delimiter=',')
print(segments_df)
segments_df.drop(['Unnamed: 0'], inplace=True, axis = 1)
print(segments_df)

unique_words = []
duplicates = []
for col in segments_df:
    for wrd in segments_df[col]:
        if wrd in unique_words and str(wrd) != 'nan':
            duplicates.append(wrd)
        else:
            unique_words.append(wrd)

print(duplicates)

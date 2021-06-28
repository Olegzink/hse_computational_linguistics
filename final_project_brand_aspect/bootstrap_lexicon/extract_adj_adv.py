# coding=utf8
import io
import pandas as pd
from nltk import RegexpParser, pos_tag
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
from spellchecker import SpellChecker
from collections import Counter
import numpy as np
import winsound

frequency = 500  # Set Frequency To 2500 Hertz
duration = 1200  # Set Duration To 1000 ms == 1 second

df = pd.read_csv('C:/dev/datasets/hotel_reviews/hotel_reviews.csv', delimiter=',', nrows=3000)
# print(df)

from nltk.stem import WordNetLemmatizer

spell = SpellChecker()
lemmatizer = WordNetLemmatizer()

# define noun phrase chunk grammar here
# noun_chunk_grammar = "N: {<NN>|<NNS>|<VBG>}"
noun_chunk_grammar = "ADJ: {<JJ>|<JJR>|<JJS>}"
# create noun phrase RegexpParser object here
noun_chunk_parser = RegexpParser(noun_chunk_grammar)

adj_chunked_text = []

corpus_tkns_count = 0

# todo Pull request - to NLTK if len(word) <= 200 tokenized = word_tokenize(neg)

for neg in df['Negative_Review']:

    tokenized = word_tokenize(neg)
    # delete words less 2 chars
    tokenized = [x for x in tokenized if not len(x) <= 2]
    corpus_tkns_count += len(tokenized)
    # Spell correction
    tokenized = [spell.correction(word) for word in tokenized]
    pos_tokenized = pos_tag(tokenized)

    try:
        tree = noun_chunk_parser.parse(pos_tokenized)
        # print(parsed_nouns)

        for subtree in tree.subtrees(filter = lambda t: t.label()=='ADJ'):
            # print()
            # print(subtree)
            ls = []
            for item in subtree.leaves():

                adj = item[0].lower()
                ls.append(adj)
                print(ls)

            adj_chunked_text.append(ls)

    except:
        pass

# converting to flat list
adj_chunked_text = [item for sublist in adj_chunked_text for item in sublist]
adj_chunked_text_counter = Counter(adj_chunked_text)

adjs_count = []
identifiers_count = []
nouns_count = []
pmi_metric = []

# PMI counter
for adj in adj_chunked_text:

    adj_cnt = adj_chunked_text_counter.get(adj, 0)
    adjs_count.append(adj_cnt)

    # prob_collocation = adj_cnt / corpus_tkns_count
    # prob_identifier = indentifier_cnt / corpus_tkns_count
    # prob_noun = noun_cnt / corpus_tkns_count
    #
    # try:
    #     pmi = np.log2( prob_collocation / (prob_identifier * prob_noun) )
    # except:
    #     pmi = 0.00
    # pmi_metric.append(pmi)

adjs_df = pd.DataFrame()
adjs_df['adjective'] = adj_chunked_text
adjs_df['adj_count'] = adjs_count
adjs_df.drop_duplicates(subset=['adjective'], inplace=True)

# adjs_df['PMI'] = pmi_metric

# print(adjs_df)

print(adjs_df.sort_values(by=['adj_count'], ascending=False))

# print(corpus_tkns_count)

# set(adj_chunked_text)

with io.open('data/adjectives_neg.csv', 'w', encoding="utf-8", newline='') as f:
    adjs_df.to_csv(f, header=True, index=False)

winsound.Beep(frequency, duration)

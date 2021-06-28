# coding=utf8
import io
import pandas as pd
from nltk import RegexpParser, pos_tag
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from collections import Counter
import numpy as np

df = pd.read_csv('C:/dev/datasets/hotel_reviews/hotel_reviews.csv', delimiter=',', nrows=1000)
# print(df)

spell = SpellChecker()
lemmatizer = WordNetLemmatizer()

# define noun phrase chunk grammar here
# noun_chunk_grammar = "N: {<NN>|<NNS>|<VBG>}"
noun_chunk_grammar = "N-ADJ: {(<JJ>|<JJR>|<JJS>|<RB>|<RBR>|<RBS>)(<NN>|<NNS>|<VBG>)}"
# create noun phrase RegexpParser object here
noun_chunk_parser = RegexpParser(noun_chunk_grammar)

noun_chunked_text = []

corpus_tkns_count = 0

all_nouns = []
all_identifiers = []

for neg in df['Negative_Review']:

    tokenized = word_tokenize(neg)
    corpus_tkns_count += len(tokenized)
    # Spell correction
    # tokenized = [spell.correction(word) for word in tokenized]
    pos_tokenized = pos_tag(tokenized)

    try:
        tree = noun_chunk_parser.parse(pos_tokenized)
        # print(parsed_nouns)

        for subtree in tree.subtrees(filter = lambda t: t.label()=='N-ADJ'):
            # print()
            # print(subtree)
            ls = []
            for item in subtree.leaves():
                # print(item[0].lower())
                # lemmatize only noun part
                if 'NN' in item[1]:
                    lemmatized_noun = lemmatizer.lemmatize(item[0]).lower()
                    ls.append(lemmatized_noun)
                    all_nouns.append(lemmatized_noun)
                else:
                    identifier = item[0].lower()
                    ls.append(identifier)
                    all_identifiers.append(identifier)

            print(ls)
            ls = ' '.join(ls)
            noun_chunked_text.append(ls)

    except:
        pass

noun_chunked_text_counter = Counter(noun_chunked_text)
all_nouns_counter = Counter(all_nouns)
all_identifiers_counter = Counter(all_identifiers)

print(noun_chunked_text)
print(all_nouns)
print(all_identifiers)

phrases_count = []
identifiers_count = []
nouns_count = []
pmi_metric = []

# PMI counter
for phrase in noun_chunked_text:
    splitted = phrase.split()

    phrase_cnt = noun_chunked_text_counter.get(phrase, 0)
    phrases_count.append(phrase_cnt)

    indentifier_cnt = all_identifiers_counter.get(splitted[0], 0)
    identifiers_count.append(indentifier_cnt)

    noun_cnt = all_nouns_counter.get(splitted[1], 0)
    nouns_count.append(noun_cnt)

    prob_collocation = phrase_cnt / corpus_tkns_count
    prob_identifier = indentifier_cnt / corpus_tkns_count
    prob_noun = noun_cnt / corpus_tkns_count

    try:
        pmi = np.log2( prob_collocation / (prob_identifier * prob_noun) )
    except:
        pmi = 0.00
    pmi_metric.append(pmi)

nouns_df = pd.DataFrame()
nouns_df['identifier_plus_noun'] = noun_chunked_text
nouns_df['identifier_count'] = identifiers_count
nouns_df['noun_count'] = nouns_count
nouns_df['phrase_count'] = phrases_count
nouns_df['PMI'] = pmi_metric

# print(nouns_df)
print(nouns_df.sort_values(by=['PMI'], ascending=False))

# print(corpus_tkns_count)

with io.open('data/nouns_from_reviews.csv', 'w', encoding="utf-8", newline='') as f:
    nouns_df.to_csv(f, header=True, index=False)







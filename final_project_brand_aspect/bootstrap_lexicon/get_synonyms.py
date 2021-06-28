from itertools import chain
from nltk.corpus import wordnet
import pandas as pd
import io

df_neg = pd.read_csv('data/final_adjectives_neg_set.csv', delimiter=',', nrows=100)
print(df_neg)

df_pos = pd.read_csv('data/final_adjectives_pos_set.csv', delimiter=',')
print(df_pos)

synonyms = []

def synonyms_search(dataframe):

    neg_ajds = dataframe.tolist()
    done_words = []

    while neg_ajds:
        word = neg_ajds.pop()
        done_words.append(word)
        print(word)
        # todo - adv for pos
        synsets = wordnet.synsets(word, pos=wordnet.ADJ)
        x = [synonyms.append(word.lemma_names()) for word in synsets]

    print(neg_ajds)
    print(done_words)

df_neg['adjective'].apply(lambda x: synonyms_search(dataframe=df_neg['adjective']))

synonyms_flat = list(set([item for sublist in synonyms for item in sublist]))

print(synonyms_flat)

final_df_neg = pd.DataFrame(data=synonyms_flat, columns=['adjectives_synonyms'])

with io.open('data/adjs_neg_synonyms.csv', 'w', encoding="utf-8", newline='') as f:
    final_df_neg.to_csv(f, header=True, index=False)
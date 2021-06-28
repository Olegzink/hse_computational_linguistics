# coding=utf8
import io
import pandas as pd
from nltk import RegexpParser, pos_tag
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize
from spellchecker import SpellChecker
from collections import Counter

df_neg = pd.read_csv('data/adjectives_neg.csv', delimiter=',')
print(df_neg)

df_pos = pd.read_csv('data/adjectives_pos.csv', delimiter=',')
print(df_pos)

final_neg_set = pd.DataFrame(set(df_neg['adjective']) - set(df_pos['adjective']))

# final_neg = pd.merge(df_neg,df_pos, indicator=False, how='left')
# inneg_neg = pd.merge(df_neg,df_pos, indicator=False, how='inner')

# cond = df_pos['adjective'].isin(df_neg['adjective'])
# print(cond)
# final_neg = df_pos.drop(df_pos[cond].index, inplace = True)
# print('final')
# print(final_neg)

print('negative')
final_neg_set = df_neg[~df_neg.isin(df_pos)].dropna()
print('positive')
final_pos_set = df_pos[~df_pos.isin(df_neg)].dropna()

# .query('_merge=="left_only"')
#        .drop('_merge', axis=1)

with io.open('data/final_adjectives_neg_set.csv', 'w', encoding="utf-8", newline='') as f:
       final_neg_set.to_csv(f, header=True, index=False)

with io.open('data/final_adjectives_pos_set.csv', 'w', encoding="utf-8", newline='') as f:
       final_pos_set.to_csv(f, header=True, index=False)

# todo - clean only adj, adv, vbg only
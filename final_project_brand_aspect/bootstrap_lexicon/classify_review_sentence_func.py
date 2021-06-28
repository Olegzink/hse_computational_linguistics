import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import RegexpParser, pos_tag
import os.path as path

def classify_phrase(phrase):

    main_path = path.abspath(path.join(__file__, ".."))

    segments_df = pd.read_csv(f"{main_path}/data/thematic_lexicon_prod_new.csv", delimiter=',')

    lemmatizer = WordNetLemmatizer()

    def lemmatize(text):
        '''lemmatizes text for the given pos tags - NN,VB,JJ'''

        wnl = WordNetLemmatizer()
        for word, tag in pos_tag(word_tokenize(text)):

            if tag.startswith("NN"):
                yield wnl.lemmatize(word, pos='n')
            elif tag.startswith('VB'):
                yield wnl.lemmatize(word, pos='v')
            elif tag.startswith('JJ'):
                yield wnl.lemmatize(word, pos='a')
            else:
                yield word

    tokens = list(lemmatize(phrase))
    pos_tokens = pos_tag(tokens)

    def extract_noun_phrases(pos_tokens):

        # classify_phrase(phrase)
        # '+' means one or more
        grammar = "NP: {(<JJ>+<NN>)|(<JJ>+<NNS>)|(<JJR>+<NN>)|(<JJR>+<NNS>)|(<JJS>+<NN>)|(<JJS>+<NNS>)|(<RB>+<NN>)|(<RB>+<NNS>)|(<JJ>+<VBG>)|(<JJR>+<VBG>)|(<JJS>+<VBG>)}"

        chunk_parser = nltk.RegexpParser(grammar)
        tree = chunk_parser.parse(pos_tokens)

        nouns = []
        nouns_chunked = []
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            ls = []
            for item in subtree.leaves():
                (word, tag) = item
                if tag == 'NN' or tag == 'NNS' or tag == 'VBG':
                    nouns.append(word)
                lemmatized_noun = lemmatizer.lemmatize(item[0]).lower()
                ls.append(lemmatized_noun)
            ls = ' '.join(ls)
            nouns_chunked.append(ls)

        print(nouns_chunked)
        print(nouns)
        return nouns

    def extact_raw_nouns(pos_tokens):

        # if not found nouns with markers. Take first noun from sentence
        grammar = "NOUN: {<NN>|<NNS>|<VBG>}"

        chunk_parser = nltk.RegexpParser(grammar)
        tree = chunk_parser.parse(pos_tokens)

        nouns = []
        nouns_chunked = []
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NOUN'):
            ls = []
            for item in subtree.leaves():
                (word, tag) = item
                if tag == 'NN' or tag == 'NNS' or tag == 'VBG':
                    nouns.append(word)
                lemmatized_noun = lemmatizer.lemmatize(item[0]).lower()
                ls.append(lemmatized_noun)
            ls = ' '.join(ls)
            nouns_chunked.append(ls)

        return nouns

    nouns_chunked = extract_noun_phrases(pos_tokens)
    raw_nouns = extact_raw_nouns(pos_tokens)

    categories = set()

    # if found nouns with emotional markers 'good breakfast'
    if nouns_chunked:

        print()
        print('=============')
        print('Find category for marked noun: ADJ + NN')
        print('=============')

        for key in nouns_chunked:
            print()
            print('keyword:')
            print(key)
            for col in segments_df:
                found = segments_df[col].astype(str).str.match(fr"\b{key}\b", na=False)
                if found.any() == True:
                    print('column:')
                    print(col)
                    categories.add(col)
                    # stop checking other columns for a keyword. Take first occurence
                    break

            # try:
            #     col_name = segments_df.columns[segments_df.isin([key]).any()]
            #     # print(col_name)
            #     categories.add(col_name[0])
            # except:
            #     categories.add('general')

    if not categories:

        # if not found nouns with markers. Take first noun from sentence and find the category
        print()
        print('=============')
        print('Find category for raw noun: NN')
        print('=============')

        for key in raw_nouns:
            print()
            print('keyword:')
            print(key)
            for col in segments_df:
                found = segments_df[col].astype(str).str.match(fr"\b{key}\b", na=False)
                if found.any() == True:
                    print('column:')
                    print(col)
                    categories.add(col)
                    # stop checking other columns for a keyword. Take first occurence
                    break

    if not categories:
        categories.add('general')

    print(categories)

    # noun_chunk_grammar = "N: {<NN>|<NNS>|<VBG>}"
    # noun_chunk_grammar = "NN: {<NN>|<NNS>|<NNP>|<VBN>|<VBG>}"
    #
    # # create noun phrase RegexpParser object here
    # noun_chunk_parser = RegexpParser(noun_chunk_grammar)

    # tokenized = word_tokenize(phrase)

    # tokenized = [spell.correction(word) for word in tokenized]
    # pos_tokenized = pos_tag(tokenized)
    #
    # nouns_chunked = []
    # try:
    #     tree = noun_chunk_parser.parse(pos_tokenized)
    #     # print(parsed_nouns)
    #     print(tree)
    #
    #     for subtree in tree.subtrees(filter = lambda t: t.label()=='NN'):
    #         # print()
    #         # print(subtree)
    #         ls = []
    #         for item in subtree.leaves():
    #             lemmatized_noun = lemmatizer.lemmatize(item[0]).lower()
    #             ls.append(lemmatized_noun)
    #         ls = ' '.join(ls)
    #         nouns_chunked.append(ls)
    #
    # except:
    #     pass

    return list(categories)

if __name__ == '__main__':

    phrase = '''Breakfast was substantial , and suited all tastes '''

    classify_phrase(phrase)

    # import nltk
    # import re
    # from nltk.stem import WordNetLemmatizer
    # from nltk.tokenize import word_tokenize
    # from nltk import RegexpParser, pos_tag
    # import os.path as path
    #
    # import spacy
    # nlp = spacy.load('en_core_web_sm')
    # doc = nlp('Way overpriced and the small deposit for the minibar to which I refused as allergic to tasty alcohol.')
    #
    # noun_adj_pairs = {}
    # for chunk in doc.noun_chunks:
    #     adj = []
    #     noun = ""
    #     for tok in chunk:
    #         if tok.pos_ == "NOUN":
    #             noun = tok.text
    #         if tok.pos_ == "ADJ":
    #             adj.append(tok.text)
    #     if noun:
    #         noun_adj_pairs.update({noun:adj})
    #
    # print()
    # print(noun_adj_pairs)






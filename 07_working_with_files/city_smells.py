import nltk
import string
import statistics
import re
import pymorphy2
import io
import json

def text_preprocess(text, lower=True, delete_punct=True):
    """The function preprocess the text.

    Args and params:
        ---------------
        text: str
        Text to process.

        lower: True/False
        Converts a text to a lowercase.

        delete_punct: True/False
        Delete or not the punctuation.
    """

    if lower:

        text = text.lower()

    if delete_punct:

        # note! - adding additional symbols to string.punctuation - '«»—', as it doesn't cover them by default
        text = text.translate(str.maketrans('', '', string.punctuation + r'«»—'))

    return text


def text_analysis(filename):
    """
    The function analyses the text and creates a json file with statistics in the 'data/' folder.

    Args and params:
    ---------------
        filename: str
            filename to process
    """

    with open('{}/{}'.format('data', filename), 'r', encoding='utf-8') as myfile:

        text = myfile.read()
        # substitute ':' for '.' in the sentences end to avoid the pentultimate sentence 'в Барселоне на улице Бальмес запах еды преобладает:', causing wrong sentence tokenizing
        text = re.sub(r':\n', '.\n', text)
        sentences = nltk.tokenize.sent_tokenize(text)
        print(sentences)

        ##################
        # Counting average sentence length by characters size
        ##################

        # length of sentences - by characters size
        sent_chars_len = [len(x) for x in sentences]

        # or simply - import statistics, then statistics.mean(lengths)
        avg_sent_len_by_char = sum(sent_chars_len) / len(sent_chars_len)

        ##################
        # Counting average sentence length by word size
        ##################

        sent_word_tokenized = [nltk.tokenize.word_tokenize(text_preprocess(sent, lower=True, delete_punct=True), language="russian") for sent in sentences]

        # length of sentences - by words size
        sent_words_len = [len(x) for x in sent_word_tokenized]

        avg_sent_len_by_word = sum(sent_words_len) / len(sent_words_len)

        ##################
        # Counting average words size in all text
        ##################

        # taking already tokenized text 'sent_word_tokenized' (it is a list of lists) and making it a flat list:
        words_flat_list = [word for sublist in sent_word_tokenized for word in sublist]

        # length of words - by chars size
        words_len = [len(x) for x in words_flat_list]

        avg_word_len = statistics.mean(words_len)

        ##################
        # Counting max word size > min word size
        ##################

        words_sorted = sorted(words_flat_list, key=len)
        min_len_word = words_sorted[0]
        max_len_word = words_sorted[-1]
        word_max_vs_min_len_coeff = len(max_len_word) / len(min_len_word)

        ##################
        # Counting max sentence size > min sentence size
        ##################

        # [0:-4] - not taking into account last section: "Источники. Нелли Бурцева и т.д.", only the text itself
        sentences_sorted = sorted(sent_word_tokenized[0:-4], key=len)
        min_len_sent = sentences_sorted[0]
        max_len_sent = sentences_sorted[-1]
        # min_len_sent_tokenized = nltk.tokenize.word_tokenize(min_len_sent)
        # max_len_sent_tokenized = nltk.tokenize.word_tokenize(max_len_sent)
        sent_max_vs_min_len_coeff = len(max_len_sent) / len(min_len_sent)

        ##################
        # Counting average punctuation marks number
        ##################

        sentences_punct_len = []
        punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""" + r'«»—'
        for sent in sentences:

            punct_counter = 0

            for mark in punctuation:
                regex = '\{}'.format(mark)
                match = re.findall(regex, sent)
                if match:
                    punct_counter += len(match)

            sentences_punct_len.append(punct_counter)

        avg_punctuation_marks_len = statistics.mean(sentences_punct_len)

        ##################
        # Counting unique words
        ##################

        unique_words_set = set()
        morph = pymorphy2.MorphAnalyzer()
        for word in words_flat_list:
            word = morph.parse(word)[0].normal_form
            unique_words_set.add(word)
        print(unique_words_set)

        unique_words_proportion = int(len(unique_words_set)*100/len(words_flat_list))

    ##################
    # Preparing data for json export
    ##################

    data = {}
    data['sentence_stats'] = []
    data['words_stats'] = []
    data['sentence_stats'].append({
        'avg_sent_len_by_char': int(avg_sent_len_by_char),
        'avg_sent_len_by_word': int(avg_sent_len_by_word),
        'max_length_sentence': len(max_len_sent),
        'min_len_sent': len(min_len_sent),
        'sent_max_vs_min_len_coeff': int(sent_max_vs_min_len_coeff),
        'avg_punctuation_marks_len': int(avg_punctuation_marks_len)
    })

    data['words_stats'].append({
        'avg_word_len': int(avg_word_len),
        'max_len_word': len(max_len_word),
        'min_len_word': len(min_len_word),
        'word_max_vs_min_len_coeff': int(word_max_vs_min_len_coeff),
        'all words count': len(words_flat_list),
        'unique_words_count': len(unique_words_set),
        'unique_words_proportion': unique_words_proportion,

    })

    # using io to avoid ascii and encoding errors
    with io.open('data/data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


    print()
    print('Average sentence length by characters size:', int(avg_sent_len_by_char))
    print('Average sentence length by words size:', int(avg_sent_len_by_word))
    print('Max length sentence and its size:', len(max_len_sent))
    print('Min length sentence and its size:', len(min_len_sent))
    print('The longest sentence is longer than the shortest sentence in a coefficient of:', int(sent_max_vs_min_len_coeff))
    print('Average punctuations marks length in the text:', int(avg_punctuation_marks_len))

    print()
    print('Average word length in the text:', int(avg_word_len))
    print('Max length word and its size:', '\'' + max_len_word + '\'', len(max_len_word))
    print('Min length word and its size:', '\'' + min_len_word + '\'', len(min_len_word))
    print('The longest word is longer than the shortest word in a coefficient of:', int(word_max_vs_min_len_coeff))
    print('Num of words in the text:', len(words_flat_list))
    print('Num of unique words', len(unique_words_set))
    print('Unique words to all words proportion:', str(unique_words_proportion)+'%')


if __name__ == "__main__":

    text_analysis(filename='city_smells.txt')

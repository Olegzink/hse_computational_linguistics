from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import json
from django.http import JsonResponse
from reviews.models import Reviews, Phrases
import pandas as pd
import os
import os.path as path
from collections import namedtuple
import datetime
from datetime import date
from .utils import simple_preprocess, calculate_sentiment
from production.bootstrap_lexicon.classify_review_sentence_func import classify_phrase
from .utils import intention_finder, review_sent_tokenize
from django.shortcuts import redirect
from lexicons.models import Thematic_tokens, Sentiment_tokens
from statistics import mean

# todo - ввести метрики точности - с чем сравниваем результат? Например, с каким-то эталонным датасетом (показать это на сайте).
# todo Ввести neutral помимо positive/negative.
# todo инверторы - та лексика, которая из позитива делает негатив и обратно - отрицания и приставки без. Отдельно глагол и отдельно глагол с отрицанием. + лексика интенсификаторы - очень плохой и т.д. учесть в общем рассчете. + нейтрализатор - модальные слова "могло бы быть, возможно...". ФАктологические слова или фразы - "не выдали рецепт", "в номере увидели таракана" - здесь нет позит или негат, но нам понятно, что это. Нужно учитывать.
# todo отдельно сделать вручную оценку поулченных результатов также.
# todo - loglikelyhood / chisquare - используется для выделения специфичной лексики
# todo - flake8 - lib for code review
# посмотреть методы контент анализа (спросить Светлану Юрьевну, что почитать - Баранов ПРикладная лингвистика). - # пример анализ концепта - что рядом с концептом "нац идея" в тексте было упомянуто. В таких-то годах это ассоциировалось с Православием, в другой с демократией и т.д. Взять в диссертацию!
# статья Лукашевич по выделению тепминов в предметной области.

# main_path = path.abspath(path.join(__file__, ""))
# print(main_path)

actual_timestamp = datetime.datetime.now()

# helper function
def db_save(phrase_text, review_id, sentiment, aspect, intention):

    phrases_model = Phrases(phrase_text = phrase_text, sentiment = sentiment, review_id = review_id, intention = eval(str(intention)), aspect = aspect)

    phrases_model.save()


def calculate_sentiment_by_phrases(instance_id):

    phrases = Phrases.objects.filter(review_id__in=[instance_id])

    sentim_scores = []
    for x in phrases:

        if x.sentiment == 'pos':
            sentim_scores.append(1)
        elif x.sentiment == 'neu':
            sentim_scores.append(0.25)
        else:
            sentim_scores.append(-1)

    if mean(sentim_scores) > 0:
        overall_sentiment = 'pos'
    else:
        overall_sentiment = 'neg'

    return overall_sentiment


def process_csv(request):

    user = request.user

    # reviews = Reviews.objects.all()[:20]

    df = pd.read_csv('C:/dev/datasets/hotel_reviews/hotel_reviews.csv', delimiter=',', nrows=10)
    neg = df['Negative_Review']

    def db_process(review):

        from .utils import simple_preprocess

        review = simple_preprocess(review)

        print(review)
        review_instance = Reviews(review_text = review, brand_name = 'Astoria', to_user = user, timestamp = actual_timestamp)
        review_instance.save()

        review_db_obj = namedtuple('review_from_db' , ['review_id', 'review_text'])
        current_db_obj = review_db_obj(review_instance.review_id, review_instance.review_text)

        tokenized_phrases = review_sent_tokenize(review_instance.review_text, current_db_obj = current_db_obj)

        [db_save(phrase_text = q['phrase'], review_id = q['review_id'], aspect = classify_phrase(q['phrase']), sentiment = calculate_sentiment(q['phrase']), intention = intention_finder(q['phrase'])) for q in tokenized_phrases]

        # updating the field 'overall_sentiment' for a current review obj
        review_update_instance = Reviews.objects.get(review_id = review_instance.review_id)
        review_update_instance.overall_sentiment = calculate_sentiment_by_phrases(review_instance.review_id)
        review_update_instance.save()

        return review

    neg.apply(lambda x: db_process(x))

    return render(request, 'data_process/process_csv.html', {'user': user, 'neg': neg})


def process_phrases(request):

    user = request.user

    reviews = Reviews.objects.all()[:5]

    for x in reviews:

        review_db_obj = namedtuple('review_from_db' , ['review_id', 'review_text'])
        current_db_obj = review_db_obj(x.review_id, x.review_text)

        tokenized_phrases = review_sent_tokenize(x.review_text, current_db_obj = current_db_obj)

        [db_save(phrase_text = q['phrase'], review_id = q['review_id'], aspect = classify_phrase(q['phrase']), sentiment=calculate_sentiment(q['phrase']), intention = intention_finder(q['phrase'])) for q in tokenized_phrases]

    return render(request, 'data_process/process_phrases.html', {'reviews': reviews,})


def submit_review(request):

    user = request.user

    if request.is_ajax() and request.method == "POST": #os request.GET()
        print('got some AJAX request!!!!!!!!!!!')

        got_ajax_data = request.body
        got_ajax_data = got_ajax_data.decode("utf-8")
        got_ajax_dict = eval(got_ajax_data)
        print(got_ajax_dict)

        review_text_ajax = got_ajax_dict.get('reviewText')
        classification_method = got_ajax_dict.get('classificationMethod')

        # if review_text_ajax:

        print('got_request: ', review_text_ajax)

        # preprocessing and saving review
        review_instance = Reviews(review_text = simple_preprocess(review_text_ajax), brand_name='Astoria', to_user = user, timestamp = actual_timestamp)
        review_instance.save()
        print(review_instance.review_id)

        # redirect to app: review to the view: current_review
        # return redirect('reviews:current_review', review_id = reviews_model.review_id)

        # preprocessing phrases
        review_db_obj = namedtuple('review_from_db' , ['review_id', 'review_text'])
        current_db_obj = review_db_obj(review_instance.review_id, review_instance.review_text)

        tokenized_phrases = review_sent_tokenize(review_instance.review_text, current_db_obj = current_db_obj)

        [db_save(phrase_text = q['phrase'], review_id = q['review_id'], aspect = classify_phrase(q['phrase']), sentiment=calculate_sentiment(q['phrase'], classification_method), intention = intention_finder(q['phrase'])) for q in tokenized_phrases]

        # updating the field 'overall_sentiment' for a current review obj
        review_update_instance = Reviews.objects.get(review_id = review_instance.review_id)
        review_update_instance.overall_sentiment = calculate_sentiment_by_phrases(review_instance.review_id)
        review_update_instance.save()

        return JsonResponse({
                'response_review_id': review_instance.review_id,
                'redirect_url': f'/reviews/{review_instance.review_id}',
                'success': True,
            })

    # else:
    #     return JsonResponse({"error": "there was an error"})

    return render(request, 'data_process/submit_review.html', {})


def upload_thematic_tokens_to_db(request, token_class):

    column = token_class

    df = pd.read_csv('C:/dev/sandbox/brand_aspect/production/bootstrap_lexicon/data/thematic_words_norm.csv', delimiter=',', nrows=50, na_values="NaN")
    df = df.dropna()

    # for token in df[column[0]]:
    #     print(token)
    #     token_instance = Thematic_tokens(token = token, token_class = column[0])
    #     token_instance.save()

    def db_save(token):

        token_instance = Thematic_tokens(token = token, token_class = column)
        token_instance.save()
        print(token)
        return token

    df[column].apply(lambda x: db_save(x))

    return HttpResponse('done')



def upload_sentiment_tokens_to_db(request):

    sentiment_class = 'negative'

    df = pd.read_csv('C:/dev/sandbox/brand_aspect/production/bootstrap_lexicon/data/final_adjectives_neg_set.csv', delimiter=',', nrows=None, na_values="NaN")
    df = df.dropna()

    def db_save(adjective, adj_count):

        try:
            token_instance  = Sentiment_tokens.objects.get(token = adjective)

        except Sentiment_tokens.DoesNotExist:

            token_instance  = Sentiment_tokens(token = adjective,
                                               token_sentiment = sentiment_class,
                                               token_count = adj_count)
            token_instance.save()

        print(adjective, adj_count)

    df.apply(lambda x: db_save(x.adjective, x.adj_count), axis=1)

    return HttpResponse('done')
from django.shortcuts import render
import pandas as pd
from reviews.models import Reviews, Phrases
import datetime
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from lexicons.models import Thematic_tokens

# import tables
from .tables import ReviewsAll


def index(request):

    return render(request, 'reviews/index.html', {})


def process_df(request):

    actual_timestamp = datetime.datetime.now()
    user = request.user

    df = pd.read_csv('C:/dev/datasets/hotel_reviews/hotel_reviews.csv', delimiter=',', nrows=20)
    neg = df['Negative_Review']

    def db_save(review):
        print(review)
        reviews_model = Reviews(review_text=review, brand_name='Astoria', to_user=user, timestamp=actual_timestamp)
        # reviews_model.save()
        return review

    neg.apply(lambda x: db_save(x))

#   todo: return neg in render


# Create your views here.
def reviews(request, sentiment = 'None'):

    user = request.user

    if sentiment == 'positive':
        reviews = Reviews.objects.filter(overall_sentiment__in=['pos'])
        print('positive')
        print(len(reviews))
    elif sentiment == 'negative':
        reviews = Reviews.objects.filter(overall_sentiment__in=['neg'])
        print('positive')
        print(len(reviews))
    else:
        reviews = Reviews.objects.all()[:20]
        print('all')
        print(len(reviews))

    reviews_len = len(reviews)

    donut_chart_data = [{'review_type': 'positive', 'count': 0}, {'review_type': 'negative', 'count': 0}]

    reviews_data = []
    for x in reviews:
        reviews_dict = {
            "review_text": x.review_text,
            "brand_name": x.brand_name,
            "review_id": x.review_id,
            "overall_sentiment": x.overall_sentiment,
            "timestamp": x.timestamp.strftime("%Y-%m-%d"),
        }
        reviews_data.append(reviews_dict)

        if x.overall_sentiment == 'pos':
            donut_chart_data[0]['count'] += 1
        else:
            donut_chart_data[1]['count'] += 1

    table = ReviewsAll(reviews_data)
    RequestConfig(request).configure(table)

    return render(request, 'reviews/all.html', {'user': user, 'reviews_data': reviews_data, 'reviews':reviews, 'reviews_len': reviews_len, 'table': table, 'sentiment': sentiment, 'donut_chart_data': donut_chart_data})


def current_review(request, review_id):

    user = request.user
    review = Reviews.objects.get(review_id=review_id)

    phrases = Phrases.objects.filter(review_id__in=[review_id])
    phrases_len = len(phrases)

    aspects_set = set()
    for x in phrases:
        for y in eval(x.aspect):
            aspects_set.add(y)

    aspects_list = list(aspects_set)

    # getting intentions

    intentions_list_all = []
    for x in phrases:
        # [{'food': 'get free coffee', 'service': 'change concierge'}]
        for y in eval(x.intention):
            for k,v in y.items():
                intentions_list_all.append(v)

    return render(request, 'reviews/current.html', {'user': user, 'review': review, 'phrases': phrases, 'aspects_list': aspects_list, 'phrases_len': phrases_len, 'intentions_list_all': intentions_list_all})


def aspects_all(request):

    user = request.user

    phrases_all = Phrases.objects.all()

    room_dict = {'aspect_name': 'room', 'total_phrases_pos': 0, 'total_phrases_neg': 0}
    bath_dict = {'aspect_name': 'bath', 'total_phrases_pos': 0, 'total_phrases_neg': 0}
    food_dict = {'aspect_name': 'food', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }
    design_dict = {'aspect_name': 'design', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }
    health_dict = {'aspect_name': 'health', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }
    location_dict = {'aspect_name': 'location', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }
    payment_dict = {'aspect_name': 'payment', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }
    hotel_dict = {'aspect_name': 'hotel', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }
    staff_dict = {'aspect_name': 'staff', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }
    services_dict = {'aspect_name': 'services', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }

    for x in phrases_all:
        if x.sentiment in 'pos':
            print(x.sentiment)
            for y in eval(x.aspect):
                # room_dict = {'aspect_name': 'room', 'total_phrases_pos': 0, 'total_phrases_neg': 0 }
                if 'room' in y:
                    room_dict['total_phrases_pos'] += 1
                if 'bath' in y:
                    bath_dict['total_phrases_pos'] += 1
                if 'food' in y:
                    food_dict['total_phrases_pos'] += 1
                if 'design' in y:
                    design_dict['total_phrases_pos'] += 1
                if 'health' in y:
                    health_dict['total_phrases_pos'] += 1
                if 'locations' in y:
                    location_dict['total_phrases_pos'] += 1
                if 'payment' in y:
                    payment_dict['total_phrases_pos'] += 1
                if 'hotel' in y:
                    hotel_dict['total_phrases_pos'] += 1
                if 'staff' in y:
                    staff_dict['total_phrases_pos'] += 1
                if 'service' in y:
                    services_dict['total_phrases_pos'] += 1
        else:
            for y in eval(x.aspect):

                if 'room' in y:
                    room_dict['total_phrases_neg'] += 1
                if 'bath' in y:
                    bath_dict['total_phrases_neg'] += 1
                if 'food' in y:
                    food_dict['total_phrases_neg'] += 1
                if 'design' in y:
                    design_dict['total_phrases_neg'] += 1
                if 'health' in y:
                    health_dict['total_phrases_neg'] += 1
                if 'locations' in y:
                    location_dict['total_phrases_neg'] += 1
                if 'payment' in y:
                    payment_dict['total_phrases_neg'] += 1
                if 'hotel' in y:
                    hotel_dict['total_phrases_neg'] += 1
                if 'staff' in y:
                    staff_dict['total_phrases_neg'] += 1
                if 'service' in y:
                    services_dict['total_phrases_neg'] += 1

    bar_chart_aspects_all_data = [room_dict, bath_dict, food_dict, design_dict, health_dict, location_dict, payment_dict, hotel_dict, staff_dict, services_dict]

    total_neg_phrases = sum([tok['total_phrases_neg'] for tok in bar_chart_aspects_all_data])
    total_pos_phrases = sum([tok['total_phrases_pos'] for tok in bar_chart_aspects_all_data])

    # fetch all token classes - room, food, etc.
    token_classes = Thematic_tokens.objects.values('token_class').distinct()
    token_class_list = [[v for k,v in group.items()] for group in token_classes]
    token_class_flat_list = [item for sublist in token_class_list for item in sublist]

    return render(request, 'reviews/aspects_all.html', {'user': user, 'bar_chart_aspects_all_data': bar_chart_aspects_all_data, 'total_neg_phrases':  total_neg_phrases, 'total_pos_phrases': total_pos_phrases, 'token_class_flat_list': token_class_flat_list})

def aspects_negative(request):

    user = request.user

    negative_phrases = Phrases.objects.filter(sentiment__in=['neg'])

    # fetch all token classes - room, food, etc.
    token_classes = Thematic_tokens.objects.values('token_class').distinct()
    token_class_list = [[v for k,v in group.items()] for group in token_classes]
    token_class_flat_list = [item for sublist in token_class_list for item in sublist]

    return render(request, 'reviews/aspects_negative.html', {'user': user, 'token_class_flat_list': token_class_flat_list, 'negative_phrases': negative_phrases})


def aspects_negative_by_aspect(request, aspect):

    user = request.user

    negative_phrases = Phrases.objects.filter(sentiment__in=['neg']).filter(aspect__icontains=aspect)

    # fetch all token classes - room, food, etc.
    token_classes = Thematic_tokens.objects.values('token_class').distinct()
    token_class_list = [[v for k,v in group.items()] for group in token_classes]
    token_class_flat_list = [item for sublist in token_class_list for item in sublist]

    return render(request, 'reviews/aspects_negative.html', {'user': user, 'aspect': aspect, 'token_class_flat_list': token_class_flat_list, 'negative_phrases': negative_phrases})

def reviews_by_aspects(request, aspect):

    user = request.user

    phrases = Phrases.objects.filter(aspect__icontains=aspect)
    phrases_len = len(phrases)

    phrases_neg = Phrases.objects.filter(aspect__icontains=aspect).filter(sentiment__in=['neg']).count()
    phrases_pos = Phrases.objects.filter(aspect__icontains=aspect).filter(sentiment__in=['pos']).count()

    # fetch all token classes - room, food, etc.
    token_classes = Thematic_tokens.objects.values('token_class').distinct()
    token_class_list = [[v for k,v in group.items()] for group in token_classes]
    token_class_flat_list = [item for sublist in token_class_list for item in sublist]

    aspects_list = []
    for x in phrases:
        for y in eval(x.aspect):
            aspects_list.append(y)
    print(aspects_list)

    phrases_donut_chart_data = []

    phrases_neg_dict = {
        "pub_type": "Negative phrases",
        "count": phrases_neg,
    }
    phrases_pos_dict = {
        "pub_type": "Positive phrases",
        "count": phrases_pos,
    }

    phrases_donut_chart_data.append(phrases_neg_dict)
    phrases_donut_chart_data.append(phrases_pos_dict)

    print(phrases_neg)
    print(phrases_pos)
    print(phrases_donut_chart_data)

    return render(request, 'reviews/reviews_by_aspects.html', {'user': user, 'phrases': phrases, 'aspects_list': aspects_list, 'phrases_len': phrases_len, 'aspect': aspect, 'phrases_neg':phrases_neg, 'phrases_pos': phrases_pos, 'phrases_donut_chart_data': phrases_donut_chart_data, 'token_class_flat_list': token_class_flat_list })


def intentions_all(request):

    user = request.user

    intentions_neg = Phrases.objects.filter(sentiment__in=['neg', 'pos'])

    room_list = []
    bath_list = []
    food_list = []
    design_list = []
    health_list = []
    location_list = []
    payment_list = []
    hotel_list = []
    staff_list = []
    services_list = []

    for x in intentions_neg:
        # [{'food': 'get free coffee', 'service': 'change concierge'}]
        print(eval(x.intention))
        for y in eval(x.intention):

            if 'room' in y:
                room_list.append(y['room'])
            if 'bath' in y:
                bath_list.append(y['bath'])
            if 'food' in y:
                food_list.append(y['food'])
            if 'design' in y:
                design_list.append(y['design'])
            if 'health' in y:
                health_list.append(y['health'])
            if 'locations' in y:
                location_list.append(y['location'])
            if 'payment' in y:
                payment_list.append(y['payment'])
            if 'hotel' in y:
                hotel_list.append(y['hotel'])
            if 'staff' in y:
                staff_list.append(y['staff'])
            if 'service' in y:
                services_list.append(y['service'])

    bar_chart_all_data = [
        {'intention_name': 'room', 'total_intentions': len(room_list) },
        {'intention_name': 'food', 'total_intentions': len(food_list) },
        {'intention_name': 'design', 'total_intentions': len(design_list) },
        {'intention_name': 'health', 'total_intentions': len(health_list) },
        {'intention_name': 'location', 'total_intentions': len(location_list) },
        {'intention_name': 'payment', 'total_intentions': len(payment_list) },
        {'intention_name': 'hotel', 'total_intentions': len(hotel_list) },
        {'intention_name': 'staff', 'total_intentions': len(staff_list) },
        {'intention_name': 'services', 'total_intentions': len(services_list) }]

    return render(request, 'reviews/intentions_all.html', {'user': user, 'bar_chart_all_data': bar_chart_all_data})


def intentions_positive(request):
    user = request.user
    return render(request, 'reviews/intentions_positive.html', {'user': user, })


def intentions_negative(request):
    user = request.user
    return render(request, 'reviews/intentions_negative.html', {'user': user, })
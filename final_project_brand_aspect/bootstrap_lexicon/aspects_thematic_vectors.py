import pandas as pd
import io
import gensim
from gensim.models import Word2Vec
from gensim.test.utils import datapath
from gensim.models import KeyedVectors


# todo add aspect service/amenitites

# Load pre-trained Word2Vec model.
# model = gensim.models.Word2Vec.load("C:/dev/datasets/word2vec/GoogleNews-vectors-negative300.bin.gz")

model = KeyedVectors.load_word2vec_format(datapath("C:/dev/datasets/word2vec/GoogleNews-vectors-negative300.bin.gz"), binary=True)

# gensim.models.KeyedVectors.load_word2vec_format
# model = Word2Vec.load_word2vec_format(

basic_aspects = {'room': ['room', 'interior', 'bed', 'sofa', 'single room', 'double room'],
                 'bath': ['bath', 'toilet', 'bathroom'],
     'food': ['food', 'coffee', 'tea', 'restaurant', 'cafe', 'pasta', 'pizza'],
     'design': ['design', 'interior'],
     'health': ['health', 'apnea', 'allergy', 'illness', 'bronchitis'],
     'location': ['location', 'street', 'address', 'transport'],
     'payment': ['price', 'payment', 'money', 'bank', 'fund', 'dollar', 'euro', 'client', 'buyer'],
     'hotel': ['motel', 'hotel', 'hostel'],
     'staff':['staff', 'concierge', 'personnel', 'employee'] }

room_similar = []
bath_similar = []
food_similar = []
design_similar = []
health_similar = []
location_similar = []
payment_similar = []
hotel_similar = []
staff_similar = []

for key,val in basic_aspects.items():
    for word in val:
        print('processing:', word)
        try:
            similar = model.most_similar(positive=[word], topn=2000)
            for tpl in similar:
                print(tpl[0])
                eval(f'{key}_similar').append(tpl[0])
        except:
            pass

print()
print(room_similar)

room_similar_df = pd.DataFrame(data=room_similar, columns=['room'])
bath_similar_df = pd.DataFrame(data=bath_similar, columns=['bath'])
food_similar_df = pd.DataFrame(data=food_similar, columns=['food'])
design_similar_df = pd.DataFrame(data=design_similar, columns=['design'])
health_similar_df = pd.DataFrame(data=health_similar, columns=['health'])
location_similar_df = pd.DataFrame(data=location_similar, columns=['location'])
payment_similar_df = pd.DataFrame(data=payment_similar, columns=['payment'])
hotel_similar_df = pd.DataFrame(data=hotel_similar, columns=['hotel'])
staff_similar_df = pd.DataFrame(data=staff_similar, columns=['staff'])

final_df = pd.concat([room_similar_df, bath_similar_df, food_similar_df, design_similar_df, health_similar_df, location_similar_df, payment_similar_df, hotel_similar_df, staff_similar_df], axis=1)

with io.open('data/thematic_words.csv', 'w', encoding="utf-8", newline='') as f:
    final_df.to_csv(f, header=True, index=False)


# helper func for thematic lexicon cleaning

import pandas as pd
import re

df = pd.read_csv('C:/dev/sandbox/brand_aspect/production/bootstrap_lexicon/data/thematic_words_norm_may.csv', delimiter=',')
print(df['room'])

room_word_set = set()
bath_word_set = set()
food_word_set = set()
design_word_set = set()
location_word_set = set()
payment_word_set = set()
staff_word_set = set()
amenities_word_set = set()
general_word_set = set()
health_word_set = set()

def norm_words(col, word_set):

    for wrd in df[col]:
        wrd = re.sub(' +', ' ', str(wrd)).lower()

        word_set.add(wrd)

room_word_set.add('room')
room_word_set.add('pillow')
room_word_set.add('floor')


norm_words('room', room_word_set)
norm_words('bath', bath_word_set)
norm_words('food', food_word_set)
norm_words('design', design_word_set)
norm_words('location', location_word_set)
norm_words('payment', payment_word_set)
norm_words('staff', staff_word_set)
norm_words('amenities', amenities_word_set)
norm_words('general', general_word_set)
norm_words('health', health_word_set)

print(room_word_set)

room_df = pd.DataFrame(list(room_word_set), columns=['room'])
bath_df = pd.DataFrame(list(bath_word_set), columns=['bath'])
food_df = pd.DataFrame(list(food_word_set), columns=['food'])
design_df = pd.DataFrame(list(design_word_set), columns=['design'])
location_df = pd.DataFrame(list(location_word_set), columns=['location'])
payment_df = pd.DataFrame(list(payment_word_set), columns=['payment'])
staff_df = pd.DataFrame(list(staff_word_set), columns=['staff'])
amenities_df = pd.DataFrame(list(amenities_word_set), columns=['amenities'])
general_df = pd.DataFrame(list(general_word_set), columns=['general'])
health_df = pd.DataFrame(list(health_word_set), columns=['health'])
print(bath_df)
print(food_df)


frames = [room_df, bath_df, food_df, design_df, location_df, payment_df, staff_df, amenities_df, general_df, health_df]

result_df = pd.concat(frames, axis=1, ignore_index=True)

columns=['room', 'bath', 'food', 'design', 'location', 'payment', 'staff', 'amenities', 'general',]
result_df.columns = columns
print(result_df)

result_df.to_csv(f'datasets/thematic_lexicon_prod.csv', sep=',')

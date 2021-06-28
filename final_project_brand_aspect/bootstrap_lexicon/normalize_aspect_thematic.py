import pandas as pd
import io
import re
from nltk.stem import WordNetLemmatizer

df = pd.read_csv('data/thematic_words.csv', delimiter=',', nrows=None)

lemmatizer = WordNetLemmatizer()

def normalize_words(str):

    result = str.lower()
    result = re.sub('_', ' ', str)
    result = lemmatizer.lemmatize(result)

    return result

df['room'] = df['room'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)
df['bath'] = df['bath'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)
df['food'] = df['food'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)
df['design'] = df['design'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)
df['health'] = df['health'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)
df['location'] = df['location'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)
df['payment'] = df['payment'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)
df['hotel'] = df['hotel'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)
df['staff'] = df['staff'].apply(lambda x: normalize_words(x) if pd.notnull(x) else x)

print(df)

with io.open('data/thematic_words_norm.csv', 'w', encoding="utf-8", newline='') as f:
    df.to_csv(f, header=True, index=False)
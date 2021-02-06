import fire
import sqlite3

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import re
import pandas as pd


DEFAULT_DB_RESULTS = '../../reddit-engagement-files/results.db'
FOLLOWED_SUBS = ['codcompetitive']


def preprocess_text(text):
    # remove urls/numbers
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[0-9]+', '', text)
    # expand contractions
    text = re.sub(r"'ve'", ' have', text)
    text = re.sub(r"n't", ' not', text)
    # remove emojis and special characters
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub('[^a-zA-Z0-9]+', ' ', text)
    # remove stop words
    stops = stopwords.words('english')
    text = ' '.join([x for x in text.split() if x not in stops])
    # tokenize and lemmatize
    text = word_tokenize(text)
    lm = WordNetLemmatizer()
    text = [lm.lemmatize(x) for x in text]
    return text
    
def read_activity_batch(db_path, start, end):
    connection = None
    # exploring ways to ensure file not open elsewhere
    try:
        with open(db_path, 'r') as _:
            connection = sqlite3.connect(db_path)
    except IOError:
        print('In use / other issue accessing %s' % db_path)
    # sort by date and preserve other ordering, return subset
    select_all = ''' SELECT * FROM activity;'''
    df_batch = pd.read_sql_query(select_all, connection)
    df_batch.access_time = pd.to_datetime(df_batch.access_time)
    df_batch = df_batch.reset_index().sort_values(by=['access_time', 'index'])
    df_batch = df_batch[df_batch.subreddit.apply(lambda x: x.lower() not in FOLLOWED_SUBS)]
    df_batch = df_batch.drop(['index'], axis=1)
    return df_batch[start:end]
    

def nlp_on_batch():
    raise NotImplemented
    

def store_batch_results():
    raise NotImplemented

    
def setup_model():
    raise NotImplemented
    
    
def main():
    raise NotImplemented
    

if __name__ == '__main__':
    pass
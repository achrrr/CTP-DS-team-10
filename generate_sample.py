import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Download requirements if not installed
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Isolating English stopwords for eventual removal
stopwords_eng = stopwords.words('english')

def lowercase(s: str):
    return s.lower()

def remove_punctuation(s: str):    
    s = re.sub(r'[^\w\s]','',s)
    return s

def remove_stopwords(s: str):
    words = word_tokenize(s)

    valid_words = []
    for word in words:
        if word not in stopwords_eng:
            valid_words.append(word)

    s = ' '.join(valid_words)

    return s

def lemmatize(s: str):
    words = word_tokenize(s)
    lemmatizer = WordNetLemmatizer()

    word_lemmings = []
    for word in words:
        word_lemmings.append(lemmatizer.lemmatize(word))
    
    return ' '.join(word_lemmings)

def pipeline(s: str):
    s = lowercase(s)
    s = remove_punctuation(s)
    s = remove_stopwords(s)
    s = lemmatize(s)
    return s

# Title, Label = {'Real', 'Fake'}
df1 = pd.read_csv('./data/fake_news_data_set.csv')
# title
df2 = pd.read_csv('./data/getting_real_dataset.csv')
# title, label = {0, 1}; 0 for real, 1 for fake
df3 = pd.read_csv('./data/WELFake_Dataset.csv')

# isolate key features
df1 = df1[['Title', 'Label']]
df2 = df2[df2['language'] == 'english']
df2['is_fake'] = 1
df2 = df2[['title', 'is_fake']]
df3 = df3[['title', 'label']]

# reformat dataframes by renaming columns, etc.
df1 = df1.rename(columns={'Title':'headline', 'Label':'is_fake'})
df1['is_fake'] = (df1['is_fake'] == 'Fake').astype(int)

df2 = df2.rename(columns={'title': 'headline'})

df3 = df3.rename(columns={'title':'headline', 'label':'is_fake'})

# merge data sets
merged = df1.merge(df2.merge(df3, how='outer'), how='outer')

# Dropping any duplicates or nulls, applying text cleaning pipeline
merged = merged.drop_duplicates().dropna()
merged['headline'] = merged['headline'].apply(pipeline)
merged.reset_index(drop=True, inplace=True)

# Saving to csv
compression_opts = dict(method='zip',archive_name='sample.csv')
merged.to_csv('./data/sample.zip', index=False, compression=compression_opts)
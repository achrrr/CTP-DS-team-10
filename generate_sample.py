import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def lowercase(s: str):
    return s.lower()

def remove_punctuation(s: str):    
    s = re.sub(r'[^\w\s]','',s)
    return s

def remove_stopwords(s: str):
    # Break the sentence down into a list of words
    words = word_tokenize(s)
    
    # Make a list to append valid words into
    valid_words = []
    
    # Loop through all the words
    for word in words:
        
        # Check if word is not in stopwords
        if word not in stopwords:
            
            # If word not in stopwords, append to our valid_words
            valid_words.append(word)

    # Join the list of words together into a string
    s = ' '.join(valid_words)

    return s

def pipeline(s: str):
    s = lowercase(s)
    s = remove_punctuation(s)
    s = remove_stopwords(s)
    return s

# Title, Label = {'Real', 'Fake'}
df1 = pd.read_csv('./data/fake_news_data_set.csv')
# headine, is_sarcastic = {0, 1}
df2 = pd.read_json('./data/sarcasm_headlines_dataset_v2.json', lines=True)
# title, label = {0, 1}; 0 for real, 1 for fake
df3 = pd.read_csv('./data/WELFake_Dataset.csv')

# isolate key features
df1 = df1[['Title', 'Label']]
df2 = df2[['headline', 'is_sarcastic']]
df3 = df3[['title', 'label']]

# reformat dataframes by renaming columns, etc.
df1 = df1.rename(columns={'Title':'headline', 'Label':'is_fake'})
df1['is_fake'] = (df1['is_fake'] == 'Fake').astype(int)

df2 = df2.rename(columns={'is_sarcastic': 'is_fake'})

df3 = df3.rename(columns={'title':'headline', 'label':'is_fake'})

# merge data sets
merged = df1.merge(df2.merge(df3, how='outer'), how='outer')

# Dropping any duplicates or nulls, applying text cleaning pipeline
merged = merged.drop_duplicates().dropna().apply(pipeline).reset_index()

# Saving to csv
compression_opts = dict(method='zip',archive_name='sample.csv')
merged.to_csv('./data/sample.zip', index=False, compression=compression_opts)
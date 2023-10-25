import pandas as pd
import numpy as np

# Title, Label = {'Real', 'Fake'}
df1 = pd.read_csv('./data/fake_news_data_set.csv')
# headine, is_sarcastic = {0, 1}
df2 = pd.read_json('./data/sarcasm_headlines_dataset_v2.json', lines=True)
# title, label = {0, 1}; 0 for real, 1 for fake
df3 = pd.read_csv('./data/WELFake_Dataset.csv')

# isolate key features
df1 = df1[['Title', 'Label']].reset_index()
df2 = df2[['headline', 'is_sarcastic']].reset_index()
df3 = df3[['title', 'label']].reset_index()

# reformat dataframes by renaming columns, etc.
df1 = df1.rename(columns={'Title':'headline', 'Label':'is_fake'})
df1['is_fake'] = (df1['is_fake'] == 'Fake').astype(int)

df2 = df2.rename(columns={'is_sarcastic': 'is_fake'})

df3 = df3.rename(columns={'title':'headline', 'label':'is_fake'})

# merge data sets
merged = df1.merge(df2.merge(df3, how='outer'), how='outer')

# Dropping any duplicates and nulls
merged = merged.drop_duplicates().dropna().reset_index()

# Saving to csv
compression_opts = dict(method='zip',archive_name='sample.csv')
merged.to_csv('./data/sample.zip', index=False, compression=compression_opts)
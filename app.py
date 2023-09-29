import streamlit as st
import pandas as pd
import numpy as np

st.title('Baseball')

DATE_COLUMN = 'date/time'
DATA_URL = ('data/baseball.csv')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('On-base Percentage to Wins')
obp_wins = data[['obp', 'w']]
st.scatter_chart(obp_wins, x='obp', y='w')
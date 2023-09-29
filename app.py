import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('Baseball')

DATE_COLUMN = 'date/time'
DATA_URL = ('data/baseball.csv')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['year'] = pd.to_datetime(data['year'], format='%Y')
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('On-base Percentage to Wins')
st.scatter_chart(data, x='obp', y='w', color='league', use_container_width=True)
st.markdown(
    '''
    We found that analyzing the relationship between On-base Percentage (OBP)
    and the numbers of wins was important as, given most baseball matches
    either end in a win or a loss, we figured On-base Percentage, a measure of how often
    a player occupies bases while on offense, would have a strong positive correlation
    with wins.
    '''
)

st.subheader('Competitiveness Over Time in National and American Leagues')

fig = plt.figure()
american_league = data[data['league'] == 'AL']
national_league = data[data['league'] == 'NL']
compete_al = american_league.groupby('year')['w'].median()
compete_nl = national_league.groupby('year')['w'].median()
compete_al.plot(kind='line')
compete_nl.plot(kind='line')
plt.xlabel('Year')
plt.ylabel('Median Wins')
plt.legend(['American League', 'National League'])
st.pyplot(fig)

st.markdown(
    '''
    Here we define "competitiveness" as the median number of wins for all teams
    in a given year--the rationale being that a higher median number of wins indicates that
    more teams are performing at the same level given a fixed number of games per season. We
    find the metric important as it could to track trends in the quality of the leagues; thus,
    giving investors a sense of how much money to invest in order to keep their franchise
    successful.
    '''
)
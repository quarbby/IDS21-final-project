import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.express
import matplotlib.pyplot as plt
from plotly import graph_objs as go
from wordcloud import WordCloud, STOPWORDS
import re
import pydeck as pdk
import plotly.graph_objects as go



st.set_page_config(page_title="US Election and Insurrection", page_icon=None, layout='wide', initial_sidebar_state='expanded', menu_items=None)

st.title('The United States Election and Insurrection')

DATE_COLUMN = 'created_at'


@st.cache
def load_data():
    df_facebook_before_insurrection = pd.read_csv('./data/facebook_before_insurrection.csv')
    df_facebook_after_insurrection = pd.read_csv('./data/facebook_after_insurrection.csv')
    df_reddit_before_insurrection = pd.read_csv('./data/reddit_before_insurrection.csv')
    df_reddit_after_insurrection = pd.read_csv('./data/reddit_after_insurrection.csv')
    df_twitter_before_insurrection = pd.read_csv('./data/twitter_before_insurrection.csv')
    df_twitter_after_insurrection = pd.read_csv('./data/twitter_after_insurrection.csv')

    return df_facebook_before_insurrection, df_facebook_after_insurrection, df_reddit_before_insurrection, df_reddit_after_insurrection, df_twitter_before_insurrection, df_twitter_after_insurrection


#df_linechart_freq = {fb_ctdate[], fb_ctdate['id'], tw_ctdate['id'], rd_ctdate['id']}

#st.table(df_linechart_freq)

df_tw_geo_before_insurrection = pd.read_csv('./data/before_with_places_ext.csv')
df_tw_geo_after_insurrection = pd.read_csv('./data/after_with_places_ext.csv')


# Project description part
desc_1, desc_space, desc_2 = st.columns((2, 0.1, 1))
with desc_1:
    st.markdown('<h3>Project Description<h3><p>The 2020 United States presidential election was held on 3 November 2020. The Democratic nominee Joe Biden won the election. Before, during and after Election Day, Republicans attempted to overturn the results, by calling out widespread voter fraud. On January 6, 2021, a mob of supporters of then-President Trump attacked the United States Capitol, seeking to overturn the Congress session that would formalize the Democrat victory.<p>', unsafe_allow_html=True)
with desc_2:
    st.image('images/img.png')

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    election_btn = st.button('<h3>US Elections 2020<h3><br><p>#corruptelection #electionfraud, #electionintegrity #fakeelection #fakevotes #voterfraud<p>')
with btn_col2:
    insurrection_btn = st.button('<h3>US Insurrection 2021<h3><br><p>#magacivilwar #marchfortrump #millionmagamarch #saveamerica #stopthesteal #stopthefraud<p>')

# Statistics of each social media platform
stat_col1, stat_col2, stat_col3 = st.columns(3)

df_facebook_before_insurrection, df_facebook_after_insurrection, df_reddit_before_insurrection, df_reddit_after_insurrection, df_twitter_before_insurrection, df_twitter_after_insurrection = load_data()

df_facebook_before = df_facebook_before_insurrection
df_facebook_after = df_facebook_after_insurrection
df_reddit_before = df_reddit_before_insurrection
df_reddit_after = df_reddit_after_insurrection
df_twitter_after = df_twitter_after_insurrection
df_twitter_before = df_twitter_before_insurrection

# METRICS
facebook_total = len(df_facebook_before) + len(df_facebook_after)
reddit_total = len(df_reddit_before) + len(df_reddit_after)
twitter_total = len(df_twitter_before) + len(df_twitter_after)
stat_col1.metric(label = "Facebook", value=f"{facebook_total:,}")
stat_col2.metric(label = "Reddit", value=f"{reddit_total:,}")
stat_col3.metric(label = "Twitter", value=f"{twitter_total:,}")

stat_breakdown_col1, stat_breakdown_col2, stat_breakdown_col3, stat_breakdown_col4, stat_breakdown_col5, stat_breakdown_col6 = st.columns(6)
stat_breakdown_col1.metric(label="BEFORE", value=f"{len(df_facebook_before):,}")
stat_breakdown_col2.metric(label="AFTER", value=f"{len(df_facebook_after):,}")

stat_breakdown_col3.metric(label="BEFORE", value=f"{len(df_reddit_before):,}")
stat_breakdown_col4.metric(label="AFTER", value=f"{len(df_reddit_after):,}")

stat_breakdown_col5.metric(label="BEFORE", value=f"{len(df_twitter_before):,}")
stat_breakdown_col6.metric(label="AFTER", value=f"{len(df_twitter_after):,}")

# LINECHART
df_fb_count = pd.concat([df_facebook_before_insurrection[['id','created_at']],df_facebook_after_insurrection[['id','created_at']]])
df_rd_count = pd.concat([df_reddit_before_insurrection[['id','created_at']],df_reddit_after_insurrection[['id','created_at']]])
df_tw_count = pd.concat([df_twitter_before_insurrection[['id','created_at']],df_twitter_after_insurrection[['id','created_at']]])

df_fb_count[DATE_COLUMN] = df_fb_count[DATE_COLUMN].apply(lambda x: x.replace('+00:00', ''))
df_fb_count[DATE_COLUMN] = pd.to_datetime(df_fb_count[DATE_COLUMN])

df_rd_count[DATE_COLUMN] = df_rd_count[DATE_COLUMN].apply(lambda x: x.replace('+00:00', ''))
df_rd_count[DATE_COLUMN] = pd.to_datetime(df_rd_count[DATE_COLUMN])

df_tw_count[DATE_COLUMN] = df_tw_count[DATE_COLUMN].apply(lambda x: x.replace('+00:00', ''))
df_tw_count[DATE_COLUMN] = pd.to_datetime(df_tw_count[DATE_COLUMN])

fb_ctdate = df_fb_count.groupby([df_fb_count[DATE_COLUMN].dt.date]).count().drop(columns=DATE_COLUMN).reset_index()
tw_ctdate = df_tw_count.groupby([df_tw_count[DATE_COLUMN].dt.date]).count().drop(columns=DATE_COLUMN).reset_index()
rd_ctdate = df_rd_count.groupby([df_rd_count[DATE_COLUMN].dt.date]).count().drop(columns=DATE_COLUMN).reset_index()

data_linechart = {'date':fb_ctdate['created_at'],'Facebook':fb_ctdate['id'],'Twitter':tw_ctdate['id'],'Reddit':rd_ctdate['id']}
df_linechart = pd.DataFrame(data=data_linechart)
df_linechart.set_index(['date'], inplace=True)

st.line_chart(df_linechart)

# LINECHART DESCRIPTOR

st.markdown('Talk about numbers, then which source generated the most content bla bla bla, Facebook peaks where, and desc of trend Twitter peaks where and desc of trend Reddit peaks where')

# SLIDER

min_date = min(df_linechart.index)
max_date = max(df_linechart.index)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{padding:0 20px;}</style>', unsafe_allow_html=True)

st.write('<style>div[role=radiogroup]{background-color:#eaeaea;border-radius:10px;padding:10px}</style>', unsafe_allow_html=True)


choose=st.radio("Social media filter",("Facebook","Reddit","Twitter"))

date_format = 'YYYY-MM-DD'


geo_after_df = pd.read_csv('./data/after_with_places_ext.csv')
geo_before_df = pd.read_csv('./data/before_with_places_ext.csv')

st.markdown("""---""")

time_container = st.container()
time_container.markdown('## Discourse over time')
time_container.markdown('Describe what you can do in this time-based ')

date_filter = time_container.slider('Select date range', min_value=min_date, max_value=max_date, value=(min_date, max_date), format=date_format)

geo_all=(pd.concat([geo_before_df,geo_after_df]))
geo_all = geo_all[geo_all['country_code']='US']]



us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

inverted_us_state = dict(map(reversed, us_state_to_abbrev.items()))

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

for col in df.columns:
    df[col] = df[col].astype(str)

df['text'] = df['state'] + '<br>' + \
    'Beef ' + df['beef'] + ' Dairy ' + df['dairy'] + '<br>' + \
    'Fruits ' + df['total fruits'] + ' Veggies ' + df['total veggies'] + '<br>' + \
    'Wheat ' + df['wheat'] + ' Corn ' + df['corn']


df_twitter_after_insurrection = pd.read_csv('./data/twitter_after_insurrection.csv')


fig = go.Figure(data=go.Choropleth(
    locations=df['code'],
    z=df['total exports'].astype(float),
    locationmode='USA-states',
    colorscale='Reds',
    autocolorscale=False,
    text=df['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Millions USD"
))

fig.update_layout(
    title_text='Discourse in US States',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)

time_container.plotly_chart(fig)

st.markdown("""---""")

emotion_container = st.container()
emotion_container.markdown('## Emotions involved in discourse')

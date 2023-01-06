# Libraries
import streamlit as st
from shroomdk import ShroomDK
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
from pandas.core.reshape.reshape import unstack

# Global Variables
theme_plotly = None  # None or streamlit

# Layout
st.set_page_config(page_title='Activiy', page_icon=':bar_chart:', layout='wide')
st.title('🔥 Activity')

st.write("")
st.write("")
st.subheader('Network Performance Overall View')

@st.cache(ttl=10000)
def querying_pagination(query_string):
    sdk = ShroomDK('653fb086-1a65-45b0-aa0c-28333f2d4f31')
    result_list = []
    for i in range(1, 11):
        data = sdk.query(query_string, page_size=100000, page_number=i)
        if data.run_stats.record_count == 0:
            break
        else:
            result_list.append(data.records)

    result_df = pd.DataFrame()
    for idx, each_list in enumerate(result_list):
        if idx == 0:
            result_df = pd.json_normalize(each_list)
        else:
            result_df = pd.concat([result_df, pd.json_normalize(each_list)])

    return result_df


# daily Transactions Metrics
df_query = """ 
with priceTb as (
SELECT
RECORDED_HOUR::date as p_date,
avg(CLOSE) as SOLPrice
FROM solana.core.fact_token_prices_hourly
WHERE SYMBOL = 'SOL'
AND p_date >= '2022-12-01'
GROUP by 1
)
SELECT
BLOCK_TIMESTAMP::date as date,
case 
when date < '2022-12-26' then 'Before Degods/y00ts News' 
else 'After Degods/y00ts News' end as period,
COUNT(DISTINCT Tx_id) as Tx_Count,
COUNT(DISTINCT SIGNERS[0]) as Usr_Count,
sum(FEE * SOLPrice) as Tx_Fee_Volume,
avg(FEE * SOLPrice) as Avg_Tx_Fee_Volume
FROM solana.core.fact_transactions t join priceTb p on t.BLOCK_TIMESTAMP::date = p.p_date
WHERE date >= '2022-12-01'
AND date <= CURRENT_DATE - 1 
GROUP by 1,2
"""

df = querying_pagination(df_query)
fig = px.bar(df, x='date', y='tx_count', color='period')
fig.update_layout(title_text='Daily # of Txs')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='usr_count', color='period')
fig.update_layout(title_text='Daily # of Active Users')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='tx_fee_volume', color='period')
fig.update_layout(title_text='Daily Amount of Fee Volume($)')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='avg_tx_fee_volume', color='period')
fig.update_layout(title_text='Daily Amount of "Average" Fee Volume($)')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.write("")
st.write("")
st.subheader('New Users Overview')

@st.cache(ttl=10000)
def querying_pagination(query_string):
    sdk = ShroomDK('653fb086-1a65-45b0-aa0c-28333f2d4f31')
    result_list = []
    for i in range(1, 11):
        data = sdk.query(query_string, page_size=100000, page_number=i)
        if data.run_stats.record_count == 0:
            break
        else:
            result_list.append(data.records)

    result_df = pd.DataFrame()
    for idx, each_list in enumerate(result_list):
        if idx == 0:
            result_df = pd.json_normalize(each_list)
        else:
            result_df = pd.concat([result_df, pd.json_normalize(each_list)])

    return result_df


# daily new wallet
df_query = """ 
with main as(
  select 
	min(BLOCK_TIMESTAMP) as min_date, 
	SIGNERS[0] as address
  FROM solana.core.fact_transactions 
  group by 2 
) 
select 
	min_date::date as date,
  	case 
  		when min_date < '2022-12-26' then 'Before Degods/y00ts News' 
  		else 'After Degods/y00ts News' end as period,
	count(DISTINCT address) as new_users
from main 
WHERE min_date::date >= '2022-12-01'
AND min_date::date <= CURRENT_DATE - 1
group by 1, 2
order by 1
"""

df = querying_pagination(df_query)
fig = px.bar(df, x='date', y='new_users', color='period')
fig.update_layout(title_text='Daily # of New Users')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


st.write("")
st.write("")
st.write("""
#### Activity Across Time
A follow-up analysis will be to see whether there are true variations in the volume of transfers made onchain by hours."""
)

@st.cache(ttl=10000)
def gat_data(query):
    if query == 'Activity Across Time':
        return pd.read_json(
            'https://node-api.flipsidecrypto.com/api/v2/queries/3b44a95c-2761-4c16-b808-5ffb69152a9b/data/latest'
        )

activity_across_time = gat_data('Activity Across Time')
df = activity_across_time
fig = px.bar(df, x='HOUR_TIME', y='TX_PERFORMED', color='PERIOD')
fig.update_layout(title_text='Transaction Volumes (Total Txs) Across Hours of the day')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='HOUR_TIME', y='AVG_TX_PER_HOUR', color='PERIOD')
fig.update_layout(title_text='Transaction Volumes (Avg Txs) Across Hours of the day')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='HOUR_TIME', y='USERS', color='PERIOD')
fig.update_layout(title_text='Unique Users Performing Transactions Across Hours of the Day')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


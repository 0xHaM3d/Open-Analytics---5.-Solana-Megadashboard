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
st.set_page_config(page_title='Development', page_icon=':bar_chart:', layout='wide')
st.title('🎨 Ecosystem Development')

st.write("")
st.write("")
st.subheader('New Deployed Program After Degods/y00ts News')


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


# daily NFT Interctions Metrics
df_query = """ 
with tb1 as (
  SELECT
  	instructions[0]:programId as program,
  	min(block_timestamp) as deploying_date
FROM solana.core.fact_transactions
  group by 1
  )
select 
  deploying_date::date as date,
  count(distinct program) as program_cnt,
  sum(program_cnt) over (order by date) as cum_program_cnt
from tb1
WHERE date >= '2022-12-26'
and date <= CURRENT_DATE - 1
GROUP by 1
order by 1
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y='program_cnt')
    fig.update_layout(title_text='Daily # of New Deployed Program')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.area(df, x='date', y='cum_program_cnt')
    fig.update_layout(title_text='Cumulative # New Deployed Program')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.write("")
st.write("")
st.subheader('Daily Interaction Count by Solana Programs, After Degods/y00ts News')


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


# daily NFT Interctions Metrics
df_query = """ 
select 
  block_timestamp::date as date,
  count(distinct t.signers[0]) as address,
  l.label, 
  count(l.label)  as interact
  from solana.core.fact_transactions t join solana.core.dim_labels l on t.instructions[0]:programId = l.address
  and t.block_timestamp:: date >= '2022-12-26' 
  and t.block_timestamp::date <= current_date - 1
  and l.label_subtype != 'token_contract'
  and l.label != 'solana'
  and t.succeeded = TRUE
  group by date, l.label
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y='address', color='label')
    fig.update_layout(title_text='Daily Interactor Count by Solana Programs')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.bar(df, x='date', y='interact', color='label')
    fig.update_layout(title_text='Daily Interaction Count by Solana Programs')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)



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


# daily NFT Interctions Metrics
df_query = """ 
with top_10 as (
  select
  count(l.label)  as interact_count,
  count(distinct t.signers[0]) as unique_address,
  l.label as program
  from solana.core.fact_transactions t join solana.core.dim_labels l on t.instructions[0]:programId = l.address
  and t.block_timestamp:: date >= '2022-12-26' 
  and t.block_timestamp::date <= current_date - 1
  and l.label_subtype != 'token_contract'
  and l.label != 'solana'
  and t.succeeded = TRUE
  group by program 
  order by unique_address desc 
  limit 10
)

select * from top_10
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['program'], y=df['unique_address'], name='Interactions'), secondary_y=False)
    fig.update_layout(title_text='Top 10 Programs Interactors Count')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='unique_address', names='program', title='Share Interactors of Top 10 Programs')
    fig.update_layout(legend_title='Program Label', legend_y=1)
    fig.update_traces(textinfo='percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['program'], y=df['interact_count'], name='Interactors'), secondary_y=False)
    fig.update_layout(title_text='Top 10 Programs Interactions Count')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='interact_count', names='program', title='Share Interactions of Top 10 Programs')
    fig.update_layout(legend_title='Program Label', legend_y=1)
    fig.update_traces(textinfo='percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.write("")
st.write("")
st.subheader('Programs Field After Degods/y00ts News')

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


# Programs Field
df_query = """ 
select 
  count(distinct signers[0]) as address
  ,LABEL_TYPE as Type
  ,count(l.label)  as interact
  from solana.core.fact_transactions t join solana.core.dim_labels l on t.instructions[0]:programId = l.address
  and t.block_timestamp:: date >= '2022-12-26' 
  and t.block_timestamp::date <= CURRENT_DATE - 1
  and l.label_subtype != 'token_contract'
  and l.label != 'solana'
  and t.succeeded = TRUE
group by type 
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['type'], y=df['address'], name='Interactions'), secondary_y=False)
    fig.update_layout(title_text='Programs Field Interactors Count')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='address', names='type', title='Share Interactors of Programs Field')
    fig.update_layout(legend_title='Programs Field', legend_y=1)
    fig.update_traces(textinfo='percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['type'], y=df['interact'], name='Interactors'), secondary_y=False)
    fig.update_layout(title_text='Programs Field Interactions Count')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='interact', names='type', title='Share Interactions of Programs Field')
    fig.update_layout(legend_title='Programs Field', legend_y=1)
    fig.update_traces(textinfo='percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
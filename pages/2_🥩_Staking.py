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
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Layout
st.set_page_config(page_title='Staking', page_icon=':bar_chart:', layout='wide')
st.title('🥩 Staking')

st.write(
    """
    Tokens (mSOL, stSOL, etc.) representing a user's stake are issued when they make a deposit with a liquid staking 
    provider. These days, there are typically only two speeds to choose from when it comes to internet service providers: 
    fast and slow. The staked tokens can be instantly unstaked and sent to the user with the fast option for a fee, 
    while the staked tokens will go through the standard unstaking process until the end of the epoch with the slow option.

    To keep things simple, we'll refer to both fast and slow unstakes collectively as WITHDRAWs from now on, as doing so 
    will cause the representative tokens to be burned and the stake to be removed from the pool of current unstakes.
    """
)
st.write("")
st.write("")
st.write("")
st.write("")

st.subheader('Staking Metrics Over Time')

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



df_query = """ 
select 
	BLOCK_TIMESTAMP::date as date,
	CASE
	when action like '%withdraw%' then 'Unstake'
  	when action like '%deposit%' then 'Stake'
  	when action = 'order_unstake' then 'Unstake Order'
  	when action = 'claim' then 'claim'
  	end as action_Status,
  	sum(amount/pow(10,9)) AS volume,
  	count(distinct ADDRESS) as user_cnt,
  	count(distinct TX_ID) as tx_cnt,
  	avg(amount/pow(10,9)) as avg_volume
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-01'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	--and amount is not null
group by 1,2
"""

df = querying_pagination(df_query)
fig = px.bar(df, x='date', y='tx_cnt', color='action_status')
fig.update_layout(title_text='Daily Tx Count per Action')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='user_cnt', color='action_status')
fig.update_layout(title_text='Daily # of Users per Action')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='volume', color='action_status')
fig.update_layout(title_text='Daily Volume(SOL) per Action')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='avg_volume', color='action_status')
fig.update_layout(title_text='Daily avg_volume(SOL) per Action')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.write("")
st.write("")
st.write("")

st.subheader('Daily Unstaking Volume Distribution')

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



df_query = """ 
select 
	BLOCK_TIMESTAMP::date as date,
  	case 
  	when amount/pow(10,9) < 50 then '1: < 50 Sol'
  	when amount/pow(10,9) between 50 and 500 then '2: 51 ~ 500 Sol'
  	when amount/pow(10,9) between 500 and 1000 then '3: 500 ~ 1K Sol'
  	when amount/pow(10,9) between 1000 and 5000 then '4: 1 ~ 5K Sol'
  	when amount/pow(10,9) between 5000 and 10000 then '5: 5 ~ 10K Sol'
  	when amount/pow(10,9) > 10000 then '6: > 10K Sol'
  end as status,
  count(distinct TX_ID)*-1 as tx_cnt
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-01'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	and amount is not null
	and action like any ('%withdraw%', 'claim')
group by 1,2
"""

df = querying_pagination(df_query)
fig = px.bar(df, x='date', y='tx_cnt', color='status')
fig.update_layout(title_text='Daily Tx Count per Action')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)



st.write("")
st.write("")
st.write("")

st.subheader('Daily Staking Volume Distribution')

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


df_query = """ 
select 
	BLOCK_TIMESTAMP::date as date,
  	case 
  	when amount/pow(10,9) < 50 then '1: < 50 Sol'
  	when amount/pow(10,9) between 50 and 500 then '2: 51 ~ 500 Sol'
  	when amount/pow(10,9) between 500 and 1000 then '3: 500 ~ 1K Sol'
  	when amount/pow(10,9) between 1000 and 5000 then '4: 1 ~ 5K Sol'
  	when amount/pow(10,9) between 5000 and 10000 then '5: 5 ~ 10K Sol'
  	when amount/pow(10,9) > 10000 then '6: > 10K Sol'
  end as status,
  count(distinct TX_ID) as tx_cnt
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-01'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	and amount is not null
	and not action like any ('%withdraw%', 'claim')
group by 1,2
"""

df = querying_pagination(df_query)
fig = px.bar(df, x='date', y='tx_cnt', color='status')
fig.update_layout(title_text='Daily Tx Count per Action')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


st.write("")
st.write("")
st.write("")

st.subheader('Staking Pools')

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



df_query = """ 
with Unstake as (
select 
  	BLOCK_TIMESTAMP::date as date,
	STAKE_POOL_NAME as pool_name,
  	sum(amount/pow(10,9))*-1 AS unstake_vol,
  	avg(amount/pow(10,9))*-1 AS avg_unstake_vol,
  	count(distinct ADDRESS)*-1 as unstaker_cnt,
  	count(distinct TX_ID)*-1 as unstake_tx_cnt
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-01'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	and action like any ('%withdraw%', 'claim')
  	--and amount is not null
group by 1,2
),
Stake as (
select 
  	BLOCK_TIMESTAMP::date as date,
	STAKE_POOL_NAME as pool_name,
  	sum(amount/pow(10,9)) AS stake_vol,
  	avg(amount/pow(10,9)) AS avg_stake_vol,
  	count(distinct ADDRESS) as staker_cnt,
  	count(distinct TX_ID) as stake_tx_cnt
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-01'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	and action like '%deposit%'
  	--and amount is not null
group by 1,2
)
  select * 
  from Unstake a join Stake b using (date, pool_name)
order by 1,2 
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y='unstake_vol', color='pool_name')
    fig.update_layout(title_text='Daily Unstaking Volume by Pools Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with c2:
    fig = px.bar(df, x='date', y='avg_unstake_vol', color='pool_name')
    fig.update_layout(title_text='Average Unstaking Volume by Pools Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y='stake_vol', color='pool_name')
    fig.update_layout(title_text='Daily Staking Volume on Solana Stake Pools Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with c2:
    fig = px.bar(df, x='date', y='avg_stake_vol', color='pool_name')
    fig.update_layout(title_text='Average Staking Volume by Pools Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y='unstake_tx_cnt', color='pool_name')
    fig.update_layout(title_text='Daily Unstaking Tx Count by Pools Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with c2:
    fig = px.bar(df, x='date', y='unstaker_cnt', color='pool_name')
    fig.update_layout(title_text='Daily Unstaker Count by Pools Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y='stake_tx_cnt', color='pool_name')
    fig.update_layout(title_text='Daily Staking Tx Count by Pools Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with c2:
    fig = px.bar(df, x='date', y='staker_cnt', color='pool_name')
    fig.update_layout(title_text='Daily Staker Count by Pools Over Time')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.write("")
st.write("")
st.write("")

st.subheader('Total Staking by Pools After Degods/y00ts Announcement')

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



df_query = """ 
with Unstake as (
select
	STAKE_POOL_NAME as pool_name,
  	sum(amount/pow(10,9)) AS unstake_vol,
  	avg(amount/pow(10,9)) AS avg_unstake_vol,
  	count(distinct ADDRESS) as unstaker_cnt,
  	count(distinct TX_ID) as unstake_tx_cnt
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-26'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	and action like any ('%withdraw%', 'claim')
  	--and amount is not null
group by 1
),
Stake as (
select 
	STAKE_POOL_NAME as pool_name,
  	sum(amount/pow(10,9)) AS stake_vol,
  	avg(amount/pow(10,9)) AS avg_stake_vol,
  	count(distinct ADDRESS) as staker_cnt,
  	count(distinct TX_ID) as stake_tx_cnt
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-26'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	and action like '%deposit%'
  	--and amount is not null
group by 1
)
select 
    *,
    stake_vol - unstake_vol as net_stake_vol
from Unstake a join Stake b using(pool_name)
order by 1,2 
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = px.pie(df, values='unstake_vol', names='pool_name', title='Total Value & Share of UnStaked Volum by Pool')
    fig.update_layout(legend_title='UnStaking Vol', legend_y=1)
    fig.update_traces(textinfo='value+percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with c2:
    fig = px.pie(df, values='stake_vol', names='pool_name', title='Total Value & Share of Staked Volum by Pool')
    fig.update_layout(legend_title='Staking Vol', legend_y=1)
    fig.update_traces(textinfo='value+percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = px.pie(df, values='unstake_tx_cnt', names='pool_name', title='Total Value & Share of UnStake Txs by Pool')
    fig.update_layout(legend_title='UnStaking Txs', legend_y=1)
    fig.update_traces(textinfo='value+percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with c2:
    fig = px.pie(df, values='stake_tx_cnt', names='pool_name', title='Total Value & Share of Stake Txs by Pool')
    fig.update_layout(legend_title='Staking Txs', legend_y=1)
    fig.update_traces(textinfo='value+percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = px.pie(df, values='unstaker_cnt', names='pool_name', title='Total Value & Share of UnStaker Cnt by Pool')
    fig.update_layout(legend_title='UnStaker Cnt', legend_y=1)
    fig.update_traces(textinfo='value+percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with c2:
    fig = px.pie(df, values='staker_cnt', names='pool_name', title='Total Value & Share of Staker Cnt by Pool')
    fig.update_layout(legend_title='Staker Cnt', legend_y=1)
    fig.update_traces(textinfo='value+percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='pool_name', y='net_stake_vol', color='pool_name')
fig.update_layout(title_text='Net Staked Volume by Pools Over Time')
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


df_query = """ 
with tb1 as (
select
	STAKE_POOL_NAME as pool_name,
	ADDRESS,
  	(amount/pow(10,9))*-1 AS volume
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-26'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	and action like any ('%withdraw%', 'claim')

UNION
  
select 
	STAKE_POOL_NAME as pool_name,
  	ADDRESS,
  	(amount/pow(10,9)) AS volume
from solana.core.fact_stake_pool_actions 
  where 1=1
	and SUCCEEDED = 'TRUE'
	and ACTION is not NULL
	and BLOCK_TIMESTAMP	>= '2022-12-26'
	and BLOCK_TIMESTAMP	<= current_date - 1
  	and action like '%deposit%'
)
, net_vol as (
    select
        pool_name,
        ADDRESS,
        sum(volume) as net_stake_vol
    from tb1
  GROUP by 1,2
)
  select 
        pool_name,
        case 
  		    when net_stake_vol < 50 then '1: < 50 Sol'
  		    when net_stake_vol between 50 and 500 then '2: 51 ~ 500 Sol'
  		    when net_stake_vol between 500 and 1000 then '3: 500 ~ 1K Sol'
  		    when net_stake_vol between 1000 and 5000 then '4: 1 ~ 5K Sol'
  		    when net_stake_vol between 5000 and 10000 then '5: 5 ~ 10K Sol'
  		    when net_stake_vol > 10000 then '6: > 10K Sol'
        end as status,
        count(distinct ADDRESS) as staker_cnt
  from net_vol
GROUP by 1,2 
"""
df = querying_pagination(df_query)
fig = px.bar(df, x='pool_name', y='staker_cnt', color='status')
fig.update_layout(title_text='Distribution of Users Count by Net Staking Volume per Pools')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

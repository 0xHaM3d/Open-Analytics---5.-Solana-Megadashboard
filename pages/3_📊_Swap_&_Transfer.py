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
st.set_page_config(page_title='Swap & Transfere', page_icon=':bar_chart:', layout='wide')
st.title('📊 Swap & Transfere')

st.write("")
st.write("")
st.subheader('Swapping Overall View Afetr Degods/y00ts News')

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


# daily Swaps Transactions Metrics
df_query = """ 
with priceTb as (
select 
    RECORDED_HOUR::date as p_date,
	SYMBOL,
  	TOKEN_ADDRESS,
	avg(CLOSE) as USDPrice
from solana.core.ez_token_prices_hourly
where RECORDED_HOUR::date >= '2022-12-26'
and RECORDED_HOUR::date <= CURRENT_DATE - 1
and IS_IMPUTED = 'FALSE'
group by 1,2,3
  )
-- D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK usdt
-- EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v usdc
select  
	block_timestamp::date as date,
  
  	-- ******** Swap From ******* -------
  
  	count(DISTINCT (CASE WHEN SWAP_FROM_MINT in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then TX_ID end)) as swap_tx_from_stablecoins,
	count(DISTINCT (CASE WHEN SWAP_FROM_MINT not in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then TX_ID end)) as swap_tx_from_non_stablecoins,
  	count(DISTINCT (CASE WHEN SWAP_FROM_MINT in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAPPER end)) as swapper_from_stablecoins,
	count(DISTINCT (CASE WHEN SWAP_FROM_MINT not in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAPPER end)) as swapper_from_non_stablecoins,
  	sum(CASE WHEN SWAP_FROM_MINT in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAP_FROM_AMOUNT end) as swap_from_stablecoins,
	sum(CASE WHEN SWAP_FROM_MINT not in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAP_FROM_AMOUNT*t2.USDPrice end) as swap_from_non_stablecoins,
  	avg(CASE WHEN SWAP_FROM_MINT in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAP_FROM_AMOUNT end) as avg_from_stablecoins,
	avg(CASE WHEN SWAP_FROM_MINT not in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAP_FROM_AMOUNT*t2.USDPrice end) as avg_from_non_stablecoins,

  	-- ******** Swap To ******* -------
  	count(DISTINCT (CASE WHEN SWAP_TO_MINT in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then TX_ID end)) as swap_tx_to_stablecoins,
	count(DISTINCT (CASE WHEN SWAP_TO_MINT not in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then TX_ID end)) as swap_tx_to_non_stablecoins,
  	count(DISTINCT (CASE WHEN SWAP_TO_MINT in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAPPER end)) as swapper_to_stablecoins,
	count(DISTINCT (CASE WHEN SWAP_TO_MINT not in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAPPER end)) as swapper_to_non_stablecoins,
	sum(CASE WHEN SWAP_TO_MINT in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAP_TO_AMOUNT end) as swap_to_stablecoins,
	sum(CASE WHEN SWAP_TO_MINT not in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v')
             then SWAP_TO_AMOUNT*t3.USDPrice end) as swap_to_non_stablecoins,
	avg(CASE WHEN SWAP_TO_MINT in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAP_TO_AMOUNT end) as avg_to_stablecoins,
	avg(CASE WHEN SWAP_TO_MINT not in ('D3KdBta3p53RV5FoahnJM5tP45h6Fd3AyFYgXTJvGCaK', 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v') 
             then SWAP_TO_AMOUNT*t3.USDPrice end) as avg_to_non_stablecoins,
  	t2.SYMBOL || ' => ' || t3.SYMBOL as swap_pair
from solana.core.fact_swaps t1 join priceTb t2 on t1.block_timestamp::date = t2.p_date and t1.SWAP_FROM_MINT = t2.TOKEN_ADDRESS
  join priceTb t3 on t1.block_timestamp::date = t3.p_date and t1.SWAP_TO_MINT = t3.TOKEN_ADDRESS
where block_timestamp::date >= '2022-12-26'
AND block_timestamp::date <= CURRENT_DATE - 1
group by date , swap_pair
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['date'], y=df['swap_tx_from_stablecoins']), secondary_y=False)
    fig.add_trace(go.Bar(x=df['date'], y=df['swap_tx_from_non_stablecoins']), secondary_y=False)
    fig.update_layout(title_text='Daily Swap Tx FROM Stablecoins/NonStablecoins')
    fig.update_yaxes(title_text='Txs FROM St', secondary_y=False)
    fig.update_yaxes(title_text='Txs FROM Non-St', secondary_y=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['date'], y=df['swap_tx_to_stablecoins']), secondary_y=False)
    fig.add_trace(go.Bar(x=df['date'], y=df['swap_tx_to_non_stablecoins']), secondary_y=False)
    fig.update_layout(title_text='Daily Swap Tx TO Stablecoins/NonStablecoins')
    fig.update_yaxes(title_text='Txs TO St', secondary_y=False)
    fig.update_yaxes(title_text='Txs TO Non-St', secondary_y=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['date'], y=df['swapper_from_stablecoins']), secondary_y=False)
    fig.add_trace(go.Bar(x=df['date'], y=df['swapper_from_non_stablecoins']), secondary_y=False)
    fig.update_layout(title_text='Daily Swappers FROM Stablecoins/NonStablecoins')
    fig.update_yaxes(title_text='Swappers FROM St', secondary_y=False)
    fig.update_yaxes(title_text='Swappers FROM Non-St', secondary_y=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['date'], y=df['swapper_to_stablecoins']), secondary_y=False)
    fig.add_trace(go.Bar(x=df['date'], y=df['swapper_to_non_stablecoins']), secondary_y=False)
    fig.update_layout(title_text='Daily Swappers TO Stablecoins/NonStablecoins')
    fig.update_yaxes(title_text='Swappers TO St', secondary_y=False)
    fig.update_yaxes(title_text='Swappers TO Non-St', secondary_y=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['date'], y=df['swap_from_stablecoins']), secondary_y=False)
    fig.add_trace(go.Bar(x=df['date'], y=df['swap_from_non_stablecoins']), secondary_y=False)
    fig.update_layout(title_text='Daily Swap Volume($) FROM Stablecoins/NonStablecoins')
    fig.update_yaxes(title_text='Swap FROM St', secondary_y=False, showgrid=True)
    fig.update_yaxes(title_text='Swap FROM Non-St', secondary_y=False, showgrid=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['date'], y=df['swap_to_stablecoins']), secondary_y=False)
    fig.add_trace(go.Bar(x=df['date'], y=df['swap_to_non_stablecoins']), secondary_y=False)
    fig.update_layout(title_text='Daily Swap Volume($) TO Stablecoins/NonStablecoins')
    fig.update_yaxes(title_text='Swap TO St', secondary_y=False, showgrid=True)
    fig.update_yaxes(title_text='Swap TO Non-St', secondary_y=False, showgrid=True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y=['avg_from_stablecoins', 'avg_from_non_stablecoins'])
    fig.update_layout(title_text='Average Swapped Volume($) FROM Stablecoins/NonStablecoins')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.bar(df, x='date', y=['avg_to_stablecoins', 'avg_to_non_stablecoins'])
    fig.update_layout(title_text='Average Swapped Volume($) TO Stablecoins/NonStablecoins')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


st.write("")
st.write("")
st.write("")
st.write("")
st.subheader('Top 10 Swaps Pair by the Most Swap Volume($) Afetr Degods/y00ts News')


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


# daily Swaps Transactions Metrics
df_query = """ 
with priceTb as (
select 
    RECORDED_HOUR::date as p_date,
	SYMBOL,
  	TOKEN_ADDRESS,
	avg(CLOSE) as USDPrice
from solana.core.ez_token_prices_hourly
where RECORDED_HOUR::date >= '2022-12-26'
and RECORDED_HOUR::date <= CURRENT_DATE - 1
and IS_IMPUTED = 'FALSE'
group by 1,2,3
  )
select  
	t2.SYMBOL || ' => ' || t3.SYMBOL as swap_pair,
	sum(SWAP_FROM_AMOUNT*t2.USDPrice) as swap_volume	
from solana.core.fact_swaps t1 join priceTb t2 on t1.block_timestamp::date = t2.p_date and t1.SWAP_FROM_MINT = t2.TOKEN_ADDRESS
  join priceTb t3 on t1.block_timestamp::date = t3.p_date and t1.SWAP_TO_MINT = t3.TOKEN_ADDRESS
where block_timestamp::date >= '2022-12-26'
AND block_timestamp::date <= CURRENT_DATE - 1
group by 1
order by 2 DESC
limit 10
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='swap_pair', y='swap_volume', color='swap_pair')
    fig.update_layout(title_text='Total Volume of Top 10 Swapped Pairs')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='swap_volume', names='swap_pair', title='Share Volume of Top 10 Swapped Pairs')
    fig.update_layout(legend_title='Staker Cnt', legend_y=1)
    fig.update_traces(textinfo='percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.write("")
st.write("")
st.subheader('Inflow/Outflow to CEXs')

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


# daily Transfere to CEXs Transactions Metrics
df_query = """ 
with cextable as (
  select * 
  from solana.core.dim_labels 
  where label_type = 'cex'
  ),

pricetable as (
select block_timestamp::date as day,
swap_from_mint,
avg (swap_to_amount/swap_from_amount) as USDPrice
from solana.fact_swaps
where swap_to_mint in ('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v','Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB') --USDC,USDT 
and swap_to_amount > 0
and swap_from_amount > 0
and block_timestamp::date >= '2022-12-26'
AND block_timestamp::date <= CURRENT_DATE - 1
and succeeded = 'TRUE'
group by 1,2
  )

select 
'Inflow To CEXs' as type,
block_timestamp::date as date,
count (distinct tx_id) as TX_Count,
count (distinct tx_from) as Users_Count,
sum (amount*usdprice) as Volume
from solana.core.fact_transfers t1 join pricetable t2 on t1.block_timestamp::date = t2.day and t1.mint = t2.swap_from_mint
where tx_to in (select address from cextable)
and block_timestamp::date >= '2022-12-26'
AND block_timestamp::date <= CURRENT_DATE - 1
group by 1,2

union ALL

select 
'Outflow From CEXs' as type,
block_timestamp::date as date,
count (distinct tx_id)*-1 as TX_Count,
count (distinct tx_to)*-1 as Users_Count,
sum (amount*usdprice)*-1 as Volume
from solana.core.fact_transfers t1 join pricetable t2 on t1.block_timestamp::date = t2.day and t1.mint = t2.swap_from_mint
where tx_from in (select address from cextable)
and block_timestamp::date >= '2022-12-26'
AND block_timestamp::date <= CURRENT_DATE - 1
group by 1,2
order by date
"""

df = querying_pagination(df_query)
fig = px.bar(df, x='date', y='tx_count', color='type')
fig.update_layout(title_text='Daily # of Transferred Txs TO/FROM CEXs')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='users_count', color='type')
fig.update_layout(title_text='Daily # of Transferrer TO/FROM CEXs')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='volume', color='type')
fig.update_layout(title_text='Daily Amount of Transferred Volume($) TO/FROM CEXs')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


st.write("")
st.write("")
st.subheader('Inflow/Outflow Vai Bridging')

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


# daily Bridging Transactions Metrics
df_query = """ 
with Outflow as (
  select 
  	BLOCK_TIMESTAMP::date as date,
  	c.address_name as tokens,
  	a.tx_id,
  	-1 * (b.value:parsed:info:amount/pow(10,8)) as Volume
from solana.core.fact_events a, lateral flatten(input => inner_instruction:instructions) b
join solana.core.dim_labels c on b.value:parsed:info:mint = c.address
where program_id = 'wormDTUJ6AWPNvk59vGQbDvGJmqbDTdgWgAqcLBCgUb'
	and block_timestamp >= '2022-12-26'
  	and block_timestamp <= current_date - 1
  	and tokens ilike ('%usd%')
	and b.value:parsed:type = 'burn'
	and SUCCEEDED = TRUE
  ), 
Inflow as (
select 
  	BLOCK_TIMESTAMP::date as date,
  	a.tx_id,
  	c.address_name as tokens,
  	b.value:parsed:info:amount/pow(10,8) as Volume	
from solana.core.fact_events a, lateral flatten(input => inner_instruction:instructions) b
join solana.core.dim_labels c on b.value:parsed:info:mint = c.address
where program_id = 'wormDTUJ6AWPNvk59vGQbDvGJmqbDTdgWgAqcLBCgUb'
	and block_timestamp >= '2022-12-26'
  	and block_timestamp <= current_date - 1
  	and tokens ilike ('%usd%')
	and b.value:parsed:type = 'mintTo'
	and SUCCEEDED = TRUE
)
select 
  	date,
	tokens,
	count(distinct a.tx_id) as outflow_txs,
	count(distinct b.tx_id) as inflow_txs,
	sum(a.Volume) as outflow_volume,
  	sum(outflow_volume*-1) over(order by date) as cum_outflow_vol,
	sum(b.Volume) as inflow_volume,
  	sum(inflow_volume) over(order by date) as cum_inflow_volume
from outflow a join inflow b using(date)
group by 1,2
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y=['outflow_txs', 'inflow_txs'])
    fig.update_layout(title_text='Daily # of Transferred Stablecoins Txs Via Bridges')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.bar(df, x='date', y=['outflow_volume', 'inflow_volume'])
    fig.update_layout(title_text='Daily Amount of Transferred Stablecoins Volume($) Via Bridges')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = px.area(df, x='date', y='cum_outflow_vol')
    fig.update_layout(title_text='Cumulative Outflowed Stablecoins Volume($) Via Bridges', showlegend=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.area(df, x='date', y='cum_inflow_volume')
    fig.update_layout(title_text='Cumulative Inflowed Stablecoins Volume($) Via Bridges', showlegend=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


fig = px.bar(df, x='date', y='outflow_txs', color='tokens')
fig.update_layout(title_text='Daily # of Outflow Txs of Stablecoins Txs Via Bridges')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig = px.bar(df, x='date', y='inflow_txs', color='tokens')
fig.update_layout(title_text='Daily # of Inflow Txs of Stablecoins Txs Via Bridges')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

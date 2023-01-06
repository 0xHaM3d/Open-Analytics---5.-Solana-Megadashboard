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
st.set_page_config(page_title='NFT Interaction', page_icon=':bar_chart:', layout='wide')
st.title('🎨 Secondary NFT Market')

st.write("")
st.write("")
st.subheader('Secondary NFT Market After Degods/y00ts News')


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
with priceTb as (
SELECT
RECORDED_HOUR::date as p_date,
avg(CLOSE) as SOLPrice
FROM solana.core.fact_token_prices_hourly
WHERE SYMBOL = 'SOL'
AND p_date >= '2022-12-01'
GROUP by 1
)
  select   
  	block_timestamp::date as date,
  	count(DISTINCT tx_id) as sales_tx_cnt,
  	count(DISTINCT PURCHASER) as buyer_cnt,
  	count(DISTINCT SELLER) as seller_cnt,
  	count(DISTINCT MINT) as nft_sales_cnt,
  	sum(SALES_AMOUNT*SOLPrice) as sales_usd_vol,
  	avg(SALES_AMOUNT*SOLPrice) as avg_price_usd,
  	sum(sales_tx_cnt) over (order by date) as cum_sales_tx_cnt,
  	sum(sales_usd_vol) over (order by date) as cum_sales_usd_vol
  from solana.core.fact_nft_sales s join priceTb p on s.BLOCK_TIMESTAMP::date = p.p_date
  where succeeded = TRUE
  and block_timestamp::date >= '2022-12-26'
  and block_timestamp::date <= CURRENT_DATE - 1
  GROUP by 1
"""

df = querying_pagination(df_query)
c1, c2 = st.columns(2)
with c1:
    fig = px.bar(df, x='date', y=['sales_tx_cnt', 'nft_sales_cnt'])
    fig.update_layout(title_text='Daily Sales Txs & Seld NFT Count')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.bar(df, x='date', y=['buyer_cnt', 'seller_cnt'])
    fig.update_layout(title_text='Daily # of Buyers & Sellers')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = px.area(df, x='date', y='cum_sales_tx_cnt')
    fig.update_layout(title_text='Cumulative Sales Txs Count', showlegend=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.area(df, x='date', y='cum_sales_usd_vol')
    fig.update_layout(title_text='Cumulative Sales Volume($)', showlegend=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    st.caption('Daily Sales Volume($) Over Time')
    st.line_chart(df, x='date', y='sales_usd_vol', width=400, height=400)
with c2:
    st.caption('Daily Average Price($) Over Time')
    st.line_chart(df, x='date', y='avg_price_usd', width=400, height=400)


st.write("")
st.write("")
st.subheader('Top 10 Collection Sales Performance')


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


# Top 10 Collection Sales Performance
df_query = """ 
with nft_tx_log AS (
SELECT 
  date_trunc('hour', block_timestamp) as date,
  marketplace,
  project_name,
  tx_id,
  PURCHASER, 
  SELLER, 
  SALES_AMOUNT,
  MINT
  FROM solana.core.fact_nft_sales a join solana.core.dim_nft_metadata b USING(mint)
),
hyperspace_sales_data AS (
SELECT *,
  project_name as project
FROM  nft_tx_log
),
project_details AS (
  SELECT 
  project_name,
  sum(SALES_AMOUNT) as "Total Volume (SOL)",
  max(DATE) as max_date, -- date of last 
  min(DATE) as min_date, 
  datediff('day', min_date, getdate()) as "Age (Days)",
  count(distinct tx_id) as "Sales Count",
  count(distinct PURCHASER) as "Buyers",
  count(distinct SELLER) as "Sellers",
  count(distinct MINT) as "Supply Sold"
FROM nft_tx_log 
GROUP BY 1
ORDER BY 2 DESC 
),
LAST7 AS ( -- sales volume in the last 7 days 
  SELECT
  project,
  count(distinct SELLER) as "7D Sellers",
  count(distinct PURCHASER) as "7D Buyers",
  count(tx_id) as "7D Tx",
  round(sum(SALES_AMOUNT),1) as "7D"
  FROM hyperspace_sales_data
    WHERE date BETWEEN DATEADD(HOUR, -168, GETDATE()) AND GETDATE()
GROUP BY Project
),
LAST14 AS (
  SELECT
  project,
  count(distinct SELLER) as "14D Sellers",
  count(distinct PURCHASER) as "14D Buyers",
  count(tx_id) as "14D Tx",
  round(sum(SALES_AMOUNT),1) as "14D"
  FROM hyperspace_sales_data
-- WHERE current_date - date < 14
    WHERE date BETWEEN DATEADD(HOUR, -336, GETDATE()) AND GETDATE()
GROUP BY Project
),
LAST30 AS ( -- sales volume in the last 30 days 
  SELECT
  Project,
  count(distinct SELLER) as "30D Sellers",
  count(distinct PURCHASER) as "30D Buyers",
  count(tx_id) as "30D Tx",
  round(sum(SALES_AMOUNT),1) as "30D"
FROM hyperspace_sales_data
 -- WHERE current_date - date < 30
    WHERE date BETWEEN DATEADD(HOUR, -720, GETDATE()) AND GETDATE()
GROUP BY Project -- to link up with project details later
)
  SELECT
  rank() over (order by "Total Volume (SOL)" desc) as "Rank",
  a.project_name as "Project",
   "Total Volume (SOL)",
  "Sales Count",
  "Supply Sold",  
  -- sales volume change
  CASE WHEN ROUND(("7D"-("14D"-"7D"))/nullif(("14D"-"7D"),0)*100,1) > 0 THEN 
  CONCAT(ROUND(("7D"-("14D"-"7D"))/nullif(("14D"-"7D"),0)*100,1), '%', '🟢 +') ELSE 
  CONCAT(ROUND(("7D"-("14D"-"7D"))/nullif(("14D"-"7D"),0)*100,1), '%', '🔴 ') END as "7D 🢒🢐 % Change",
  "7D" as "7D 🢒🢐",
  "14D" as "14D 🢒🢐",
  "30D" as "30D 🢒🢐",
  --- buyer interest
  CASE WHEN ROUND(("7D Buyers"-("14D Buyers"-"7D Buyers"))/nullif(("14D Buyers"-"7D Buyers"),0)*100,1) > 0 THEN 
  CONCAT(ROUND(("7D Buyers"-("14D Buyers"-"7D Buyers"))/nullif(("14D Buyers"-"7D Buyers"),0)*100,1), '%', '🟢 +') ELSE 
  CONCAT(ROUND(("7D Buyers"-("14D Buyers"-"7D Buyers"))/nullif(("14D Buyers"-"7D Buyers"),0)*100,1), '%', '🔴 ') END as "7D Buyers % Change",
  "7D Buyers", "14D Buyers",  "30D Buyers", 
  -- sales count (tx)
  "7D Tx", "14D Tx", "30D Tx",
  ROUND(("7D"-("14D"-"7D"))/nullif(("14D"-"7D"),0)*100,1) as "7D 🢒🢐 %"
FROM project_details a
LEFT JOIN LAST7 d ON d.Project = a.project_name
LEFT JOIN LAST14 e ON e.Project = a.project_name
LEFT JOIN LAST30 f ON f.Project = a.project_name
  WHERE "7D 🢒🢐 % Change" is not NULL
ORDER BY  "Total Volume (SOL)" DESC
LIMIT 10 
"""

df = querying_pagination(df_query)

c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['project'], y=df['7d 🢒🢐'], base='project'), secondary_y=False)
    fig.update_layout(title_text='7D Sales Volume($)')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['project'], y=df['7d 🢒🢐 %'], base='project'), secondary_y=False)
    fig.update_layout(title_text='7D Sales Volume($) % Change')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns(2)
with c1:
    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df['project'], y=df['7d buyers'], name='7d Buyers'), secondary_y=False)
    fig.add_trace(go.Bar(x=df['project'], y=df['7d tx'], name='7D Transactions'), secondary_y=False)
    fig.update_layout(title_text='7D Buyer & Sales Count')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    fig = px.pie(df, values='7d 🢒🢐 %', names='project', title='Share Volume of Top 10 Collections (7-Day)')
    fig.update_layout(legend_title='7-Day Volume', legend_y=1)
    fig.update_traces(textinfo='percent', textposition='inside')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


st.caption('Solana Top 10 Collection Sales Performance')
st.dataframe(df, use_container_width=True)
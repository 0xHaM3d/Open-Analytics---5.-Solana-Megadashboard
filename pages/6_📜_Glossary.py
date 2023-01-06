# Libraries
import streamlit as st

# [theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

# Layout
st.set_page_config(page_title='Definitions & Data Transparency', page_icon=':bar_chart:', layout='wide')
st.write("### 📜 Definitions & Data Transparency")

st.write("")
st.write("")
st.write("")
st.write("")

st.write(
    """
    The main data source is [**Flipside Crypto**](https://flipsidecrypto.xyz/). They offer free access to blockchain 
    data across a variety of different blockchains. 
    The SQL queries to extract the data to display are written by me and are automatically updated every
    24 hours. They all are open-sourced and feel free to reach out if you need access to anything in
    particular. 
    """
)
st.write(
    """
    #### Solana
    Solana is a blockchain designed to host decentralized and scalable applications. Solana is very fast in terms of 
    the number of transactions it can process and has much lower transaction fees than competing blockchains like Ethereum. 
    This blockchain works based on proof-of-stake technology. Therefore, users can participate in the chain by staking 
    their SOL(Native token of Solana blockchain) in the validators and as a result, receive participation yields.
    
    #### How are daily transactions counted?    
    To calculate daily transactions on Solana (as well as other chains transactions), 
    all transactions that interact with on protocols are included. 

    The users that have had as the first transactions called as **New Users**.
    All addresses that execute a transaction interacting on Solanas' ecosystem
    for the first time have been counted as **New Users** number.

    #### Popularity assessed by:
    The volume of active users on Solana per day 
    The adoption by new users per day
    Protocol popularity among all Solana users represents the ability to retain users, 
    whereas protocol popularity among Solana users represents the ability to attract users.

    #### How is the users growth(Cumulative) calculated?    
    On a given day, all addresses that execute a transaction interacting for the first time have been counted 
    towards the daily New Users number. 
    The cumulative curve is simply a progressive sum of the new daily users.  

    #### Programs
    An applicarions that are a collection of functions executed through one or many programs as On-chain state.
    This can be for example making a swap, staking a token, burning an NFT etc.
    
    [DeGods](https://www.degods.com/) is a digital art collection and global community of creators, developers, 
    entrepreneurs, athletes, artists, experimenters and innovators.
    
    [Y00ts](https://y00ts.com/) is An NFT collection on the Solana blockchain made by the same developers of DeGods and Dust Labs. 
    Duppies were the original idea before y00ts came. In early July 2022, the team announced an expected Duppies mint 
    around the end of July or early August.
    """

)

st.write("")
st.write("")
st.write("")
st.write("")

fig = st.write(
    """
                     ### Made with :red[❤] & Honor
    """
)
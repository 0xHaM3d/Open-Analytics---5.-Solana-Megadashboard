# Libraries
import streamlit as st

# from PIL import Image

# Layout
st.set_page_config(page_title='Is Solana dead?', page_icon=':bar_chart:', layout='wide')

st.write("")
st.write("")
st.write("")
st.header('Is Solana dead?')

st.write("")
st.write("")
st.write("### Let’s check the temperature on #solana now that the top 2 NFT projects are leaving $SOL! 👋")

st.write("")
st.write("")
st.write("")
st.write("")

st.write(
    """
    Solana hosts decentralized, scalable applications on blockchain. The Geneva-based Solana Foundation runs the 
    open-source project, which Solana Labs produced in San Francisco. Solana processes transactions faster and cheaper 
    than Ethereum. 
    
    The second half of 2022 saw a continued decline in the Solana blockchain's performance, prompting several key 
    players to look elsewhere for advancement. Magic Eden was one of the first platforms to publicly state its intent 
    to expand into cross-chain interactions. Solana's two most prominent PFP projects, DeGods and y00ts, have recently 
    announced that they will be leaving the network.

    On December 25th, the [DeGods](https://twitter.com/degodsnft/status/1607156858019794944?s=46&t=h1QcAy6W15nZ-BQY-es4Bg)
    and [y00ts](https://twitter.com/y00tsNFT) Twitter pages shared the news with a brief announcement that they planned 
    to build a bridge off of Solana in 2023. Although both projects are part of the same overarching organization, 
    they are technically splitting up because DeGods is building a bridge to Ethereum and y00ts is building a bridge to Polygon.

    This tool is designed and structured in multiple **Pages** that are accessible using the sidebar.
    Each of these Pages addresses a different category of the ecosystem to track the health of Solana network after this announcement. 
    Within each category (Activity, Swap & Transfer, Staking, etc.) you are able to access your desired class to narrow/expand the Solanas' 
    ecosystem since Degods/y00ts announcements. 

    All values for amounts, prices, and volumes are in **SOL & U.S. dollars** and the time frequency of the
    analysis was limited to the over **Launch date by day**.
    """
)

st.subheader('Methodology')
st.write(
    """
    The data for this analysis were selected from the [**Flipside Crypto**](https://flipsidecrypto.xyz/)
    data platform by using its **shroomDK(SDK)**. The codes for this tool are saved and accessible
     in its [**GitHub Repository**](https://github.com/0xHaM3d/Open-Analytics---5.-Solana-Megadashboard).

    As the queries are updated on a daily basis to cover the most recent data, there is a chance
    that viewers encounter inconsistent data through the app. Due to the heavy computational power required to execute
    the queries, and also the size of the raw data being too large, it may take a few minutes to reload the data,
    or by downloading the data and loading it from the repository itself. 

    Besides the codes and queries mentioned above, the following dashboards created using Flipside Crypto were used
    as the core references in developing the current tool:
    - [Open Analytics Bounty](https://app.flipsidecrypto.com/dashboard/open-analytics-bounty-solana-november-26-TdrGRS)
    - [Solana Staking Madness](https://app.flipsidecrypto.com/dashboard/solana-staking-madness-eoLPVq)
    - [Unique Solana Programs](https://app.flipsidecrypto.com/dashboard/unique-solana-programs-solana-NfmpZX)
    """
)


c1, c2 = st.columns(2)
with c1:
    st.info('**Developer/Analyst: [@0xHaM☰d](https://twitter.com/0xham3d_eth)**', icon="💻")
with c2:
    st.info('**Data: [Flipside Crypto](https://flipsidecrypto.xyz/)**', icon="🧠")
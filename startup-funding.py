import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('startup-cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month']=df['date'].dt.month

st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('select one', ['Startup', 'Investor', 'Overall Analysis'])

def investor_details(investor):
    st.title(investor)
    #load recent 5 investment
    last_five_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'amount', 'round']]

    st.subheader('Recent Five Investments')
    st.dataframe(last_five_df)
    # Biggest Investment
    col1, col2 = st.columns(2)
    with col1:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investments')
        # st.dataframe(biggest_investment)
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In')
        # st.dataframe(biggest_investment)
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Round Invested In')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage_series, labels=stage_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Invested In')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")
        st.pyplot(fig3)


    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('City Invested In')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)
    st.pyplot(fig4)

def load_overall_analysis():
    st.title('Overall Analysis')
    total = round(df['amount'].sum())

    #max amount invested
    max_in = round(df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0])

    #avg funding
    avg_in = round(df.groupby('startup')['amount'].mean().sort_values(ascending=False).head(1).values[0])

    # total funded startup
    no=df['startup'].nunique()

    col5,col6,col7,col8=st.columns(4)
    with col5:
         st.metric('Total', str(total) + 'Cr')
    with col6:
        st.metric('Max', str(max_in) + 'Cr')
    with col7:
        st.metric('Average', str(avg_in) + 'Cr')
    with col8:
        st.metric('Total Startup', str(no))
    st.header('MOM Graph')
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'].index, temp_df['amount'].values)
    st.pyplot(fig5)


if option =='Overall Analysis':

    #btn0 = st.sidebar.button('Overall Analysis')
   # if btn0:
    load_overall_analysis()

elif option =='Startup':
    st.sidebar.selectbox('Select one', sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    st.title('Startup')
else:
    selected_investor = st.sidebar.selectbox('Select one',  sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        investor_details(selected_investor)





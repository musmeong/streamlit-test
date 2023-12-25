import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "registered": "sum",
        "casual": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "cnt": "order_count",
        "registered": "registered_order_count",
        "casual": "casual_order_count"
    }, inplace=True)
    
    return daily_orders_df

df = pd.read_csv("day.csv")

datetime_columns = ["dteday"]
df.sort_values(by="dteday", inplace=True)
df.reset_index(inplace=True)
 
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])

min_date = df["dteday"].min()
max_date = df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://png.pngtree.com/png-vector/20220705/ourmid/pngtree-cat-logo-black-png-image_5682480.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
# Create proportion of each user category
daily_orders_df['casual_prop'] = daily_orders_df['casual_order_count']/daily_orders_df['order_count']
daily_orders_df['registered_prop'] = daily_orders_df['registered_order_count']/daily_orders_df['order_count']

st.header('Dicoding Submission Dashboard by Muhamad Mustain')

st.subheader('Overall Orders')

order = daily_orders_df.order_count.sum()
st.metric("Overall Orders", value=order) 

fig, ax = plt.subplots(figsize=(16, 5))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader('Orders per User Category')
 
col1, col2 = st.columns(2)
 
with col1:
    casual_user = daily_orders_df.casual_order_count.sum()
    st.metric("Casual Orders", value=casual_user)
 
with col2:
    reg_user = daily_orders_df.registered_order_count.sum() 
    st.metric("Registered Users", value=reg_user)

casual_col = (0.12156862745098039, 0.4666666666666667, 0.7058823529411765)
reg_col = (1.0, 0.4980392156862745, 0.054901960784313725)

optchart = st.radio(
    label="Show Chart as...",
    options=('Normal', 'Stacked'),
    horizontal=True
)

if optchart == 'Normal':
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.plot(
        daily_orders_df["dteday"],
        daily_orders_df["casual_order_count"],
        marker='o', 
        linewidth=2,
        color=casual_col,
        label='Casual'
    )
    ax.plot(
        daily_orders_df["dteday"],
        daily_orders_df["registered_order_count"],
        marker='o', 
        linewidth=2,
        color=reg_col,
        label='Registered'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend()
    
    st.pyplot(fig)
else:
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.stackplot(
        daily_orders_df["dteday"],
        [daily_orders_df["casual_prop"], daily_orders_df["registered_prop"]],
        labels=['Casual', 'Registered']
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.legend()
    
    st.pyplot(fig)

st.subheader('Scatterplot and Correlation between Two Variables')

col1 = st.selectbox(
    label="Select column 1",
    options=('season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt')
)
col2 = st.selectbox(
    label="Select column 2",
    options=('season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt')
)

corr = main_df[[col1, col2]].corr().values[0][1]
st.metric("Correlation", value=corr) 

fig, ax = plt.subplots(figsize=(16, 5))
ax.scatter(
    main_df[col1],
    main_df[col2],
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


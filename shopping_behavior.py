import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

st.set_page_config(page_title=" Dashboard Creation", layout="wide")

st.title("📊 Shopping Behavior Dashboard")

st.write('Shopping Behavior Analysis')

df=pd.read_csv('shopping_behavior_updated.csv')
print(df)

#------------------Side bar Data Entry----------------------------------
st.sidebar.header("Data Entry")
filtered_df=df.copy()

gender=st.sidebar.selectbox("Select Gender",['All']+df.Gender.unique().tolist())
season=st.sidebar.selectbox("Select Season",['All']+df.Season.unique().tolist())
category=st.sidebar.selectbox("Select Category",['All']+df.Category.unique().tolist())
item_purchased=st.sidebar.selectbox("Select Item Purchased",['All']+df['Item Purchased'].unique().tolist())
payment_method=st.sidebar.selectbox("Select Payment Method",['All']+df['Payment Method'].unique().tolist())


if gender!='All':
    filtered_df=filtered_df[filtered_df.Gender==gender]
if season!='All':
    filtered_df=filtered_df[filtered_df.Season==season]
if category!='All':
    filtered_df=filtered_df[filtered_df.Category==category]
if item_purchased!='All':
    filtered_df=filtered_df[filtered_df['Item Purchased']==item_purchased]
if payment_method!='All':
    filtered_df=filtered_df[filtered_df['Payment Method']==payment_method]   

#----------------Showing KPI data--------------
col1,col2,col3=st.columns(3)
col1.metric("Total sale ",f"${filtered_df['Purchase Amount (USD)'].sum()}")
col2.metric("Total Customer ",f"{filtered_df['Customer ID'].count()}")
col3.metric("Gender",f"{filtered_df['Gender'].count()}")


#--------------Showing Tabel---------------------------
col1,col2,col3,col4=st.columns(4)
with col1:
    sales=filtered_df.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
    fig = px.bar(
        sales,
        x='Category',
        y='Purchase Amount (USD)',
        title='Total Purchase Amount by Category'
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:
    sales=filtered_df.groupby('Item Purchased')['Purchase Amount (USD)'].sum().reset_index()
    fig = px.bar(
        sales,
        x='Item Purchased',
        y='Purchase Amount (USD)',
        title='Total Purchase Amount by Item',
        
    )
    st.plotly_chart(fig)

with col3:
    sales=filtered_df.groupby('Payment Method')['Purchase Amount (USD)'].sum().reset_index()
    fig = px.bar(
        sales,
        x='Payment Method',
        y='Purchase Amount (USD)',
        title='Total Amount by payment',
        
    )
    st.plotly_chart(fig)

with col4:
    sales=filtered_df.groupby('Gender')['Purchase Amount (USD)'].sum().reset_index()
    fig = px.pie(
    sales,
    values="Purchase Amount (USD)",
    names="Gender",
    title="Sales Amount by Gender"
)

st.plotly_chart(fig, use_container_width=True)




st.write(filtered_df)
print(filtered_df)



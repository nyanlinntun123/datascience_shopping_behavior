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

conditions=[
    (df['Age'] >= 18) & (df['Age'] <= 26),
    (df['Age'] > 26) &  (df['Age'] <= 35),
    (df['Age'] > 35) &  (df['Age'] <= 50),
    (df['Age'] > 50)    
]
values=['Young Age(18 to under 26)','Early Professional(26 and under 35)',' Middle Age(35 and under 50)','Over 50']
df['New Age']=np.select(conditions,values,default='Unknown')

print(df)

#------------------Side bar Data Entry----------------------------------
st.sidebar.header("Data Entry")
filtered_df=df.copy()

gender=st.sidebar.selectbox("Select Gender",['All']+df.Gender.unique().tolist())
season=st.sidebar.selectbox("Select Season",['All']+df.Season.unique().tolist())
category=st.sidebar.selectbox("Select Category",['All']+df.Category.unique().tolist())
age=st.sidebar.selectbox("Select Age",['All']+df['New Age'].unique().tolist())
payment_method=st.sidebar.selectbox("Select Payment Method",['All']+df['Payment Method'].unique().tolist())


if gender!='All':
    filtered_df=filtered_df[filtered_df.Gender==gender]
if season!='All':
    filtered_df=filtered_df[filtered_df.Season==season]
if category!='All':
    filtered_df=filtered_df[filtered_df.Category==category]
if age!='All':
    filtered_df=filtered_df[filtered_df['New Age']==age]
if payment_method!='All':
    filtered_df=filtered_df[filtered_df['Payment Method']==payment_method]   

#----------------Showing KPI data--------------
col1,col2,col3,col4=st.columns(4)
col1.metric("Total sale ",f"${filtered_df['Purchase Amount (USD)'].sum()}")
col2.metric("Total Customer ",f"{filtered_df['Customer ID'].count()}")
col3.metric("Female",f"{filtered_df[filtered_df['Gender']=='Female'].shape[0]}")
col4.metric("Female",f"{filtered_df[filtered_df['Gender']=='Male'].shape[0]}")


#--------------Showing Tabel---------------------------
col1,col2,col3=st.columns(3)
with col1:
    sales=filtered_df.groupby(['Category','Gender'])['Purchase Amount (USD)'].sum().reset_index()
    fig = px.bar(
        sales,
        x='Category',
        y='Purchase Amount (USD)',
        color='Gender',
        barmode="group",
        title='Total Purchase Amount by Category',
        text='Purchase Amount (USD)'
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:
    sales=filtered_df.groupby('Item Purchased')['Purchase Amount (USD)'].sum().reset_index()
    fig = px.bar(
        sales,
        x='Item Purchased',
        y='Purchase Amount (USD)',
        title='Total Purchase Amount by Item',
        text='Purchase Amount (USD)'
        
    )
    st.plotly_chart(fig)

with col3:
    sales=filtered_df.groupby(['Payment Method','Gender'])['Purchase Amount (USD)'].sum().reset_index()
    fig = px.bar(
        sales,
        x='Payment Method',
        y='Purchase Amount (USD)',
        color='Gender',
        barmode="group",
        title='Total Amount by payment',
        text='Purchase Amount (USD)'
        
    )
    st.plotly_chart(fig)

with col1:
    sales=filtered_df.groupby('Gender')['Purchase Amount (USD)'].sum().reset_index()
    fig = px.pie(
    sales,
    values="Purchase Amount (USD)",
    names="Gender",
    title="Sales Amount by Gender"
    
)
st.plotly_chart(fig)

with col2:
    sales=filtered_df.groupby('New Age')['Purchase Amount (USD)'].sum().reset_index()
    fig = px.pie(
    sales,
    values="Purchase Amount (USD)",
    names="New Age",
    title="Sales Amount by Age"
)


st.plotly_chart(fig)


#-------------Multi line chart
col1,col2=st.columns(2)
with col1:
    sales=filtered_df.groupby(['Season','Category'])['Purchase Amount (USD)'].sum().reset_index()
    fig=px.line(sales,
                x='Season',
                y='Purchase Amount (USD)',
                color='Category',
                markers=True,
                title='Sales per category in season')
               
    st.plotly_chart(fig)

with col2:
    sales=filtered_df.groupby(['Shipping Type','Category'])['Purchase Amount (USD)'].sum().reset_index()
    fig=px.line(sales,
                x='Shipping Type',
                y='Purchase Amount (USD)',
                color='Category',
                markers=True,
                title='Sales per category by shipping type')
    st.plotly_chart(fig)





st.write(filtered_df)
print(filtered_df)



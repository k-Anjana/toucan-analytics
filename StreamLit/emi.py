from matplotlib import pyplot as plt
import streamlit as st
import requests
import pandas as pd
import altair as alt

emi_list =[]
customer_list =[]



if st.button('GET'):

    get_method=requests.get('http://127.0.0.1:8000/index/')
    if get_method.status_code==200:
        data=get_method.json()
        for item in data:
            emi_list.append(item['EMI_paid_on_time'])
            customer_list.append(item['total_customers'])
    else:
        st.write(get_method.status_code)

   
source = pd.DataFrame({
    'EMI Paid On Time': emi_list,
    'Number of customers': customer_list
 })

bar_chart = alt.Chart(source).mark_bar().encode(
    x='EMI Paid On Time:O',
    y='Number of customers:Q',
)

st.altair_chart(bar_chart, use_container_width=True)

if st.button('GET pie char'):
    
    st.header("PIE Chart")
    #  User input form
    url = "http://127.0.0.1:8000/pie/"
    response = requests.get(url)
    if response.status_code == 200:
    # Extract the data from the response
        data = response.json()
        labels = data['labels']
        sizes = data['sizes']
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    
        explode = [0,0,0,0,0,0]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)
    
    else:
        st.error(f'Error: {response.status_code}')
    
    
payment_list =[]
customer_list =[]

if st.button('GET PAYMENT'):
   
    st.header("PAYMENT GRAPH")
    get_method=requests.get('http://127.0.0.1:8000/payment/')
    if get_method.status_code==200:
        data=get_method.json()
        for item in data:
            payment_list.append(item['mode_of_payments'])
            customer_list.append(item['total_customers'])
    else:
        st.write(get_method.status_code)

   
source = pd.DataFrame({
    'Mode of Payment': payment_list,
    'Number of customers': customer_list
 })

bar_chart = alt.Chart(source).mark_bar().encode(
    x='Mode of Payment:O',
    y='Number of customers:Q',
)

st.altair_chart(bar_chart, use_container_width=True)

if st.button('GET TABLE'):

    get_method=requests.get('http://127.0.0.1:8000/table')
    if get_method.status_code == 200:
          # Extract the data from the response
        data = get_method.json()
        customer = data['customer']
        mode = data['values']
        
   
        data = {
            'Customer Id': [i for i in customer],
            'Frequent mode of Transanction': [i for i in mode],
        }
        df = pd.DataFrame(data)
        st.dataframe(df)
       
        
    else:
        st.error(f'Error: {get_method.status_code}')
        
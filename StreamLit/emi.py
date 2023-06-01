from matplotlib import pyplot as plt
import streamlit as st
import requests
import pandas as pd
import altair as alt

# emi graph streamlit code 
col1,col2 = st.columns(2,gap="large")

with col1:
    emi_list =[]
    customer_list =[]

    if st.button('GET EMI GRAPH'):
        st.header("EMI GRAPH")
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
    # color = alt.Color("EMI Paid On Time")
)

st.altair_chart(bar_chart, use_container_width=True)

# pichart streamlit code
with col2:
    if st.button('GET PIE GRAPH'):
        st.header("PIE Chart")
        response = requests.get("http://127.0.0.1:8000/pichart/")
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

col3,col4 = st.columns(2,gap="large")
# mode_of_payment code

with col3:
    payment_list =[]
    customer_list =[]

    if st.button('GET PAYMENT GRAPH'):
        st.header(":red[PAYMENT GRAPH]")
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

# code for table 
with col4:
    if st.button('GET TABLE'):
        get_method=requests.get('http://127.0.0.1:8000/table')
        if get_method.status_code == 200:
        # Extract the data from the response
            data = get_method.json()
            customer = data['customer']
            mode = data['values']
        
    # Create a sample data frame
            data = {
                'Customer Id': [i for i in customer],
                'Frequent mode of Transanction': [i for i in mode],
            }
            df = pd.DataFrame(data)
            st.dataframe(df)  
        else:
            st.error(f'Error: {get_method.status_code}')

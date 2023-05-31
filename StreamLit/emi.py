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

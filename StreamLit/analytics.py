import streamlit as st
import matplotlib.pyplot as plt
import requests
import json
import streamlit as st
from django.http import request
import streamlit as st
import altair as alt
import pandas as pd
import datetime
# col1, col2= st.columns(2)

# data = {
#             "title": "Streamlit Request",
#             "body": "This is a sample request",
#             "userId": 1
#         }
# with col1:
#     if st.button('Post'):
#         response_post = requests.post("http://127.0.0.1:8000/analytics", data=data)
#         if response_post.status_code == 200:
#             st.write("POST request successful!")
#             st.write(data)
#         else:
#             st.write(f"POST request failed! {response_post.status_code}")
#     else:
#         st.write('click here')

# with col2:
#     a=st.button
#     if a('get'):
#         response_get = requests.get("http://127.0.0.1:8000/analytics")
#         if response_get.status_code == 200:
#             st.write("GET request successful!")
#             st.write("Response:")
#             st.write(response_get.json())
            
            
#         else:
#             st.write(f"GET request failed! {response_get.status_code}")
#     else:
#         st.write('click here')

    # "2023-01-01", "2023-12-31"

min_date = datetime.date(2023, 1, 1)
max_date = datetime.date(2023, 12, 31)

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    st.write("")
with col2:
    st.write("")
with col3:
    st.write("")
with col4:
    st.write("")
with col5:
    st.write("")
with col6:
    st.write("")
with col7:
    start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date,value=min_date)
with col8:
    end_date = st.date_input("End Date", min_value=min_date, max_value=max_date,value=max_date)


if start_date and end_date:
    if start_date > end_date:
        st.error("Error: Start Date must be before End Date.")
    else:
        params = {
        "start_date": str(start_date),
        "end_date": str(end_date)
    }
col1, col2 = st.columns(2, gap="large")
with col1:
    if st.button('GET PIE GRAPH'):
        st.header("PIE Chart")
    #  User input form
        response=requests.get('http://127.0.0.1:8000/pie',params=params)
    # url = "http://127.0.0.1:8000/analytics/?type=pie"
    # response = requests.get(url)
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

with col2:
    emi_list =[]
    customer_list =[]

    if st.button('GET EMI graph '):
        st.header("EMI graph")
        get_method=requests.get('http://127.0.0.1:8000/emi/')
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

#user_colour = st.color_picker(label='Choose a colour for your plot')

    bar_chart = alt.Chart(source).mark_bar().encode(
        x='EMI Paid On Time:O',
        y='Number of customers:Q',
        # c=user_colour,
    )

    st.altair_chart(bar_chart, use_container_width=True)


col3, col4 = st.columns(2, gap="large")
with col3:
#bargraph 
    payment_list =[]
    customer_list =[]

    if st.button('GET PAYMENT GRAPH'):
        st.header("payment graph")
        get_method=requests.get('http://127.0.0.1:8000/payment/',params=params)
        if get_method.status_code==200:
            data=get_method.json()
            for item in data:
                payment_list.append(item['mode_of_payments'])
                customer_list.append(item['total_customers'])
        else:
            st.write(get_method.status_code)


    source = pd.DataFrame({
        'mode_of_payments': payment_list,
        'Number of customers': customer_list
    })


    bar_chart = alt.Chart(source).mark_bar().encode(
        x='mode_of_payments:O',
        y='Number of customers:Q',
    
    )

    st.altair_chart(bar_chart, use_container_width=True)

with col4:
# TABLE
    if st.button('GET TABLE'):
        st.header("Table")
        get_method=requests.get('http://127.0.0.1:8000/table',params=params)
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
        # # Add a serial number column
        # df.insert(0, 'S.No', range(1, len(df) + 1))
        # # Convert DataFrame to HTML table without index column
        # html_table = df.to_html(index=False)
        # # Display the table
        # st.write(html_table, unsafe_allow_html=True)
        # st.write('\n')
        else:
            st.error(f'Error: {get_method.status_code}')
    
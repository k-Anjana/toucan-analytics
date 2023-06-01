import streamlit as st
import matplotlib.pyplot as plt
import requests
import json
import streamlit as st
from django.http import request
import streamlit as st
import altair as alt
import pandas as pd

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


st.header("PIE Chart")
    #  User input form
url = "http://127.0.0.1:8000/analytics/?type=pie"
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

emi_list =[]
customer_list =[]



if st.button('GET'):

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
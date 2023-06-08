import datetime
from matplotlib import pyplot as plt
import streamlit as st
import requests
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

local_host = 'http://localhost:8000/'


# Create a session state object
session_state = st.session_state

def get_jwt_token(username, password):
    url = local_host + 'api/token/'
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access']
        return access_token
    else:
        return None
    

def get_data(token):
    url = local_host + 'data/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def login_page():
    st.markdown("<h1 style='text-align: center; '>Login Page</h1> <br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2,col3,col4,col5 = st.columns(5)
        with col3:
            login_button = st.button(":blue[Login]")

    if login_button:
        token = get_jwt_token(username, password)
        if token:
            data = get_data(token)
            if data:
                return True  

        else:
            st.error("Invalid username or password.")
            return False  # Return False to indicate unsuccessful login

# Display the login page
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login_success = login_page()

    if login_success:
        st.session_state['logged_in'] = True
        st.experimental_rerun()
else:
    
    st.markdown("<u><h1 style='text-align: center'>Toucan Analytics</h1><u> <br>", unsafe_allow_html=True)

    # emi graph streamlit code 
    col1,col2 = st.columns(2,gap="large")

    with col1:
        emi_list =[]
        customer_list =[]


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
        color_scale = alt.Scale(range=['pink','blue'])
        bar_chart = alt.Chart(source).mark_bar().encode(
            x='EMI Paid On Time:O',
            y='Number of customers:Q',
            color = alt.Color('EMI Paid On Time:N',scale = color_scale)

        
        )

        st.altair_chart(bar_chart, use_container_width=True)

    # pichart streamlit code
    with col2:
        
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
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',startangle=90)#pie() function creats a pie chart
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)
        
        else:
            st.error(f'Error: {response.status_code}')

    col3,col4 = st.columns(2,gap="large")
    # mode_of_payment code

    with col3:
        payment_list =[]
        customer_list =[]

        
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
            color = alt.Color('Mode of Payment:N')      # random colours
        )

        st.altair_chart(bar_chart, use_container_width=True)

    # code for table 
    with col4:
        st.header("CUSTOMER TABLE")
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
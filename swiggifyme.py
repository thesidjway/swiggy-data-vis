import streamlit as st
import pandas as pd
import json

f = open("data/orders_sid.json")
order_data = json.load(f)

for num, i in enumerate(order_data):
    # Iterate through all orders
    df = pd.DataFrame.from_dict(i, orient='index')
    # print(df)
    print(num)

st.title('SwiggifyMe!')
st.header('Visualize your Swiggy order statistics here.')
st.caption('Please log in to your Swiggy account on your web browser, and click the button below. We do not store any of your data!')

if st.button('Click here to get your data'):
     st.write('Why hello there')
else:
     st.write('Goodbye')

st.caption('Developed by @thesidjway and @shashwatg1 in 12 hrs as a part of the half-day build hackathon, organized by @louispereira')
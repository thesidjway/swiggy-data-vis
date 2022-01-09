import streamlit as st
import streamlit.components.v1 as components 
import pandas as pd
import json
import datetime
import math

f = open("data/orders_sid.json")
order_data = json.load(f)
df = pd.DataFrame(order_data)

# st.dataframe(df)
time_to_start_end = {
    0 : ('midnight', '1:00AM'),
    1 : ('1:00AM', '2:00AM'),
    2 : ('2:00AM', '3:00AM'),
    3 : ('3:00AM', '4:00AM'),
    4 : ('4:00AM', '5:00AM'),
    5 : ('5:00AM', '6:00AM'),
    6 : ('6:00AM', '7:00AM'),
    7 : ('7:00AM', '8:00AM'),
    8 : ('8:00AM', '9:00AM'),
    9 : ('9:00AM', '10:00AM'),
    10 : ('10:00AM', '11:00AM'),
    11 : ('11:00AM', 'noon'),
    12 : ('noon', '1:00PM'),
    13 : ('1:00PM', '2:00PM'),
    14 : ('2:00PM', '3:00PM'),
    15 : ('3:00PM', '4:00PM'),
    16 : ('4:00PM', '5:00PM'),
    17 : ('5:00PM', '6:00PM'),
    18 : ('6:00PM', '7:00PM'),
    19 : ('7:00PM', '8:00PM'),
    20 : ('8:00PM', '9:00PM'),
    21 : ('9:00PM', '10:00PM'),
    22 : ('10:00PM', '11:00PM'),
    23 : ('11:00PM', 'midnight'),
}

for num, i in enumerate(order_data):
    # Iterate through all orders
    df = pd.DataFrame.from_dict(i, orient='index')
    # print(df)
    print(num)

st.title('SwiggifyMe!')
st.header('Visualize your Swiggy order statistics here.')

components.html('<script src="https://cdn.jsdelivr.net/gh/thesidjway/swiggy-data-vis@main/test_scripts/getdata.js"></script> <input type = "button" onclick = "openInNewTab("https://google.com");" value = "Display">', height=100)


st.caption('Please log in to your Swiggy account on your web browser, and click the button below. We do not store any of your data!')

if st.button('Click here to get your data'):
    #first_order_date
    first_order_time = 1515496380
    #num_orders
    num_orders = 500
    #total_spend
    total_spend = 100000
    #average_spend
    average_spend = total_spend/num_orders
    #top_10_orders
    top_10_dishes = [('Chicken', 50), ('Chicken', 50), ('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50)]
    #top_10_restaurants
    top_10_restaurants = [('Dominos', 50), ('Dominos', 50), ('Dominos', 50),('Dominos', 50),('Dominos', 50),('Dominos', 50),('Dominos', 50),('Dominos', 50),('Dominos', 50), ('Dominos', 50)]
    #top_10_categories
    top_10_categories = [('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50)] 
    #veg/nonveg/egg_split
    veg_nonveg_egg_split = [0.3, 0.6, 0.1]
    #day_of_week_split
    day_of_week_split = [(60, 'Monday'), (50, 'Tuesday'), (40, 'Wednesday'), (30, 'Thursday'), (20, 'Friday'), (15, 'Saturday'), (10, 'Sunday')]
    #month_split
    month_split = [(60, 'February'), (50, 'January'), (40, 'May'), (30, 'November'), (25, 'March'), (24, 'June'), (22, 'December'), (20, 'August'), (15, 'September'), (14, 'October'), (10, 'April'), (8, 'July')]
    #year_split
    year_split = [(100, 2021), (90, 2020), (80, 2019), (70, 2016), (60, 2022), (50, 2017), (20, 2018)]
    #hour_split
    hour_split = [10, 5, 5, 3, 6, 8, 6, 15, 20, 32, 40, 30, 22, 25, 20, 16, 15, 10, 9, 2, 10, 2, 2, 1]
    #top_city
    top_city = "Bangalore"
    #waiting
    waiting = 50000
    #waiting_per_order
    waiting_per_order = waiting / num_orders
    #total_savings
    total_savings = 10000
    #distance
    total_distance = 1000
    #average_distance
    average_distance = total_distance / num_orders
    #map
    latlon = [(20, 40), (20, 40), (20, 40), (20, 40)]
    #streak
    streak = 10

    date = datetime.datetime.fromtimestamp(first_order_time)

    line1 = f"Since your first order on {date}, you've ordered {num_orders} times, spent ₹{total_spend} at an average of ₹{average_spend} per order"
    st.subheader(line1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Top Dish", str(top_10_dishes[0][0]))
    col2.metric("Top Restaurant", str(top_10_restaurants[0][0]))
    col3.metric("Top Category", str(top_10_categories[0][0]))

    #TODO: Show top 10 here

    line2 = f"Your most prolific year was {year_split[0][1]}, month was {month_split[0][1]} and day was {day_of_week_split[0][1]}. The city you ordered most in was: {top_city}, but you'd have known that already!"
    st.subheader(line2)

    max_index = hour_split.index(max(hour_split))

    line3 = f"You ordered the most between: {time_to_start_end[max_index][0]} and {time_to_start_end[max_index][1]}: {hour_split[max_index]} times"
    st.subheader(line3)

    #TODO: Show all timewise data here

    line4 = f"You spent {math.ceil(waiting/60)} hours waiting for your orders, that's an average of {waiting_per_order} minutes per order"
    st.subheader(line4)

    line5 = f"You ordered from restaurants that were, on an average, {average_distance}km away. That means, Swiggy delivery men travelled {total_distance}km just to deliver your orders. Another reason to tip them well!"
    st.subheader(line5)

    line6 = f"Here's a map of all the places you ordered from!"
    st.subheader(line6)

    #Show map here!

    line7 = f"You had an ordering streak of {streak} days between <date1> and <date2>, wow!"
    st.subheader(line7)

payment_button_url = r'<form><script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_Ihe4fKr1AVERm8" async> </script></form>'

components.html(payment_button_url, height = 1000)

st.caption('Developed by @thesidjway and @shashwatg1 in 12 hrs as a part of the half-day build hackathon, organized by @louispereira')
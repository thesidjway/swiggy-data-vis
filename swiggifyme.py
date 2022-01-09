import streamlit as st
import streamlit.components.v1 as components 
import pandas as pd
import json
import datetime
import math
import time

st.title('SwiggifyMe!')
st.header('Visualize your Swiggy order statistics here.')

st.caption("Follow these instructions and create a JSON on swiggy.com. Upload the JSON here (We don't intend to access the data in any way or form)")
st.caption("1. Go to www.swiggy.com and log in to your account")
st.caption("2. Go to https://www.swiggy.com/my-account/orders")
st.caption("3. Press F12 on your browser, paste the script below into the console")
st.caption("4. Upload the downloaded orders.json here!")

code = '''order_array=[]
order_id=''
page = 1
try {
    while(true){
        var xmlHttp = new XMLHttpRequest()
        xmlHttp.open("GET", "https://www.swiggy.com/dapi/order/all?order_id="+order_id, false)
        xmlHttp.send(null)
        resText=xmlHttp.responseText
        var resJSON = JSON.parse(resText)
        order_id=resJSON.data.orders[resJSON.data.orders.length-1].order_id
        order_array=order_array.concat(resJSON.data.orders)
        console.log("On page: "+page+" with last order id: "+order_id)
        page++
    }
}
catch(err) {
    const a = document.createElement("a");
    const file = new Blob([JSON.stringify(order_array, null, 2)], { type: "text/plain" });
    a.href = URL.createObjectURL(file);
    a.download = "orders.json";
    a.click();
    console.log(order_array)
}
'''

st.code(code, language='javascript')

up_data_file = st.file_uploader("Upload JSON",type=["json"])

if up_data_file is not None:
    order_data = json.load(up_data_file)
    df = pd.DataFrame(order_data)
    #Initialise Metrics
    first_order_time = time.time()
    num_orders = 0
    total_spend = 0
    waiting = 0
    total_savings = 0
    total_distance = 0
    latlon = []

    for index, row in df.iterrows():
        A = row['ordered_time_in_seconds']
        first_order_time = min(first_order_time, A)
        num_orders += 1
        total_spend += float(row['order_total'])
        total_savings += float(row['order_discount'])
        total_distance += float(row['restaurant_customer_distance'])
        waiting += float(row['delivery_time_in_seconds'])
        latlontup = tuple(float(s) for s in row['restaurant_lat_lng'].split (","))
        latlon.append( latlontup )

    average_spend = total_spend/num_orders
    waiting_per_order = (waiting/60) / num_orders
    average_distance = total_distance / num_orders
    city_split = df.restaurant_city_name.value_counts()

    top_10_dishes = [('Chicken', 50), ('Chicken', 50), ('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50),('Chicken', 50)]
    top_10_restaurants = [('Dominos', 50), ('Dominos', 50), ('Dominos', 50),('Dominos', 50),('Dominos', 50),('Dominos', 50),('Dominos', 50),('Dominos', 50),('Dominos', 50), ('Dominos', 50)]
    top_10_categories = [('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50), ('Pizza', 50)] 
    veg_nonveg_egg_split = [0.3, 0.6, 0.1]
    day_of_week_split = [(60, 'Monday'), (50, 'Tuesday'), (40, 'Wednesday'), (30, 'Thursday'), (20, 'Friday'), (15, 'Saturday'), (10, 'Sunday')]
    month_split = [(60, 'February'), (50, 'January'), (40, 'May'), (30, 'November'), (25, 'March'), (24, 'June'), (22, 'December'), (20, 'August'), (15, 'September'), (14, 'October'), (10, 'April'), (8, 'July')]
    year_split = [(100, 2021), (90, 2020), (80, 2019), (70, 2016), (60, 2022), (50, 2017), (20, 2018)]
    hour_split = [10, 5, 5, 3, 6, 8, 6, 15, 20, 32, 40, 30, 22, 25, 20, 16, 15, 10, 9, 2, 10, 2, 2, 1]
    top_city = "Bangalore"
    streak = 10

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
        
    date = datetime.datetime.fromtimestamp(first_order_time)
    line1 = f"Since your first order on {date}, you've ordered {num_orders} times, spent ₹{total_spend} at an average of ₹{average_spend} per order"
    st.subheader(line1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Top Dish", str(top_10_dishes[0][0]))
    col2.metric("Top Restaurant", str(top_10_restaurants[0][0]))
    col3.metric("Top Category", str(top_10_categories[0][0]))

    #TODO: Show top 10 here
    top10data = {
        'Category': [str(top_10_categories[0][0])],
        'Restaurant': [str(top_10_restaurants[0][0])],
        'Dish': [str(top_10_dishes[0][0])]
    }
    top10tab = pd.DataFrame(top10data)
    st.table(top10tab)

    line2 = f"Your most prolific year was {year_split[0][1]}, month was {month_split[0][1]} and day was {day_of_week_split[0][1]}. The city you ordered most in was: {top_city}, but you'd have known that already!"
    st.subheader(line2)

    max_index = hour_split.index(max(hour_split))

    line3 = f"You ordered the most between: {time_to_start_end[max_index][0]} and {time_to_start_end[max_index][1]}: {hour_split[max_index]} times"
    st.subheader(line3)

    #TODO: Show all timewise data here

    line4 = f"You spent {math.ceil(waiting/3600)} hours waiting for your orders, that's an average of {waiting_per_order} minutes per order"
    st.subheader(line4)

    line5 = f"You ordered from restaurants that were, on an average, {average_distance} KM away. That means, Swiggy delivery men travelled {total_distance} KM just to deliver your orders. Another reason to tip them well!"
    st.subheader(line5)

    line6 = f"Here's a map of all the places you ordered from! (In case of multiple geographies, please zoom in using your mouse)"
    st.subheader(line6)
    #Show map here!
    mapdf = pd.DataFrame(
        latlon, columns = ['lat', 'lon']
    )
    st.map(mapdf)

    line7 = f"You had an ordering streak of {streak} days between <date1> and <date2>, wow!"
    st.subheader(line7)

payment_button_url = r'<form><script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_Ihe4fKr1AVERm8" async> </script></form>'

components.html(payment_button_url, height = 1000)

st.caption('Developed by @thesidjway and @shashwatg1 in 12 hrs as a part of the half-day build hackathon, organized by @louispereira')
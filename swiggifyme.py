import streamlit as st
import streamlit.components.v1 as components 
import pandas as pd
import json
import datetime
import math
import time
import operator

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

def day_time_month_year_split(timestrings):
    day_of_week_split = [0,0,0,0,0,0,0]
    hour_split = [0]*24
    month_split = [0]*12
    year_split = dict()
    for i in timestrings:
        year = int(i.split('-')[0])
        month = int(i.split('-')[1])
        date = int(i.split('-')[2].split(' ')[0])
        hour = int(i.split(' ')[-1].split(':')[0])
        day = datetime.datetime(year, month, date, hour, 0, 0).weekday()
        day_of_week_split[day] += 1
        month_split[month - 1] += 1
        hour_split[hour] += 1
        if year not in year_split.keys():
            year_split[year] = 1
        else:
            year_split[year] += 1
    
    return day_of_week_split, hour_split, month_split, year_split 


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
    isVeg = [0, 0, 0]
    totalOrders = 0
    dishes = []
    category = []

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
        for row1 in row['order_items']:
            isVeg[int(row1['is_veg'])] += 1
            totalOrders += 1
            dishes.append(row1['name'])
            category.append(row1['category_details']['category'])

    average_spend = total_spend/num_orders
    waiting_per_order = (waiting/60) / num_orders
    average_distance = total_distance / num_orders
    city_split = df.restaurant_city_name.value_counts()
    restaurant_split = df.restaurant_name.value_counts()
    dishes_split = {}
    for items in dishes:
        dishes_split[items] = dishes.count(items)
    dishes_split_s = dict(sorted(dishes_split.items(), key=operator.itemgetter(1),reverse=True))
    category_split = {}
    for items in category:
        category_split[items] = category.count(items)
    category_split_s = dict(sorted(category_split.items(), key=operator.itemgetter(1),reverse=True))

    timestamps = df.order_time
    day_of_week_split, hour_split, month_split, year_split = day_time_month_year_split(timestamps)

    top_city = city_split.index[0]
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
    month_to_name = {
        0 : 'January',
        1 : 'February',
        2 : 'March',
        3 : 'April',
        4 : 'May',
        5 : 'June',
        6 : 'July',
        7 : 'August',
        8 : 'September',
        9 : 'October',
        10 : 'November',
        11 : 'December'
    }

    day_to_name = {
        0 : 'Monday',
        1 : 'Tuesday',
        2 : 'Wednesday',
        3 : 'Thursday',
        4 : 'Friday',
        5 : 'Saturday',
        6 : 'Sunday',
    }
    
       
    date = datetime.datetime.fromtimestamp(first_order_time)
    line1 = f"Since your first order on {date.date()}, you've ordered {num_orders} times, spent ₹{total_spend:.2f} at an average of ₹{average_spend:.2f} per order"
    st.subheader(line1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Top Dish", max(dishes_split.items(), key = operator.itemgetter(1))[0])
    col2.metric("Top Restaurant", str(restaurant_split.index[0]))
    col3.metric("Top Category", max(category_split.items(), key = operator.itemgetter(1))[0])

    st.subheader("Top Restaurants: ")
    st.table(restaurant_split[:10])
    st.subheader("Top Categories: ")
    st.table(pd.DataFrame(category_split_s, index=[0]).transpose()[:10])
    st.subheader("Top Dishes: ")
    st.table(pd.DataFrame(dishes_split_s, index=[0]).transpose()[:10])

    max_mo_index = month_split.index(max(month_split))
    Keymax = max(zip(year_split.values(), year_split.keys()))[1]
    max_day_index = day_of_week_split.index(max(day_of_week_split))

    line2 = f"Your most prolific year was {Keymax}, month was {month_to_name[max_mo_index]} and day was {day_to_name[max_day_index]}. The city you ordered most in was: {top_city}, but you'd have known that already!"
    st.subheader(line2)
    
    st.subheader("Top Cities")
    st.table(city_split[:10])

    max_hr_index = hour_split.index(max(hour_split))

    line3 = f"You ordered the most between {time_to_start_end[max_hr_index][0]} and {time_to_start_end[max_hr_index][1]}: {hour_split[max_hr_index]} times"
    st.subheader(line3)

    #TODO: Show all timewise data here

    line4 = f"You spent {math.ceil(waiting/3600)} hours waiting for your orders, that's an average of {waiting_per_order:.2f} minutes per order"
    st.subheader(line4)

    line5 = f"You ordered from restaurants that were, on an average, {average_distance:.2f} KM away. That means, Swiggy delivery men travelled {total_distance:.2f} KM just to deliver your orders. Another reason to tip them well!"
    st.subheader(line5)

    line6 = f"Here's a map of all the places you ordered from! (In case of multiple geographies, please zoom in using your mouse)"
    st.subheader(line6)
    #Show map here!
    mapdf = pd.DataFrame(
        latlon, columns = ['lat', 'lon']
    )
    st.map(mapdf)

payment_button_url = r'<form><script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_Ihe4fKr1AVERm8" async> </script></form>'

components.html(payment_button_url, height = 1000)

st.caption('Developed by @thesidjway and @shashwatg1 in 12 hrs as a part of the half-day build hackathon, organized by @louispereira')
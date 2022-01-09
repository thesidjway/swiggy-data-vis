import streamlit as st
import pandas as pd
import numpy as np
import webbrowser
import requests
import js2py
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Example App", page_icon="🤖")
st.title("Get Data from Swiggy")
session = requests.Session()
    
if st.button('Open Swiggy'):

    driver = webdriver.Chrome(ChromeDriverManager().install())

    url = 'https://www.swiggy.com/restaurants'
    driver.get(url)
    # Open a new window
    driver.execute_script("window.open('');")
    # Switch to the new window and open new URL
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)

"""

    js = """
"""
    order_array=[]
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
        console.log(order_array)
    }
    """
"""
    result = js2py.eval_js(js)  # executing JavaScript and converting the result to python string 
    print (result)
"""




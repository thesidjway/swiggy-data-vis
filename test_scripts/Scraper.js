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
    const a = document.createElement("a");
    const file = new Blob([JSON.stringify(order_array)], { type: "text/plain" });
    a.href = URL.createObjectURL(file);
    a.download = "orders.json";
    a.click();
    console.log(order_array)
}
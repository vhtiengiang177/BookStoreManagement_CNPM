function addToCart(id, name, price, discount, quantity){
    fetch('/api/cart' , {
        'method': 'post',
        'body': JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
            'discount': discount,
            'quantity': quantity
    }),
    'headers':{
        'Content-Type':'application/json'
        }
    }  ).then(res=>res.json())
    .then(data=>{
        alert(data.message);
    })
}

function pay(){
    var name_receiver = document.getElementById("name_receiver").value;
    var phone_number_receiver = document.getElementById("phone_number_receiver").value;
    var address_receiver = document.getElementById("address_receiver").value;
    var discount_receiver = document.getElementById("discount_receiver").value;
    fetch('/api/pay' , {
        'method': 'post',
        'body': JSON.stringify({
            'name_receiver': name_receiver,
            'phone_number_receiver': phone_number_receiver,
            'address_receiver': address_receiver,
            'discount_receiver' : discount_receiver
    }),
    'headers':{
        'Content-Type':'application/json'
        }
    }  ).then(res=>res.json())
    .then(data=>{
        alert(data.message);
//        location.reload();
        window.location.href = "http://example.com/new_url";
    })
}




function check_would_buy(id) {
  var checkBox = document.getElementById(id);
  fetch('/api/check_would_buy' , {
        'method': 'post',
        'body': JSON.stringify({
            'id': id,
            'checked': checkBox.checked,
    }),
        'headers':{
        'Content-Type':'application/json'
        }
    }  ).then(res=>res.json())
    .then(data=>{
        alert(data.message);
    })
}

function del_item(item_id){
    if(confirm("Bạn có chắc chắn muốn xóa khỏi giỏ hàng?") == true){
        fetch(`/api/delete/${item_id}`,{
        'method': 'delete',
        'headers':{
            'Content-Type':'application/json'
        }
    }  ).then(res=>res.json())
    .then(data=>{
        alert(data.message);
        location.reload();
    }).catch(err=> alert('Xóa thất bại'))
}
}

function update_item(obj, item_id){
fetch(`/api/cart/${item_id}` , {
        'method': 'post',
        'body': JSON.stringify({
            'quantity': obj.value
    }),
    'headers':{
        'Content-Type':'application/json'
        }
    }  ).then(res=>res.json())
    .then(data=>{
        if(data.code !=200)
            alert("That bai")
        else{
            alert("Thanh cong")
            document.getElementById('total_quantity').innerText = data.total_quantity;
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
}


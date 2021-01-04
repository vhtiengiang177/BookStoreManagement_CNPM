function addToCart(id, name, price, quantity){
    fetch('/api/cart' , {
        'method': 'post',
        'body': JSON.stringify({
            'id': id,
            'name': name,
            'price': price,
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

function pay(id_user, cart){
    fetch('/api/pay' , {
        'method': 'post',
        'body': JSON.stringify({
            'id_user': id_user,
            'cart': cart
    }),
    'headers':{
        'Content-Type':'application/json'
        }
    }  ).then(res=>res.json())
    .then(data=>{
        alert(data.message);
        location.reload();
    })
}
<<<<<<< HEAD
=======



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
>>>>>>> 02f2f2bd9b1d7cf61f23da6da2e82d83e2eba527

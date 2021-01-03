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
        alert(checkBox.checked);
    })
}

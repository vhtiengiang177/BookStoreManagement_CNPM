function addToCart(id, name, price){
    fetch('/api/cart' , {
        'method': 'post',
        'body': JSON.stringify({
            'id': id,
            'name': name,
            'price': price
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

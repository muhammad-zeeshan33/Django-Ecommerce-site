
var updateBtns =document.getElementsByClassName('update-cart')
for (var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){        
        productId = this.dataset.product
        action = this.dataset.action               
        console.log('Product:', productId, 'action:' , action)
        console.log('USER:', user)
        if (user === 'AnonymousUser'){
            console.log('User is not logged in')
        }else{            
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action, url){    
    var url= 'http://127.0.0.1:8000/store/update_item';

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}
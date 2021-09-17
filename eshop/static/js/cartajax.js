var updateBtns = document.getElementsByClassName('update-cart')
for(i=0; i<updateBtns.length; i++){
    $(document).on('click', updateBtns[i], function(){
        productId=this.dataset.product;
        action = this.dataset.action;
        $.ajax({
            type: 'POST',
            url: '/store/update_item',
            data:{
                productId: productId,
                action: action,                
            },
            success:function(){
                
            }

        })
    })
}
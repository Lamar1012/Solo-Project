
function changeimage(){
    var img = document.getElementById('dynamic1');
    img.src = 'static/img/13.png';
}


function out(){
    var img = document.getElementById('dynamic1');
    img.src = 'static/img/1.png';
}

function changeimage2(){
    var img = document.getElementById('dynamic2');
    img.src = 'static/img/11.png';
}

function out2(){
    var img = document.getElementById('dynamic2');
    img.src = 'static/img/towel.png';
}

function changeimage3(){
    var img = document.getElementById('dynamic3');
    img.src = 'static/img/12.png';
}

function out3(){
    var img = document.getElementById('dynamic3');
    img.src = 'static/img/black_guy.png';
}

function changeimage4(){
    var img = document.getElementById('dynamic4');
    img.src = 'static/img/14.png';
}

function out4(){
    var img = document.getElementById('dynamic4');
    img.src = 'static/img/face_mask.png';
}

function changeimage5(){
    var img = document.getElementById('dynamic5');
    img.src = 'static/img/10.png';
}

function out5(){
var img = document.getElementById('dynamic5');
    img.src = 'static/img/headband.png';
}

function delete_product(id, e){
    console.log(id);
    console.log("Its mE");
    document.getElementById(id).remove()
    fetch(`http://127.0.0.1:5000/products/delete/${e}`)
        .then( response => response.json())
        .catch(data => console.log(data))
                    

}

function addToCart(){
    $.ajax({
        url:"/add_to_cart",
        type:'POST',
        success: function(response) {
            $('#cart-count').text(response.cart_count);
        },
        error: function(){
            console.log('Error occured while adding to cart.');
        }
        
    })
}

function cartCounter(event, id){
    event.preventDefault()
    console.log("Here");
    console.log(event)
    console.log(id)
    // console.log(id);
    var cart_form = document.getElementById(id);
    console.log('cart_form', cart_form);
    //                     cart_form.onsubmit = function(e){

                            // e.preventDefault();

                            var form = new FormData(cart_form);
                            console.log('my new form',form);
                            var cart = document.getElementById('cart-count')
                            var before = parseInt(cart.innerText)
                            var qt =  parseInt(form.get('quantity'))
                            cart.innerText = before + qt
                            fetch("http://127.0.0.1:5000/add_to_cart", {method:'POST', body: form})
                            .then( response => response.json())
                            .then(data => console.log(data))
                        }
    // $(document).ready(function() {
    //     $('#add_to_cart_button').click(function() {
    //         document.getElementById('cart-count').innerText ++
    //         $.ajax({
    //             type: 'POST',
    //             url: '/add_to_cart',
    //             success: function(response) {
    //             $('#cart-count').text(response.count);
                

    //         }
            
    //         });
            
    //     });
    // });

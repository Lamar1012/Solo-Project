from flask_app import app, bcrypt
from flask import render_template, redirect, session,request, jsonify
from flask_app.models import user, product

@app.route("/new/product")
def new_product():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id":session["user_id"]
    }
    users = user.User.get_by_id(data)
    if users.is_admin != 1:
        return redirect("/")
    return render_template("create_product.html", user = users)

@app.route("/create/product", methods = ["POST"])
def create_product():
    if "user_id" not in session:
        return redirect("/")
    
    if not product.Product.products_validation(request.form):
        return redirect("/new/product")
    
    data = {
        "price":request.form["price"],
        "product_name":request.form["product_name"],
        "product_image":request.form["product_image"],
        "user_id":session["user_id"]
    }

    product.Product.create_product(data)
    return redirect("/products")

@app.route("/products")
def products_page():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }

    users = user.User.get_by_id(data)
    if "cart_count" not in session:        
        session["cart_count"] = 0


    return render_template("products_page.html", users = users, all_products = product.Product.get_all_products(), count_items = session['cart_count'])

@app.route("/add_to_cart", methods = ["POST"]) #add to cart button
def add_to_cart():
    product_id = request.form["product_id"]
    print("In add to cart route")
    print(product_id)
    quantity = int(request.form["quantity"])
    count = session.get('cart_count', 0)
    count += quantity
    session['cart_count'] = count
    

    # get_product_by_id = product.Product.get_by_id(product_id)

    data = {
        "id": product_id
    }

    get_product_id = product.Product.get_product_id_for_cart(data)

    total_price =  get_product_id.price * quantity

    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append({
        "product_id":product_id,
        "product_name": get_product_id.product_name,
        "quantity": quantity,
        "total_price": total_price
    })

    session['cart'] = [i for i in session["cart"]]
    
    # return redirect("/products")
    response = {'count': count}
    return jsonify(response)

@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    users = user.User.get_by_id(data)
    if 'cart' not in session:
        session['cart'] = []
    total_sum = sum(products['total_price'] for products in session['cart'])

    return render_template("cart.html", cart=session['cart'], total_sum = total_sum, users=users)

@app.route("/delete/cart/<string:id>")
def delete_product_from_cart(id):
    if 'user_id' not in session:
        return redirect("/")
    temp = []
    for i in session["cart"]:
        if i["product_id"] != id:
            print(i)
            temp.append(i)
    session["cart"] = temp
    session["cart_count"] -= 1
    return redirect("/cart")

@app.route("/order_summary")
def placed_order():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    users = user.User.get_by_id(data)
    if 'cart' not in session:
        session['cart'] = []
    total_sum = sum(products['total_price'] for products in session['cart'])
    cart = session['cart']

    session['cart'] = []
    session['cart_count'] = 0

    return render_template("order_summary.html", cart=cart, total_sum=total_sum, users=users)

@app.route("/products/edit/<int:id>")
def edit_products(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id":id
    }

    one_product = product.Product.get_by_id(data)
    
    users = users = user.User.get_by_id({"id":session['user_id']})
    if users.is_admin != 1:
        return redirect("/")

    return render_template("edit_product.html", one_product=one_product)
@app.route("/products/update/<int:id>", methods = ["POST"])
def update_product(id):
    if "user_id" not in session:
        return redirect("/")
    if not product.Product.products_validation(request.form):
        return redirect(f"/products/edit/{request.form['id']}")
    data = {
        "id":id,
        "price":request.form["price"],
        "product_name":request.form["product_name"],
        "product_image":request.form["product_image"]
    }

    product.Product.update_product(data)
    return redirect("/products")

@app.route("/products/delete/<int:id>")
def delete_product(id):
    if 'user_id' not in session:
        return redirect("/")
    product.Product.delete_product({"id":id})
    return redirect("/products")


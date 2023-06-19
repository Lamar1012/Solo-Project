from flask_app import app, bcrypt
from flask import render_template, redirect, session,request, flash
from flask_app.models import user,product

@app.route("/")
def index():
    return redirect("/RoyalTskincare")

@app.route("/RoyalTskincare")
def home_page():
    return render_template("homepage.html", users = user.User.get_all_users())

@app.route("/register", methods = ["POST"])
def register():

    if not user.User.is_valid_reg(request.form):
        return redirect("/")

    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "is_admin":int(request.form["is_admin"]),
        "password": bcrypt.generate_password_hash(request.form["password"])
    }

    session["user_id"] = user.User.create(data)
    
    return redirect("/RoyalTskincare/user/dashboard")

@app.route("/login", methods = ["POST"])
def login():
    data = {
        "email":request.form["email"]
    }

    user_from_db = user.User.get_by_email(data)
    if not user_from_db:
        flash("Invalid Login", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_from_db.password, request.form["password"]):
        flash("invalid Login", "login")
        return redirect("/")
    session["user_id"] = user_from_db.id
    if user_from_db.is_admin != 1:
        return redirect("/RoyalTskincare/user/dashboard")
    else:
        return redirect("/RoyalTskincare/admin/dashboard")

@app.route("/RoyalTskincare/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    users = user.User.get_by_id(data)
    if users.is_admin != 1:
        return redirect("/")
    
    return render_template("admin_dashboard.html", users = users)

@app.route("/RoyalTskincare/user/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    users = user.User.get_by_id(data)
    return render_template("dashboard.html", users=users)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

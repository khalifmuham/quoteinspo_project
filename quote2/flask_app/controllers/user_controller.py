from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.quote_model import Quote
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("login_register.html")

@app.route("/register", methods = ["POST"])
def register():
    if User.validate_registration(request.form) == False:
        return redirect("/")
    else:
        if User.get_user_email({"email": request.form["email"]}) == None:
            data = {
                "first_name": request.form["first_name"],
                "last_name": request.form["last_name"],
                "email": request.form["email"],
                "password": bcrypt.generate_password_hash(request.form["password"])
            }
            user_id = User.register_user(data)
            session["first_name"] = request.form["first_name"]
            session["last_name"] = request.form["last_name"]
            session["email"] = request.form["email"]
            session["user_id"] = user_id
            return redirect("/dashboard")
        else:
            flash("This email is already in use" , "error_email")
            return redirect("/")

@app.route('/login',methods=['POST']) #decorator
def login():
    if User.validate_login(request.form) == False:
        return redirect("/")
    else:
        data = {
            "email": request.form['email']
        }
        result = User.get_user_email(data)
        if result == None:
            flash("Invalid login","login_error")
            return redirect("/")
        else:
            if not bcrypt.check_password_hash(result.password, request.form["password"]):
                flash("Invalid login","login_error")
                return redirect("/")
            else:
                session["first_name"] = result.first_name
                session["last_name"] = result.last_name
                session["email"] = result.email
                session["user_id"] = result.id
                return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if User.validate_session():
        quotes = Quote.get_all_quote_with_user()
        return render_template("dashboard.html", quotes = quotes)
    else:
        return redirect('/')

#Logout session
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


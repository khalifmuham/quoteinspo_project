from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.quote_model import Quote
from flask_app.models.user_model import User

#Routes for creating one quote
@app.route("/new/quote")
def display_quote():
    if User.validate_session == False:
        return redirect("/")
    else:
        return render_template("create_quote.html")

@app.route("/display/quote", methods = ['POST'])
def create_quote():
    data = {
            "author": request.form["author"],
            "description": request.form["description"],
            "created_at": request.form["created_at"],
            "user_id": session["user_id"]
    }
    Quote.create(data)
    return redirect("/dashboard")

@app.route("/view/quote/<int:id>")
def show_one_quote(id):
    if User.validate_session():
        data = {
            "id": id
        }
        quote = Quote.show_one(data)
        return render_template("view_one_quote.html", quote = quote)
    else: 
        return redirect('/')

@app.route("/edit/quote/<int:id>")
def view_edit_quote(id):
    if User.validate_session():
        data = {
            "id":id
        }
        quote = Quote.view_one(data)
        return render_template("edit_quote.html", quote = quote)
    else: 
        return redirect('/')

@app.route("/edit/quote/<int:id>", methods = ['POST'])
def create_edit_quote(id):
    data = {
        "author": request.form["author"],
        "description": request.form["description"],
        "created_at": request.form["created_at"],
        "user_id": session["user_id"],
        "id": id   
    }
    Quote.edit_quote(data)
    return redirect("/dashboard")


#DELETE a quote
@app.route("/delete/quote/<int:id>")
def delete_quote(id):
    if User.validate_session():        
        data = {
            "id": id
        }
        Quote.delete(data)
        return redirect("/dashboard")
    else: 
        return redirect('/')

from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,logout_user,current_user
from . import db

auth = Blueprint("auth",__name__)

@auth.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user:User = User.query.filter_by(email = email).first()
        
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully!",category = "success")
                login_user(user,remember = True )
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password! Try again",category = "error")
        else:
            flash("User does not exist!",category = "error")
    return render_template("login.html",user = current_user)

@auth.route("/sign-up",methods = ["GET","POST"])
def signUp():
    
    if request.method == "POST":
        email = request.form.get("email")
        firstName:str = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user:User = User.query.filter_by(email = email).first()
        
        if user:
            flash("User already exists.Please Login",category = "error")
        elif len(email) < 4:
            flash("Email needs to be greeater than 3 characters",category = "error")
        elif len(firstName) < 2:
            flash("Name must be longer than 1 character",category = "error")
        elif password1 != password2:
            flash("Passwords mismatch",category = "error")
        elif len(password1) < 7:
            flash("Password should be atleast 7 characters long",category = "error")
        else:
            #add user to Database
            newUser = User(email = email,firstName = firstName,password = generate_password_hash(password1,method = "pbkdf2:sha256"))
            db.session.add(newUser)
            db.session.commit()
            
            login_user(user,remember = True )
            
            flash("Account Created!",category = "success")
            return redirect(url_for("views.home"))
    
    return render_template("sign-up.html",user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
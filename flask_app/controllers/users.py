from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import song, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  # creating object 'bcrypt' - made by invoking the function Bcrypt with our app as an argument


#! index
@app.get("/")
def index():
    return redirect("/home")


#! home page
@app.get("/home")
def home_page():
    return render_template("index.html")


#! dashboard page
@app.get("/songs")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    
    one_user = user.User.get_by_id(session["user_id"])
    all_the_songs = song.Song.get_all_songs_with_user()
    return render_template("user_dashboard.html", user=one_user, all_the_songs=all_the_songs)


#! user log in
@app.post("/user/login")
def login_user():
    # validate
    if not user.User.validate_login(request.form):
        return redirect("/")
    
    user_in_db = user.User.get_by_email(request.form["email"])
    # password check if match
    pw_check = bcrypt.check_password_hash(user_in_db.password, request.form["password"])
    if not pw_check:
        flash("Invalid password.", "login")
        return redirect("/")
    # store user into session
    session["user_id"] = user_in_db.id
    return redirect("/songs")  #! login successful


#! user register
@app.post("/user/register")
def register_user():
    # validate
    if not user.User.validate_register(request.form):
        return redirect("/")
    
    # validate to see if email exists in database
    user_in_db = user.User.get_by_email(request.form["email"])
    if user_in_db:
        flash("Email already in use!", "register")
        return redirect("/")
    
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    # post info saved into 'data' dict
    data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash,  # hash upon registration
        }
    user_id = user.User.save(data)
    # store user into session
    session["user_id"] = user_id
    return redirect("/songs")  #! register successful


#! user log out
@app.get("/destroy")
def destroy():
    if "user_id" not in session:
        return redirect("/")
    session.clear()
    print("Session cleared")
    return redirect("/")
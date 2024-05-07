from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import song, user


#! new song page
@app.route("/songs/new")
def new_song():
    if "user_id" not in session:
        return redirect("/")
    
    one_user = user.User.get_by_id(session["user_id"])
    return render_template("new_song.html", user=one_user)


#! create song post
@app.route("/songs/create", methods=['POST'])
def create_song():
    if not song.Song.validate_song_info(request.form):
        return redirect("/songs/new")
    
    data = {
        "user_id": session["user_id"],
        "title": request.form["title"],
        "artist": request.form["artist"]
    }
    song.Song.save(data)
    return redirect("/dashboard")


#! view song page
@app.route("/songs/view/<int:song_id>")
def view_song(song_id):
    if "user_id" not in session:
        return redirect("/")

    one_user = user.User.get_user_with_song(song_id)
    return render_template("view_song.html", user=one_user)


#! edit song page
@app.route("/songs/edit/<int:song_id>")
def edit_song(song_id):
    if "user_id" not in session:
        return redirect("/")
    
    one_user = user.User.get_user_with_song(song_id)
    
    return render_template("edit_song.html", user=one_user)


#! update song post
@app.route("/songs/update")
def update_song():     
    song_id = request.form["song_id"]
    if not song.Song.validate_song_info(request.form):
        return redirect(f"/songs/edit/{song_id}")
    
    song.Song.update(request.form)
    return redirect("/songs")


#! delete song by song_id
@app.route("/songs/delete/<int:song_id>")
def delete_song(song_id):
    if "user_id" not in session:
        return redirect("/")
    
    song.Song.destroy_by_song_id(song_id)
    return redirect("/songs")
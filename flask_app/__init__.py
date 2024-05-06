from flask import Flask, session
from flask_app.models import song, user

app = Flask(__name__)
app.secret_key = "This is my secret key."
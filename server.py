from flask_app import app
from flask_app.controllers import songs, users


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=7000)
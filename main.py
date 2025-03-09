import datetime

from flask import Flask, render_template, request, redirect, url_for
from firebase import firebase
import os
import uuid

app = Flask(__name__)
firebase = firebase.FirebaseApplication(os.environ.get('FIREBASE_DB_URL'), None)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "create" in request.form:
            game_id = str(uuid.uuid4())
            new_game = {"name": request.form["game_name"], "id": game_id}
            firebase.post("/games", new_game)
            return redirect(url_for("game", game_id=game_id))
    return render_template("index.html")


@app.route("/game/<game_id>")
def game(game_id):
    games = firebase.get('/games', None)
    for game in games.values():
        if game['id'] == game_id:
            return render_template("game.html", game=game)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
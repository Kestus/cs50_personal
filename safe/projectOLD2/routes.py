from flask import flash, redirect, render_template, request, url_for
import json

from project import app, db
from project.helpers import valid, counter
from project.database import getPlaylist
from project.errors import _Flash



@app.route("/")
def index():
    
    return redirect(url_for("latest"))


@app.route("/playlist/<spotify_id>")
def renderPlaylist(spotify_id):

    playlist = db.execute("SELECT tracks FROM playlists WHERE spotify_id = ?", spotify_id)

    if not playlist:
        return redirect(url_for("index"))

    tracks = playlist[0]["tracks"]
    tracks = json.loads(tracks)
    length = len(tracks)

    try:
        videos = []
        for track in tracks:
            video = db.execute("SELECT * FROM videos WHERE video_id like ?", track)[0]
            videos.append(video)
        return render_template("playlist.html", tracks=tracks, length=length, videos=videos, count=counter())
    except IndexError:
        return render_template("playlist.html", tracks=tracks, length=length, count=counter())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        url = request.form.get("spotify_url")

        # if url is empty return error
        if not url:
            return render_template("add.html", count=counter(), error="Enter URL!")
        # if it doesen't look like spotify album or playlust url, return error
        if not valid(url):
            return render_template("add.html", count=counter(), error="Invalid URL!")
            

        # getPlaylist adds playlist to db if it doesen't exists there yet
        # returns spotify ID of playlist
        spotify_id = getPlaylist(url)

        # redirect to playlist
        return redirect(url_for("renderPlaylist", spotify_id=spotify_id))

    else:
        return render_template("add.html", count=counter())


@app.route("/latest")
def latest():

    playlists = db.execute("SELECT * FROM playlists ORDER BY timestamp DESC LIMIT 50")

    return render_template("latest.html", playlists=playlists, count=counter())


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search = request.form.get("search")
        search = f"%{search}%"

        if not search:
            return render_template("search.html", count=counter())

        results = db.execute("SELECT * FROM playlists WHERE name LIKE ?", search)

        return render_template("search.html", results=results, count=counter())

    else:
        return render_template("search.html", GET=1, count=counter())


@app.route("/e")
def er():
    log("bla")
    return _Flash("Not Found", "/add")

from cs50 import SQL
import json

import spotify
import youtube

db = SQL("sqlite:///project.db")

# make spotify api request, then youtube search, then add result to db
def addPlaylist(url, spotify_id, update=False):
    # get name and artist of tracks in the playlist
    info = spotify.info(url)
    tracks = spotify.tracks(url)

    name = info["name"]
    img = info["images"][0]["url"]
    _type= info["type"]
    total = info["tracks"]["total"]

    if _type == "Playlist":
        if info["owner"]["display_name"] == "Spotify":
            temp = 1
    else:
        temp = 0

    # search youtube and get youtube video id's
    id_list = youtube.search(tracks)

    # add playlist to db
    if not id_list:
        return -1

    # convert list to a string
    id_string = json.dumps(id_list)

    # CREATE NEW
    if update == False:
        db.execute("""INSERT INTO playlists
                        (spotify_id, tracks, name, img, type, total, temp)
                      VALUES
                        (?, ?, ?, ?, ?, ?, ?)""",
                    spotify_id, id_string, name, img, _type, total, temp)

    # UPDATE
    else:
        db.execute("""UPDATE playlists
                      SET tracks = ?, name = ?, img = ?, total = ?, timestamp = CURRENT_TIMESTAMP
                      WHERE spotify_id = ?""",
                    id_string, name, img, total, spotify_id)

    return



# expects spotify url
# if id already in db, returns spotify id, else addPlaylist(), return spotify_id
def getPlaylist(url):
    # get ID for db table, to be able search it later
    spotify_id = spotify.getID(url)

    # search playlist with that spotify ID already exists in db
    data = db.execute("SELECT temp, total FROM playlists WHERE spotify_id = ?", spotify_id)

    # if it doesen't, make API calls and INSERT result to db
    if len(data) == 0:
        addPlaylist(url, spotify_id)
    elif data[0]["temp"] == True:
        addPlaylist(url, spotify_id, update=True)

    return spotify_id





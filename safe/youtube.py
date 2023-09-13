import requests
import json
import concurrent.futures

from project.helpers import resetKeys, strFormat
from project import db, app
from project.errors import _Flash, Error



def search(tracks):
    # declare url, headers and params for request
    url = "https://www.googleapis.com/youtube/v3/search"
    headers = {"Accept": "application/json"}
    params = {
            "q": "",
            "part": "snippet",
            "maxResults": 8,
            "topicId": "/m/04rlf",
            "type": "video",
            "videoEmbeddable": "true",
            "key": ""
    }

    # check if keys counters need a reset
    resetKeys()

    video_id_list = []

    # for each track in playlist make a search call
    for track in tracks:
        select = db.execute("SELECT key FROM keys WHERE count < 100 AND name = 'youtube' ORDER BY id LIMIT 1")

        if len(select) != 1:
            app.logger.error("Failed to select YouTube API key")
            return _Flash("Quita Limit reached. Try again later", "/add")

        API_KEY = select[0]["key"]

        artist = strFormat(track["artist"])
        name = strFormat(track["name"])
        album = strFormat(track["album"])

        # q param update
        params["q"] = f"{name} {artist}"
        params["key"] = {API_KEY}

        # make a search api request
        try:
            request = requests.get(url, headers=headers, params=params, timeout=10)
        except requests.exceptions.RequestException as e:
            app.logger.error(f"YouTube API: {e}")
            return Error("Youtube API Error")
        # increment key use counter
        db.execute("UPDATE keys SET count = count + 1 WHERE key = ?", API_KEY)

        # check status code and try request 3 more times
        # if status code in consecutive requests still != 200, return error
        if request.status_code != 200:
            app.logger.error(f"YouTube API:{request.status_code}:{request.text}")
            for i in range(3):
                select = db.execute("SELECT key FROM keys WHERE count < 100 AND name = 'youtube' ORDER BY id LIMIT 1")

                if len(select) != 1:
                    app.logger.error("Failed to select YouTube API key")
                    return _Flash("Quita Limit reached. Try again later", "/add")

                request = requests.get(url, headers=headers, params=params, timeout=10)
                db.execute("UPDATE keys SET count = count + 1 WHERE key = ?", API_KEY)

                if request.status_code == 200:
                    break
            if request.status_code != 200:
                app.logger.error(f"Consecutive youtube API:{request.status_code}:{request.text}")
                return Error("YouTube API Error")

        
        request = request.json()
        items = request["items"]

        # additional soft check for the right search result
        for item in items:
            title = strFormat(item["snippet"]["title"])
            channelTitle = strFormat(item["snippet"]["channelTitle"])
            description = strFormat(item["snippet"]["description"])

            if name.lower() not in f"{title} {description}".lower():
                # app.logger.info(f"NAME::  {name}:: {title} - {description}")
                if artist.lower() not in f"{title} {channelTitle} {description}".lower():
                    # app.logger.info(f"ARTIST::  {artist}:: {title} - {channelTitle} - {description}")
                    if album.lower() not in f"{title} {description}".lower():
                        # app.logger.info(f"ALBUM::  {album}:: {title} - {description}")
                        continue
            if "version" in title.lower() and "version" not in name.lower():
                continue


            video_id = item["id"]["videoId"]
            thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]

            video_id_list.append(video_id)

            # "OR IGNORE" will ignore ValueError on INSERT video_id duplicate
            db.execute("INSERT OR IGNORE INTO videos (video_id, title, thumbnail, name, artist) VALUES (?, ?, ?, ?, ?)", video_id, title, thumbnail, name, artist)

            break

    return video_id_list




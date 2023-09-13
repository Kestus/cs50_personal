import requests
import datetime

from project.helpers import resetKeys
from project import db



def search(tracks):
    # declare url, headers and params for request
    url = "https://www.googleapis.com/youtube/v3/search"
    headers = {"Accept": "application/json"}
    params = {
            "q": "",
            "part": "snippet",
            "maxResults": "5",
            "regionCode": "eu",
            "topicId": "music",
            "type": "video",
            "key": ""
    }

    video_id_list = []

    # check if keys counters need a reset
    resetKeys()

    # for each track in playlist make a search call
    for track in tracks:
        select = db.execute("SELECT key FROM keys WHERE count < 100 AND name = 'youtube' ORDER BY id LIMIT 1")

        if len(select) != 1:
            return 0

        API_KEY = select[0]["key"]

        artist = track["artist"]
        name = track["name"]

        # q param update
        params["q"] = f"{artist} {name}"
        params["key"] = {API_KEY}

        # make a search api request
        try:
            request = requests.get(url, headers=headers, params=params, timeout=10)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        # increment key use counter
        db.execute("UPDATE keys SET count = count + 1 WHERE key = ?", API_KEY)

        # check status code
        if not request.status_code == 200:
            raise request.status_code
        if not request:
            raise request.status_code

        request = request.json()

        items = request["items"]
        # additional soft check for the right search result
        for item in items:
            title = item["snippet"]["title"]

            if artist.lower() and name.lower() in title.lower():
                video_id = item["id"]["videoId"]
                thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]

                video_id_list.append(video_id)

                # "OR IGNORE" will ignore ValueError on INSERT video_id duplicate
                db.execute("INSERT OR IGNORE INTO videos (video_id, title, thumbnail) VALUES (?, ?, ?)", video_id, title, thumbnail)

                break

    return video_id_list




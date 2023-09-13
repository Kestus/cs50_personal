from cs50 import SQL
import json
import requests

from spotify import getToken
import helpers

db = SQL("sqlite:///project.db")

def asfd():
    token = getToken()

    # url_type = "playlists"
    # url_id = "37i9dQZF1E35MzuIDHW07H"


    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    playlists = db.execute("SELECT spotify_id, type FROM playlists WHERE name LIKE 'DISCO%' LIMIT 1")

    for playlist in playlists:
        url_id = playlist["spotify_id"]
        url_type = playlist["type"]

        url = f"https://api.spotify.com/v1/{url_type}s/{url_id}/tracks"

        request = requests.get(url, headers=headers)
        request = request.json()


        with open("dataSpot3.json", "w") as file:
                json.dump(request, file, indent=4)



    # with open("data.json", "r") as file:
    #     data = json.load(file)
    #     x = data["owner"]["display_name"]
    #     print(x)


    # for playlist in playlists:

    #     url_id = playlist["spotify_id"]
    #     url_type = playlist["type"]

    #     url = f"https://api.spotify.com/v1/{url_type}s/{url_id}"

    #     request = requests.get(url, headers=headers)
    #     request = request.json()


    #     name = request["name"]
    #     img = request["images"][0]["url"]
    #     total = request["tracks"]["total"]

    #     db.execute("UPDATE playlists SET img = ?, total = ? WHERE spotify_id = ?", img, total, url_id)


    # with open("data.json", "r") as file:
    #     data = json.load(file)
    # title = data["snippet"]["title"]
    # img = data["snippet"]["thumbnails"]["medium"]["url"]

    # print(title)
    # print(img)


def main():
    x = helpers.counter()

    print(type(x))


if __name__ == "__main__":
    main()
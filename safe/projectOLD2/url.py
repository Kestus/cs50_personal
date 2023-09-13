

# formats url for api request, playlist or album
def formatUrl(url):
    # is it album or playlist?
    if "album" in url:
        url_type = "albums"
    else:
        url_type = "playlists"

    # find start and end point of playlist/album ID
    id_start = url.find(url_type[:-1]) + len(url_type[:-1]) + 1

    if "?si=" in url:
        id_end = url.find("?si=")
        # set ID to separate variable
        url_id = url[id_start:id_end]
    else:
        url_id = url[id_start:]

    # format url
    request_url = f"https://api.spotify.com/v1/{url_type}/{url_id}/tracks"

    return request_url
    
    
# parse url, extract spotify ID
def getID(url):
    # is it album or playlist?
    if "album" in url:
        url_type = "albums"
    else:
        url_type = "playlists"

    # find start and end point of playlist/album ID
    id_start = url.find(url_type[:-1]) + len(url_type[:-1]) + 1
    
    if "?si=" in url:
        id_end = url.find("?si=")
        # set ID to separate variable
        url_id = url[id_start:id_end]
    else:
        url_id = url[id_start:]

    # set ID to separate variable
    url_id = url[id_start:id_end]

    return url_id
    
    
def valid(url):
    if not "spotify.com" in url:
        return False
    if not "playlist" in url:
        if not "album" in url:
            return False
            
    return True
from cs50 import SQL
import datetime
from flask import render_template

db = SQL("sqlite:///project.db")

def expired(expires):
    # to check if token is expired
    # What time is now?
    now = datetime.datetime.now()

    # Convert expiration date from string to datetime format
    token_expiration_date = datetime.datetime.strptime(expires, "%Y-%m-%d %H:%M:%S")

    # If now > then expiration date, that means token is expired
    if now > token_expiration_date:
        return True
    else:
        return False

def valid(url):
    if not "spotify.com" in url:
        return False
    if not "playlist" in url:
        if not "album" in url:
            return False
    if not "?si=" in url:
        return False

    return True


def resetKeys():
    # key quota reset 00:00 PT, PT offset = 8, but set it to 9 to give time to google to reset
    # today, type = datetime in YYYY-MM-DD format
    offset = datetime.timedelta(hours=-9)
    today_str = datetime.datetime.now(datetime.timezone(offset, name="PT")).strftime("%Y-%m-%d")
    today = datetime.datetime.strptime(today_str, "%Y-%m-%d")

    # find tomorrow date and convert to str
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    # select date of reset from keys table and convert to datetime tipe, same format as today
    select_date = db.execute("SELECT next_reset_date FROM keys")
    reset_date_str = select_date[0]["next_reset_date"]
    reset_date = datetime.datetime.strptime(reset_date_str, "%Y-%m-%d")

    # if reset day has already passed
    # reset counter and update date of next reset
    if today >= reset_date:
        db.execute("UPDATE keys SET count = ?, next_reset_date = ?", 0, tomorrow_str)
        return
    else:
        return

def counter():
    resetKeys()
    # select SUM of all the key couters
    select = db.execute("SELECT SUM(count) FROM keys")

    # convert dict to dict_values to list, firs item in the list is integer SUM of counters
    summ = list(select[0].values())[0]

    return summ
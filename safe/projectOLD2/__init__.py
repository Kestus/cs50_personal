from flask import Flask
from cs50 import SQL
import logging
import datetime


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "b28a71cefdc3d7b77d486d9c702195e1"


# logger config
now = datetime.datetime.now()
date = now.strftime("%d-%m-%Y")
time = now.strftime("%H:%M:%S")
handler = logging.FileHandler(f"logs/{date}.log")
handler.setFormatter(logging.Formatter(f"[{time}]:%(levelname)s: %(message)s"))
app.logger.addHandler(handler)


db = SQL("sqlite:///project.db")


from project import routes, errors

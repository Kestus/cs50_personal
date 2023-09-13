from flask import Flask, request

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "b28a71cefdc3d7b77d486d9c702195e1"






@app.route("/")
def index():

    return "No value for count provided"

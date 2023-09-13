import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import datetime
# datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    shares = db.execute("SELECT * FROM ownership WHERE user_id = ? ORDER BY symbol", session["user_id"])

    total = 0

    for count, share in enumerate(shares):

        symbol = share["symbol"]
        search = lookup(symbol)

        share["price"] = search["price"]
        share["name"] = search["name"]

        total_share = share["price"] * share["amount"]
        total = total + total_share

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = int(cash[0]["cash"])

    return render_template("index.html", shares=shares, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # get submitted values
        try:
            amount = int(request.form.get("shares"))
        except ValueError:
            return apology("Enter valid amount of shares", 400)

        symbol = request.form.get("symbol")
        operation = "BUY"

        # Check submitted values
        if not symbol:
            return apology("Symbol Required")
        if not amount:
            return apology("Enter amount of shares")

        # lookup submitted symbol's price
        quote = lookup(symbol)
        if not quote:
            return apology("Symbol not found")

        symbol = quote["symbol"]

        if amount < 1:
            return apology("You can only buy 1 or more shares")

        # Check how mutch cash the user has, and if its enough for the purchase
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_cash = user_cash[0]["cash"]

        price = quote["price"]
        value = (price * amount)

        if value > user_cash:
            return apology("Not enough Cash")

        user_cash = user_cash - value

        # withdraw cash from user
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, session["user_id"])

        # record transaction
        # history
        db.execute("INSERT INTO transactions (user_id, symbol, operation, price, amount) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, operation, price, amount)
        # ownership record
        rec = db.execute("SELECT * FROM ownership WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        # if ownership record with that user_id and symbol doesent exists, create it, if already exists update value
        if len(rec) == 0:
            db.execute("INSERT INTO ownership (user_id, symbol, amount) VALUES (?, ?, ?)", session["user_id"], symbol, amount)
        else:
            db.execute("UPDATE ownership SET amount = amount + ? WHERE user_id = ? AND symbol = ?",
                       amount, session["user_id"], symbol)

        flash("Purchase Successful!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    logs = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", session["user_id"])

    return render_template("history.html", logs=logs)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        items = lookup(symbol)
        if not items:
            return apology("Symbol not found", 400)

        return render_template("quoted.html", items=items)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # checl input
        if not request.form.get("username"):
            return apology("Must provide username", 400)
        if not request.form.get("password"):
            return apology("Must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("Must confirm password", 400)

        # Check username
        username = request.form.get("username")
        if len(username) <= 4:
            return apology("Username must be longer then 4 characters")

        existing_username = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(existing_username) != 0:
            return apology("User with that name already exists")

        # Check password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if len(password) <= 5:
            return apology("Password must be longer then 5 characters", 400)
        if password != confirmation:
            return apology("Passwords must match", 400)

        # check password strength
        if not strong_password(password):
            return apology("Password mist contain atleast 1 digit, symbol, lower and upper case characters")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Add user to database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)

        # remember user
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)
        user_id = user_id[0]["id"]
        session["user_id"] = user_id

        # Flash message and redirect to login form
        flash("Registration Successful!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # get submitted values
        try:
            amount = int(request.form.get("shares"))
        except ValueError:
            return apology("Enter valid amount of shares", 400)

        symbol = request.form.get("symbol")
        operation = "SELL"

        # get user ownership info from db
        user = db.execute("SELECT * FROM ownership WHERE user_id = ?", session["user_id"])
        # convert list of dicts to list of values
        user_symbols = [dictionary["symbol"] for dictionary in user]

        # Check request
        if symbol == "Symbol":
            return apology("Select an option from dropdown menu")
        if not symbol in user_symbols:
            return apology("Please select available option")
        if amount < 1:
            return apology("Can only sell 1 or more amount of shares")

        # get amount of shares user ownes of chosen symbol
        user_amount = db.execute("SELECT amount FROM ownership WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        user_amount = user_amount[0]["amount"]

        # Check if user owns enougn shares to sell
        if amount > user_amount:
            return apology("You dont own enougn shares")

        # get current price and value of transaction
        quote = lookup(symbol)
        price = quote["price"]

        # record transaction
        # history
        db.execute("INSERT INTO transactions (user_id, symbol, operation, price, amount) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, operation, price, amount)

        # ownership
        # select how mutch shares user ownes
        user_amount = db.execute("SELECT amount FROM ownership WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        user_amount = user_amount[0]["amount"]

        # calculate final amount of shares
        final_amount = user_amount - amount

        # if final amount of shares = 0, delete record of ownership
        if final_amount == 0:
            db.execute("DELETE FROM ownership WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        # else update amount owned
        else:
            db.execute("UPDATE ownership SET amount = amount - ? WHERE user_id = ? AND symbol = ?",
                       amount, session["user_id"], symbol)

        # update user data
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_cash = user_cash[0]["cash"]
        value = price * amount
        user_cash = user_cash + value

        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, session["user_id"])

        flash("Sale Successful!")
        return redirect("/")

    else:
        symbols = db.execute("SELECT symbol FROM ownership WHERE user_id = ? ORDER BY symbol", session["user_id"])

        return render_template("sell.html", symbols=symbols)


@app.route("/account")
@login_required
def account():
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    username = user[0]["username"]
    cash = user[0]["cash"]

    return render_template("account.html", username=username, cash=cash)


@app.route("/pw_change", methods=["GET", "POST"])
@login_required
def pw_change():
    if request.method == "POST":
        # check input
        if not request.form.get("old-password"):
            return apology("Enter Old Password", 400)
        if not request.form.get("password"):
            return apology("Must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("Must confirm password", 400)

        old_password = request.form.get("old-password")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check old password
        hash_old = generate_password_hash(old_password)
        user_password = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
        user_password = user_password[0]["hash"]

        if not check_password_hash(user_password, old_password):
            return apology("Incorrect old password")

        # check new password
        if len(password) <= 5:
            return apology("Password must be longer then 5 characters", 400)

        if password != confirmation:
            return apology("Passwords must match", 400)

        # Hash new password
        hashed_password = generate_password_hash(password)

        # update password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_password, session["user_id"])

        flash("Password Changed")
        return redirect("/account")
    else:
        return render_template("pw_change.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        if not request.form.get("cash"):
            return apology("Enter amount")

        cash = int(request.form.get("cash"))

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", cash, session["user_id"])

        flash("Cash Added")
        return redirect("/account")
    else:
        return render_template("add_cash.html")


def strong_password(string):
    """Check password strengh"""
    upper = 0
    lower = 0
    digit = 0
    symbol = 0

    for c in string:
        if c.isupper():
            upper += 1
        elif c.islower():
            lower += 1
        elif c.isdigit():
            digit += 1
        else:
            symbol += 1

    if upper > 0 and lower > 0 and digit > 0 and symbol > 0:
        return True
    else:
        return False


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

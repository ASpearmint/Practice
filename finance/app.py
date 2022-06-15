import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

price = []


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show symbol, shares, lookup(symbol), shares*price and users(cash) """
#need to look for symbol and type "buy"/"sell" and do math
#first method is find unique symbols, store in list, perform operation
#Find each symbol owned, store into list.
#LOOP through each symbol to find total SUM of shares
#Store into dictionary
#If 0 don't show
#LAST THING -> TO REMOVE STOCKS WITH 0 SHARES NEEDS TRIPLET TO STORE PRICES
    if not db.execute("SELECT * FROM transactions WHERE person_id=?", session["user_id"]):
        return apology("Make some purchases to see stocks!", 404)
    stock_list = db.execute("SELECT DISTINCT symbol FROM transactions WHERE person_id=?", session["user_id"])
    transactions = {}
    prices = {}
    for dictionary in stock_list:
        shares = (db.execute("SELECT SUM(shares) FROM transactions WHERE person_id=? AND symbol=? ", session["user_id"], dictionary["symbol"]))
        for diction in shares:
            shares = diction["SUM(shares)"]
        if shares == 0:
            continue
        transactions[dictionary["symbol"]] = shares
        prices[dictionary["symbol"]] = lookup(dictionary["symbol"])["price"]
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]
    return render_template("index.html", prices=prices, cash=cash, transactions=transactions.items())


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    """Makes sure form data is correct, then converts lookups output and form output to float and then updates and inserts into transactions"""
    if request.method == "POST":

        if not request.form.get("buy") and not request.form.get("shares"):
            return apology("Please give symbol and shares")
        symbol = request.form.get("buy")

        if not lookup(symbol):
            return apology("Please give valid symbol")
        price = lookup(symbol)["price"]
        cashola = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])

        for money in cashola:
            cash = float(money["cash"])
        shares = float(request.form.get("shares"))

        if cash - (price * shares) < 0:
            return apology('Dude you\'re poor, add some money')
        total = cash - (price * shares)
        db.execute("UPDATE users SET cash= ? WHERE id=?", total, session["user_id"])
        db.execute("INSERT INTO transactions (person_id, type, symbol, shares) VALUES (?,?,?,?)", session["user_id"], "buy", symbol, shares)
        return render_template("buy_again.html")

    else:
        return render_template("buy.html")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM transactions WHERE person_id=?", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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
        if request.form.get("symbol"):
            symbol = request.form.get("symbol")
            if lookup(symbol):
                i = 0
                if len(price) == 8:
                    price.pop(0)
                    price.insert(7, lookup(symbol))
                else:
                    price.append(lookup(symbol))
                return render_template("quoted.html", price=price)
            else:
                return apology("Ticker not found", 405)

        else:
            return apology("Ticker not found", 405)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))


        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, password)
        return render_template("success.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("sell") and not request.form.get("shares"):
            return apology("Please give symbol and shares")
        symbol = request.form.get("sell")

        if not lookup(symbol):
            return apology("Please give valid symbol")
        price = lookup(symbol)["price"]
        cashola = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])

        for money in cashola:
            cash = float(money["cash"])
        shares = -float(request.form.get("shares"))

        stock_list = db.execute("SELECT DISTINCT symbol FROM transactions WHERE person_id=?", session["user_id"])
        transactions = {}
        for dictionary in stock_list:
            shares_total = (db.execute("SELECT SUM(shares) FROM transactions WHERE person_id=? AND symbol=? ", session["user_id"], dictionary["symbol"]))
            for diction in shares_total:
                shares_total = diction["SUM(shares)"]
            transactions[dictionary["symbol"]] = shares_total

        if (shares_total+shares <= -1):
            return apology('You can\'t sell what you don\'t have')
        total = cash - (price * shares)
        db.execute("UPDATE users SET cash= ? WHERE id=?", total, session["user_id"])
        db.execute("INSERT or IGNORE INTO transactions (person_id, type, symbol, shares) VALUES (?,?,?,?)", session["user_id"], "sell", symbol, shares)

        return render_template("buy_again.html")

    else:
        return render_template("sell.html")



from flask import Flask, render_template, request, redirect
import sqlite3
import random

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        dob = request.form["dob"]
        username = request.form["username"]
        password = request.form["password"]

        account_number = str(
            random.randint(
                1000000000,
                9999999999
            )
        )

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO users
            (fullname,dob,username,password,account_number)
            VALUES (?,?,?,?,?)
            """,
            (
                fullname,
                dob,
                username,
                password,
                account_number
            )
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE username=? AND password=?
            """,
            (username, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            return render_template(
                "dashboard.html",
                user=user
            )

        return "Invalid Username or Password"

    return render_template("login.html")


# PROFILE
@app.route("/profile/<username>")
def profile(username):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cur.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


# TRANSACTIONS
@app.route("/transactions")
def transactions():

    transactions = [
        ("12-Jun-2026", "Credit", "₹25,000"),
        ("11-Jun-2026", "Debit", "₹1,500"),
        ("10-Jun-2026", "Debit", "₹700"),
        ("09-Jun-2026", "Credit", "₹50,000")
    ]

    return render_template(
        "transactions.html",
        transactions=transactions
    )


# FRAUD DETECTION
@app.route("/fraud")
def fraud():

    fraud_data = [
        ("₹1,200 UPI Payment", "SAFE"),
        ("₹10,000 Transfer", "SAFE"),
        ("₹95,000 Transfer", "SUSPICIOUS"),
        ("₹1,50,000 Withdrawal", "HIGH RISK")
    ]

    return render_template(
        "fraud.html",
        fraud_data=fraud_data
    )


# LOGOUT
@app.route("/logout")
def logout():
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
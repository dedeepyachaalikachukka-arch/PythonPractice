from flask import Flask, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="bank"
)

cursor = db.cursor(buffered=True)

@app.route("/")
def login():
    return """
    <h2>Login Page</h2>
    <form action="/save" method="post">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Submit">
    </form>
    """

@app.route("/save", methods=["POST"])
def save():
    username = request.form["username"]
    password = request.form["password"]

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        return redirect("/menu/" + username)
    else:
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        old_user = cursor.fetchone()

        if old_user:
            return "Wrong password for this username"
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            return redirect("/menu/" + username)

@app.route("/menu/<username>")
def menu(username):
    return """
    <h2>Banking Application</h2>
    <a href="/deposit/""" + username + """">Make Deposit</a><br><br>
    <a href="/withdraw/""" + username + """">Withdraw</a><br><br>
    <a href="/view_deposits/""" + username + """">View Account Details</a><br><br>
    <a href="/">Logout</a>
    """

@app.route("/deposit/<username>")
def deposit(username):
    return """
    <h2>Deposit Page</h2>
    <form action="/save_deposit" method="post">
        <input type="hidden" name="username" value='""" + username + """'>
        Username: <input type="text" value='""" + username + """' readonly><br><br>
        Amount: <input type="number" name="amount"><br><br>
        <input type="submit" value="Deposit">
    </form>
    <br>
    <a href="/menu/""" + username + """">Back to Banking Menu</a><br><br>
    <a href="/">Logout</a>
    """

@app.route("/save_deposit", methods=["POST"])
def save_deposit():
    username = request.form["username"]
    amount = request.form["amount"]

    cursor.execute("INSERT INTO deposits (username, amount) VALUES (%s, %s)", (username, amount))
    db.commit()

    return """
    <h2>Deposited Successfully</h2>
    <a href="/menu/""" + username + """">Back to Banking Menu</a><br><br>
    <a href="/">Logout</a>
    """

@app.route("/withdraw/<username>")
def withdraw(username):
    return """
    <h2>Withdraw Page</h2>
    <form action="/save_withdraw" method="post">
        <input type="hidden" name="username" value='""" + username + """'>
        Username: <input type="text" value='""" + username + """' readonly><br><br>
        Amount: <input type="number" name="amount"><br><br>
        <input type="submit" value="Withdraw">
    </form>
    <br>
    <a href="/menu/""" + username + """">Back to Banking Menu</a><br><br>
    <a href="/">Logout</a>
    """

@app.route("/save_withdraw", methods=["POST"])
def save_withdraw():
    username = request.form["username"]
    amount = int(request.form["amount"])

    cursor.execute("SELECT amount FROM deposits WHERE username=%s", (username,))
    rows = cursor.fetchall()

    total_balance = 0
    for r in rows:
        total_balance = total_balance + int(r[0])

    if amount > total_balance:
        return """
        <h2>Insufficient Balance</h2>
        <a href="/menu/""" + username + """">Back to Banking Menu</a><br><br>
        <a href="/">Logout</a>
        """

    new_amount = -amount
    cursor.execute("INSERT INTO deposits (username, amount) VALUES (%s, %s)", (username, new_amount))
    db.commit()

    balance_after = total_balance - amount

    return """
    <h2>Withdraw Successful</h2>
    Withdrawn Amount: $""" + str(amount) + """<br><br>
    Total Balance: $""" + str(balance_after) + """<br><br>
    <a href="/menu/""" + username + """">Back to Banking Menu</a><br><br>
    <a href="/">Logout</a>
    """

@app.route("/view_deposits/<username>")
def view_deposits(username):
    cursor.execute("SELECT amount FROM deposits WHERE username=%s", (username,))
    rows = cursor.fetchall()

    output = "<h2>" + username + " Account Details</h2>"

    total_balance = 0

    if rows:
        for r in rows:
            output += "Amount: $" + str(r[0]) + "<br><br>"
            total_balance = total_balance + int(r[0])
    else:
        output += "No transactions found<br><br>"

    output += "<h3>Total Balance: $" + str(total_balance) + "</h3>"
    output += "<a href='/menu/" + username + "'>Back to Menu</a><br><br>"
    output += "<a href='/'>Logout</a>"

    return output

app.run(debug=True)
from flask import Flask, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="bank"
)

cursor = db.cursor()

@app.route("/")
def home():
    return """
    <h2>Banking Application</h2>
    <a href="/deposit">Make Deposit</a><br><br>
    <a href="/view_deposits">View Deposits</a>
    """

@app.route("/deposit")
def deposit_page():
    return """
    <h2>Deposit Page</h2>
    <form action="/save_deposit" method="post">
        Username: <input type="text" name="username"><br><br>
        Amount: <input type="number" name="amount" step="0.01"><br><br>
        <input type="submit" value="Deposit">
    </form>
    """

@app.route("/save_deposit", methods=["POST"])
def save_deposit():
    username = request.form["username"]
    amount = request.form["amount"]

    cursor.execute("INSERT INTO deposits (username, amount) VALUES (%s, %s)", (username, amount))
    db.commit()

    return """
    <h3>Deposit saved successfully!</h3>
    <a href="/">Go Home</a>
    """

@app.route("/view_deposits")
def view_deposits():
    cursor.execute("SELECT username, amount FROM deposits")
    data = cursor.fetchall()

    output = "<h2>All Deposits</h2>"

    for row in data:
        output += "Username: " + str(row[0]) + " | Amount: " + str(row[1]) + "<br><br>"

    output += "<a href='/'>Go Home</a>"

    return output

app.run()
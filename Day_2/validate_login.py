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

    cursor.execute("INSERT INTO users VALUES (%s,%s)", (username, password))
    db.commit()

    return "Data saved successfully"

app.run()

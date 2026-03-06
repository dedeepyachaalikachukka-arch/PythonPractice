import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "mysql123",
    database = "test"
)

cur = conn.cursor()

n = int(input("How many students do you want to enter? "))

for i in range(n):
    print("\nEnter details for student", i+1)
    
    id = int(input("Enter student ID: "))
    name = input("Enter student name: ")

    cur.execute(
        "INSERT INTO students (id, name) VALUES (%s, %s)",
        (id, name)
    )

conn.commit()

print("\nStudent added successfully!\n")

cur.execute("SELECT * FROM students")

for row in cur.fetchall():
    print(row)

cur.close()
conn.close()

import mysql.connector



table_name = "tasks"
connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="todolist"
)
cursor = connexion.cursor()

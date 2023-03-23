
import mysql.connector

with open('products.txt') as file:
    for line in file:
        code, name, qty, price = line.strip().split(",")

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            port=2222,
            password="example",
            database="mysql"
        )
        my_cursor = mydb.cursor()
        mysql_query = "INSERT INTO products (name,qty,productid,price) VALUES (%s,%s,%s,%s)"
        record = (name, qty, code, price)
        my_cursor.execute(mysql_query, record)
        mydb.commit()
    print("Record inserted successfully into Laptop table")

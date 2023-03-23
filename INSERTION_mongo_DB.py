import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = my_client["db"]
products = db["products"]

product = {}
with open('products.txt') as file:
    for line in file:
        code, name, qty, price = line.strip().split(",")
        customer_list = [
            {"code": code, "item": name, "qty_in_stocks": qty, "unit_price": price},
        ]
        products.insert_many(customer_list)
        if not line:
            break

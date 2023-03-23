import json
import logging
import socket
from datetime import datetime
import base64
import pika
import pymongo
import mysql.connector
import requests
from flask import Flask, render_template, request
from flask_restful import Resource, Api
import hprose

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


class GetStockIDs(Resource):
    def get(self):
        import json
        output_buffer = '{"products":['

        with open('products.txt') as file:
            for line in file:
                code, name, qty, price = line.strip().split(",")
                customer_list = {"code": code}
                output_buffer += json.dumps(customer_list) + ","
        output_buffer = output_buffer[:-1]
        output_buffer += ']}'

        print(output_buffer)
        f = open('calls.log', 'a')
        y = datetime.now()
        y = y.strftime("%d/%m/%Y %H:%M:%S")
        f.write(str(y) + '/stockIDs \n')
        f.close()

        return json.loads(output_buffer)


api.add_resource(GetStockIDs, '/getStockIDs')


class GetAllData(Resource):
    def get(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            port=2222,
            password="example",
            database="mysql"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT* FROM products;")
        output_buffer = '{"products":['
        for x in mycursor:
            customer_list = {"id": x[0], "code": x[3], "item": x[1], "qty_in_stocks": x[2], "unit_price": x[4]}
            output_buffer += json.dumps(customer_list) + ","
        output_buffer = output_buffer[:-1]
        output_buffer += ']}'
        f = open('calls.log', 'a')
        y = datetime.now()
        y = y.strftime("%d/%m/%Y %H:%M:%S")
        f.write(str(y) + '/all_data\n')
        f.close()
        return json.loads(output_buffer)


api.add_resource(GetAllData, '/getalldata')

if __name__ == '__main__':
    app.run(debug=True)


class GetStockNames(Resource):
    def get(self):

        output_buffer = '{"name": ['
        my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = my_client["db"]
        products = db["products"]
        for x in products.find():
            if "item" in x:
                output_buffer += '" ' + x['item'] + ' ",'
        output_buffer = output_buffer[:-1]
        output_buffer += ']}'
        f = open('calls.log', 'a')
        y = datetime.now()
        y = y.strftime("%d/%m/%Y %H:%M:%S")
        f.write(str(y) + '/stock_names \n')
        f.close()
        import json
        return json.loads(output_buffer)


api.add_resource(GetStockNames, '/getStockNames')


class Ping_server(Resource):
    def get(self):
        f = open('calls.log', 'a')
        y = datetime.now()
        y = y.strftime("%d/%m/%Y %H:%M:%S")
        client = hprose.HttpClient('http://127.0.0.1:8080/')
        f.write(str(y) + '/ping from ' + client.ping() + '\n')
        f.close()
        return client.ping()


api.add_resource(Ping_server, '/ping_server')


class PlaceOrder(Resource):
    def get(self):
        f = open('calls.log', 'a')
        y = datetime.now()
        y = y.strftime("%d/%m/%Y %H:%M:%S")
        f.write(str(y) + '/ order\n')
        f.close()

        content = request.args.get('param')

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='order')

        channel.basic_publish(exchange='', routing_key='order', body='order completed')
        print(" [x] Sent 'Hello World!'")
        connection.close()

        return json.loads(base64.b64decode(content))


api.add_resource(PlaceOrder, '/place_order')

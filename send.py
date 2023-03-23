import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='order')

channel.basic_publish(exchange='', routing_key='order', body='order completed')
print(" [x] Sent 'Hello World!'")
connection.close()

#!/usr/bin/env python
import pika
from flask import Flask, request, jsonify
from flask_cors import CORS
from OpenSSL import SSL
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
CERT_FILE = "/home/adam/my_virtualenvs/certkeys/server.crt"
KEY_FILE = "/home/adam/my_virtualenvs/certkeys/server.key"


app = Flask(__name__)
CORS(app)

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'task_queue'

@app.route('/spin', methods=['POST'])
def calculation():
    try:
        # Parse JSON data from request
        # data = request.json
        # message = data.get('message', 'Hello World!')

        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        # Declare queue
        # channel.queue_declare(queue=QUEUE_NAME, durable=True)

        # Publish message to queue
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body='message',
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

        # Close connection
        connection.close()

        # Return success response
        return jsonify({'message': 'Message published successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
     app.run(host='0.0.0.0',port=8080)
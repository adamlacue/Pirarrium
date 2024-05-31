import time
import pika
import RPi.GPIO as GPIO

# Set up GPIO pins
MOTOR_PIN = 17
DOOR_SENSOR_PIN = 16

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_PIN, GPIO.OUT)
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def spin():
    GPIO.output(MOTOR_PIN, GPIO.LOW) #Start motor
    time.sleep(10)
    try:
        while GPIO.input(DOOR_SENSOR_PIN) == GPIO.HIGH:
            time.sleep(0.1) #Check every .1 second if switch is open
    finally:
        GPIO.output(MOTOR_PIN, GPIO.HIGH) #Stop motor
    time.sleep(1)

def connect_to_rabbitmq():
    # RabbitMQ connection parameters
    credentials = pika.PlainCredentials('myuser', 'mypassword')
    parameters = pika.ConnectionParameters('100.125.45.107', 5672, '/', credentials)

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    return channel, connection

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    spin()
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consuming(channel):
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print(' [*] Waiting for spin commands. To exit press ctrl+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        setup_gpio()
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()

    # Connect to Rabbit and start consuming messages
    channel, connection = connect_to_rabbitmq()
    start_consuming(channel)
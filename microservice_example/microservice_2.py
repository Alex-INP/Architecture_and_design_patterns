import time
from socket import socket, AF_INET, SOCK_STREAM
import pika


def send_by_socket(target_adr, target_port, payload):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((target_adr, target_port))
	sock.send(f"{payload}".encode())
	sock.close()


def func_rabbit(chanel, method, props, body):
	print(f"Got message from mq: {body.decode()}")
	print("Sleep 10 sec started!")
	time.sleep(10)
	print("Sleep end")
	# default_gunicorn_port = 8081
	gunicorn_port = 8022
	send_by_socket(adr, gunicorn_port, f"{body.decode()} |microservice_2 job done|")


if __name__ == "__main__":
	adr = "127.0.0.1"
	broker_connection = pika.BlockingConnection(pika.ConnectionParameters(adr))
	channel = broker_connection.channel()
	channel.queue_declare(queue="test_queue")
	channel.basic_consume(queue="test_queue", auto_ack=True, on_message_callback=func_rabbit)
	print("Microservice 2 is waiting for messages.")
	channel.start_consuming()

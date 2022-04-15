from socket import socket, AF_INET, SOCK_STREAM
import pika


def receiver_socket():
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((adr, port))
	sock.listen(3)
	print(f"Microservice 1 server socket {adr}:{port} is listening.")
	while True:
		sender_socket, sender_address = sock.accept()
		print(f"Client Socket {sender_address} connected.")
		result = sender_socket.recv(1024)
		print(f"Got message! {result.decode()}")
		send_to_mq(f"{result.decode()} |microservice_1 job done|")


def send_to_mq(message):
	broker_connection = pika.BlockingConnection(pika.ConnectionParameters(adr))
	channel = broker_connection.channel()
	channel.queue_declare(queue="test_queue")
	message = message.encode()
	channel.basic_publish(exchange="", routing_key="test_queue", body=message)
	broker_connection.close()


if __name__ == "__main__":
	adr = "127.0.0.1"
	port = 8020
	receiver_socket()


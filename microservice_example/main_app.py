from socket import socket, AF_INET, SOCK_STREAM

def receiver_socket(main_adr, main_port):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((adr, port))
	sock.listen(3)
	print(f"Main APP server socket {main_adr}:{main_port} is listening.")
	while True:
		sender_socket, sender_address = sock.accept()
		print(f"Client Socket {sender_address} connected.")
		result = sender_socket.recv(1024)
		print(f"Result message: {result.decode()}")


def send_by_socket(target_adr, target_port, payload):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((target_adr, target_port))
	sock.send(f"{payload}".encode())
	sock.close()


if __name__ == "__main__":
	microservice_1_adr = "127.0.0.1"
	microservice_1_port = 8020
	for i in range(3):
		message = f"main_app initial message {i}"
		send_by_socket(microservice_1_adr, microservice_1_port, message)

	adr = "127.0.0.1"
	port = 8022
	receiver_socket(adr, port)


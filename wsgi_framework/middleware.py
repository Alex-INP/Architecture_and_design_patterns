def print_environ(environ):
	print("New request:")
	for key, val in environ.items():
		print(f"{key}: {val}")
	print()

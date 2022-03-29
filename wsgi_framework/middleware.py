def print_environ(environ):
	print("New request:")
	for key, val in environ.items():
		print(f"{key}: {val}")
	print()

def default_authentication(environ):
	environ["FRAMEWORK_DEFAULT_AUTH"] = True

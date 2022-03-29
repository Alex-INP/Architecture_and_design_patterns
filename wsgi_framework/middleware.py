def print_environ(environ):
	print("New request:")
	for key, val in environ.items():
		print(f"{key}: {val}")
	print()


def default_authorization(environ):
	environ["FRAMEWORK_DEFAULT_AUTH"] = True


def favicon_suppress(environ):
	if environ["PATH_INFO"] == "favicon.ico":
		environ["PATH_INFO"] = "/index"

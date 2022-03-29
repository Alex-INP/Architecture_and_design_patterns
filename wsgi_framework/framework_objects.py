import base64

class UserBuilder:
	def __init__(self, environ):
		self.environ = environ

	def get_user(self):
		if "HTTP_AUTHORISATION" in self.environ.keys():
			return User(**self.get_user_data())
		return User()

	def get_user_data(self):
		data_list = base64.b64decode(self.environ["HTTP_AUTHORISATION"]).decode().split(":")
		return {"username": data_list[0], "password": data_list[1]}


class User:
	def __init__(self, username="Guest", password=""):
		self.username = username
		self.is_auth = False
		self.password = password

	def auth(self):
		self.is_auth = True


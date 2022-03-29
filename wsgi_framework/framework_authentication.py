from abc import ABC, abstractmethod


class AbstractAuthenticator(ABC):
	@abstractmethod
	def authenticate(self):
		pass


class BasicAuthenticator(AbstractAuthenticator):
	def __init__(self, user, environ):
		self.user = user
		self.environ = environ

	def authenticate(self):
		# !!! Хардкод. Переделать с использованием орм.
		if self.user.username == "Alex" and self.user.password == "1":
			self.user.auth()
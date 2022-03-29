from abc import ABC, abstractmethod


class AbstractAuthorizator(ABC):
	@abstractmethod
	def authorize(self):
		pass


class BasicAuthorizator(AbstractAuthorizator):
	def __init__(self, user, environ):
		self.user = user
		self.environ = environ

	def authorize(self):
		# !!! Хардкод. Переделать с использованием орм.
		if self.user.username == "Alex" and self.user.password == "1":
			self.user.auth()
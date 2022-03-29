from wsgi_framework.framework_authentication import AbstractAuthenticator


class CustomAuthenticator(AbstractAuthenticator):
	def __init__(self, user, environ):
		self.user = user
		self.environ = environ

	def authenticate(self):
		print("My custom authenticator in action!")
		if 1 == 1:
			self.user.auth()
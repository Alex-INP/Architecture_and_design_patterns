from wsgi_framework.framework_authorization import AbstractAuthorizator


class CustomAuthorizator(AbstractAuthorizator):
	def __init__(self, user, environ):
		self.user = user
		self.environ = environ

	def authorize(self):
		# Create your authorization here
		pass
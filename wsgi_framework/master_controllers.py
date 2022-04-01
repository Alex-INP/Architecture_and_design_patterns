import inspect

from wsgi_framework.template_creator import render_template
from wsgi_framework.framework_logger import Logger
from wsgi_framework.exceptions import NotAuthenticatedError

LOG = Logger()

class BasicController:
	def __init__(self):
		self.template = ""
		self.context = {}
		self.method = ""
		self.data = {}
		self.user = None
		self.need_auth = False
		self.allow_cors = False
		self.allowed_cors_domains = []

	def pre_execute(self):
		pass

	def execute(self):
		self.pre_execute()
		for func_name, func in inspect.getmembers(self, inspect.ismethod):
			if func_name == self.method.lower() and func_name in ["get", "post", "update", "delete"]:
				if LOG.is_type_enabled("Info"):
					LOG["Info"](f"Method approved and about to execute: '{func_name}'.")

				if self.need_auth and not self.user.is_auth:
					raise NotAuthenticatedError
				elif self.need_auth and self.user.is_auth:
					LOG["Debug"](f"User {self.user.username} successfully authorized.")

				return func(self.data)

		if LOG.is_type_enabled("ERROR"):
			LOG["ERROR"](f"Method error: no method {self.method} defined for this controller.")

	def set_method(self, method):
		self.method = method

	def set_data(self, data):
		self.data = data

	def get(self, data):
		return render_template(self.template, **self.context)

	def post(self, data):
		return render_template(self.template, **self.context)




import inspect

from template_creator import render_template

class BasicController:
	def __init__(self):
		self.template = ""
		self.context = {}
		self.method = ""
		self.data = {}

	def execute(self):
		for func_name, func in inspect.getmembers(self, inspect.ismethod):
			if func_name == self.method.lower() and func_name in ["get", "post", "update", "delete"]:
				if self.data:
					return func(self.data)
				return func()
		print(f"Method error: no method {self.method} defined for this controller.")

	def set_method(self, method):
		self.method = method

	def set_data(self, data):
		self.data = data

	def get(self, data):
		return render_template(self.template, **self.context)




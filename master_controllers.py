import inspect

from template_creator import render_template

class BasicController:
	def __init__(self, method=""):
		self.template = ""
		self.context = {}
		self.method = method

	def execute(self):
		for func_name, func in inspect.getmembers(self, inspect.ismethod):
			if func_name == self.method.lower() and func_name in ["get", "post", "update", "delete"]:
				return func()
		print(f"Method error: no method {self.method} defined for this controller.")

	def get(self):
		return render_template(self.template, **self.context)




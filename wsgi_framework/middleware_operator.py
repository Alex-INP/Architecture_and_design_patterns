import importlib

from config import settings
from wsgi_framework.exceptions import NoMiddlewareFoundError

class MiddlewareOperator:
	def __init__(self, environ):
		self.middleware_list = []
		self.environ = environ

	def __call__(self):
		self.collect_middlewares()
		self.execute_middlewares()

	def collect_middlewares(self):
		for mid_full_path in settings.MIDDLEWARE:
			splitted_full_path = mid_full_path.split(".")
			mid_name, mid_path = splitted_full_path[-1], ".".join(splitted_full_path[:-1])
			try:
				imported_mid = importlib.import_module(mid_path)
				self.middleware_list.append(imported_mid.__dict__[mid_name])
			except ModuleNotFoundError:
				raise NoMiddlewareFoundError(mid_name, mid_path)
			except KeyError:
				raise NoMiddlewareFoundError(mid_name, mid_path)


		self.middleware_list = iter(reversed(self.middleware_list))

	def execute_middlewares(self):
		try:
			current_middleware = next(self.middleware_list)
			self.execute_middlewares()
			current_middleware(self.environ)
		except:
			return


from wsgi_framework.framework_logger import Logger

LOG = Logger()

class MainRouter:
	def __init__(self, inputed_urls):
		self.url_list = []
		self.url_pairs = []

		self.process_urls(inputed_urls)

	def process_urls(self, urls):
		for url in urls:
			self.register_route(url[0], url[1])

	def register_route(self, url, controller):
		self.url_list.append(url)
		self.url_pairs.append({"url": url, "controller": controller})

		if LOG.is_type_enabled("Debug"):
			LOG["Debug"](f"Controller '{controller.__name__}' registered in router on route {url}.")

	def is_exist(self, url):
		return True if url in self.url_list else False

	def get_controller(self, url):
		for pair in self.url_pairs:
			if pair["url"] == url:
				return pair["controller"]





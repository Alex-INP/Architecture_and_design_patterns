

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

	def is_exist(self, url):
		return True if url in self.url_list else False

	def get_controller(self, url):
		return self.url_pairs[url]





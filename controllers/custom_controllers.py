from master_controllers import BasicController


class IndexController(BasicController):
	def __init__(self):
		super().__init__()
		self.template = "index.html"
		self.context = {"names": ["Alex", "Bill", "Kate"]}


class AboutUsController(BasicController):
	def __init__(self):
		super().__init__()
		self.template = "about_templates/about_main.html"


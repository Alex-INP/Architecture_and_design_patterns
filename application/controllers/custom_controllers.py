from wsgi_framework.master_controllers import BasicController
from wsgi_framework.framework_logger import Logger

LOG = Logger()

class IndexController(BasicController):
	def __init__(self):
		super().__init__()
		self.template = "index.html"
		self.context = {"names": ["Alex", "Bill", "Kate"]}

		LOG["My_Logtype_1"](f"My own controller '{self.__class__.__name__}' ready to deal with {self.template}.")


class AboutUsController(BasicController):
	def __init__(self):
		super().__init__()
		self.template = "about_templates/about_main.html"


class ContactsController(BasicController):
	def __init__(self):
		super().__init__()
		self.template = "contacts.html"
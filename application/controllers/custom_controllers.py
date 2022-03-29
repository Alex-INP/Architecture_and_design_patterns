from wsgi_framework.master_controllers import BasicController
from wsgi_framework.framework_logger import Logger

LOG = Logger()

class IndexController(BasicController):
	def __init__(self):
		super().__init__()
		self.template = "index.html"
		self.context = {"names": ["Alex", "Bill", "Kate"]}
		self.need_auth = True

		if LOG.is_type_enabled("My_Logtype_1"):
			LOG["My_Logtype_1"](f"My own controller '{self.__class__.__name__}' ready to deal with {self.template}.")

	# def pre_execute(self):
	# 	if self.user.username == "Alex":
	# 		self.user.auth()


class AboutUsController(BasicController):
	def __init__(self):
		super().__init__()
		self.template = "about_templates/about_main.html"

	def post(self, data):
		return bytes(f"Your data: {data}", "utf-8")


class ContactsController(BasicController):
	def __init__(self):
		super().__init__()
		self.template = "contacts.html"

	def post(self, data):
		return bytes("My custom post function answer", "utf-8")
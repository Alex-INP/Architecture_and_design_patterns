from wsgi_framework.master_controllers import StandardController
from wsgi_framework.framework_logger import Logger
from application.models.custom_models import Good

LOG = Logger()

class IndexController(StandardController):
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


class AboutUsController(StandardController):
	def __init__(self):
		super().__init__()
		self.template = "about_templates/about_main.html"
		self.allow_cors = True
		self.allowed_cors_domains = ["http://127.0.0.1:8000"]

	def post(self, data):
		return bytes(f"Your data: {data}", "utf-8")


class ContactsController(StandardController):
	def __init__(self):
		super().__init__()
		self.template = "contacts.html"

	def post(self, data):
		# new_good = Good(name="Fridge", description="very good")
		# new_good.add_row()
		# new_good.update(price=200)
		# new_good = Good().filter(name="Fridge")[0]
		# new_good.delete()
		return bytes("My custom post function answer", "utf-8")
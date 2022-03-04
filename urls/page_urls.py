import sys
sys.path.append("..")

from controllers.custom_controllers import IndexController, AboutUsController, ContactsController


registered_urls = [
	["/index", IndexController],
	["/aboutus", AboutUsController],
	["/contacts", ContactsController],
]

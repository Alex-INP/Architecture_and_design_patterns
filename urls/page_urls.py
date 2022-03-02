import sys
sys.path.append("..")

from controllers.custom_controllers import IndexController, AboutUsController


registered_urls = [
	["/index", IndexController],
	["/aboutus", AboutUsController]
]

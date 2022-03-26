from wsgi_framework.framework_logger import Logger, LogType, LogColors
from config import settings


def setup_custom_logger():
	# Create your custom loggers here

	LOG = Logger()
	LOG.set_file_path(settings.APP_LOG_DIR_PATH)
	LOG.set_output_mode(settings.LOGGER_STDOUT)

	colors = LogColors()
	colors.add_color("my_color", "\033[96m")

	my_logtypes_list = [
		LogType("My_Logtype_1", colors.my_color),
		LogType("My_Logtype_2", colors.red),
		LogType("My_Logtype_3", colors.blue),
	]

	LOG.register_logtypes(my_logtypes_list, exclude=["Debug"])

	LOG.disable_logtype("My_Logtype_2")

	LOG["My_Logtype_1"]("My logger types are ready!")





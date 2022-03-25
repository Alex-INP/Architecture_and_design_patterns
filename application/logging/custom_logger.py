from wsgi_framework.framework_logger import Logger, LogType, LogColors
from application.engine import setup_logger

# Create your custom loggers here

LOG = Logger()
setup_logger(custom=True)

colors = LogColors()

colors.add_color("my_color", "\033[96m")


my_logtypes_list = [
	LogType("My_Logtype_1", colors.my_color),
	LogType("My_Logtype_2", colors.red),
	LogType("My_Logtype_3", colors.blue),
]

LOG.register_logtypes(my_logtypes_list, exclude=[])

LOG.disable_logtype("My_Logtype_2")


LOG["My_Logtype_1"]("My logger types are ready!")

print()
for i in LOG.log_types:
	print(i)





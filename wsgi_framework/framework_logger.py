from datetime import datetime

from wsgi_framework.exceptions import LogTypeNameDuplicationError, LogTypeNotRegisteredError, LoggerStdoutSettingError,\
	NoLogFileError, OutputModeError

class Logger:
	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Logger, cls).__new__(cls)
		return cls.instance

	def __init__(self):
		self.log_types = {}
		self.colors = LogColors()
		self.file_path = None
		self.output_mode = None

	def __getitem__(self, item):
		if item not in self.log_types.keys():
			raise LogTypeNotRegisteredError(item)
		return self.log_types[item]

	def set_output_mode(self, output_mode):
		self.output_mode = output_mode
		# print(self.output_mode)

	def set_file_path(self, file_path):
		self.file_path = file_path
		# print(self.file_path)

	def register_logtype(self, log_type):
		if log_type.name not in self.log_types.keys():
			if self.file_path is not None:
				log_type.set_file_path(self.file_path)
			# if self.output_mode is not None:
			# 	log_type.set_output_mode(self.output_mode)
			if self.output_mode is not None:
				log_type.set_output_mode(self.output_mode)
			else:
				raise OutputModeError
			self.log_types[log_type.name] = log_type
		else:
			raise LogTypeNameDuplicationError(log_type.name)

	def register_logtypes(self, types_list=None, exclude=None):
		self.log_types.clear()
		if types_list is None:
			types_list = []

		standard_types = [
			LogType("ERROR", self.colors.red),
			LogType("Info", self.colors.bright_white),
			LogType("Debug", self.colors.blue),
			LogType("CRITICAL", self.colors.red_background)
		]
		if exclude is not None:
			if exclude == "all":
				standard_types.clear()
			else:
				for name in exclude:
					standard_types = list(filter(lambda x: x.name != name, standard_types))
		types_list.extend(standard_types)

		for item in types_list:
			self.register_logtype(item)

	def is_type_enabled(self, logtype_name):
		return True if logtype_name in self.log_types.keys() else False

	def disable_logtype(self, log_type_name):
		del self.log_types[log_type_name]

class LogType:
	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.file_path = None
		self.output_mode = None

	def __call__(self, message):
		if self.output_mode.lower() == "file" or self.output_mode.lower() == "console":
			self.log_message_out(message, self.output_mode)
		elif self.output_mode.lower() == "both":
			self.log_message_out(message, "file")
			self.log_message_out(message, "console")
		else:
			raise LoggerStdoutSettingError(self.output_mode)

	def log_message_out(self, message, output_mode):
		tail = "\033[0m"
		result = f"{datetime.now()}"
		result = self.add_spaces(result, 35)
		if output_mode.lower() == "file":
			result += f"|{self.name}"
		else:
			result += f"|{self.color}{self.name}{tail}"
		result = self.add_spaces(result, 60)
		if output_mode.lower() == "file":
			result += f"|{message}"
		else:
			result += f"{' ' * len(self.color)}{' ' * len(tail)}|{message}"
		if output_mode.lower() == "file":
			try:
				with open(f"{self.file_path}-{datetime.today().strftime('%d-%m-%Y')}.txt", "a", encoding="utf-8") as file:
					file.write(f"{result}\n")
			except:
				raise NoLogFileError(self.file_path)
			return
		print(result)

	def set_file_path(self, path):
		self.file_path = path

	def set_output_mode(self, mode):
		self.output_mode = mode

	@staticmethod
	def add_spaces(subject, spaces):
		subj_len = len(subject)
		delta = spaces - subj_len
		return f"{subject}{' '*delta}"


class LogColors:
	def __new__(cls, file_path=None):
		if not hasattr(cls, 'instance'):
			cls.instance = super(LogColors, cls).__new__(cls)
		return cls.instance

	def __init__(self):
		self.bright_white = "\033[1m"
		self.red = "\033[91m"
		self.green = "\033[92m"
		self.yellow = "\033[93m"
		self.blue = "\033[94m"
		self.red_background = "\033[101m"

	def add_color(self, name, escape):
		self.__setattr__(name, escape)





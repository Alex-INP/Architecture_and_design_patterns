class WsgiFrameworkException(Exception):
	def __init__(self, message=None):
		super().__init__("Framework exception has occurred." if message is None else message)


# Settings exceptions
class NoSettingDefinedError(WsgiFrameworkException):
	def __init__(self, e: AttributeError):
		attr_name = self.get_attr_name(e.args[0])
		super().__init__(f"Mandatory settings parameter not defined: {attr_name}. Define it in 'settings.toml'.")

	@staticmethod
	def get_attr_name(e):
		return e.split(" ")[-1]


# Logger exceptions
class LogTypeNameDuplicationError(WsgiFrameworkException):
	def __init__(self, logtype_name):
		super().__init__(f"LogType name is not unique: '{logtype_name}'. Check your custom LogType names.")


class LogTypeNotRegisteredError(WsgiFrameworkException):
	def __init__(self, logtype_name):
		super().__init__(f"LogType '{logtype_name}' was not registered in Logger.")


class LoggerStdoutSettingError(WsgiFrameworkException):
	def __init__(self, mode_name):
		super().__init__(f"Incorrect LOGGER_STDOUT setting name: '{mode_name}'. It can be: 'file', 'console', 'both'.")


class NoLogFileError(WsgiFrameworkException):
	def __init__(self, file_path):
		super().__init__(f"LOGGER_STDOUT setting was set to 'file' or 'both', but no LOG_FILE or LOG_FILE_DIR setting specified or directory not exists: {file_path}")


class OutputModeError(WsgiFrameworkException):
	def __init__(self):
		super().__init__(f"Logger's output mode cannot be None.")

# Template exceptions
class TemplateException(WsgiFrameworkException):
	def __init__(self, template=None, message=None):
		super().__init__(f"Template exception has occurred while handling {template}." if message is None else message)


class NoParentTemplateError(TemplateException):
	def __init__(self, path):
		super().__init__(message=f"Not found. No parent template '{path}' found.")


class SectionTagNameDuplicationError(TemplateException):
	def __init__(self, section_name):
		super().__init__(message=f"Section name in template is not unique: '{section_name}'.")

import sys
sys.path.append("..")
import os
import platform

from wsgi_framework.main import MainEngine
from wsgi_framework.exceptions import NoSettingDefinedError
from wsgi_framework.framework_logger import Logger

from config import settings
from urls.page_urls import registered_urls


def setup_logger(custom=False):
	LOG = Logger()
	exclude = []
	output_mode = None
	log_file_path = None
	if not custom:
		try:
			exclude = settings.DEFAULT_LOGGER_EXCLUDE
		except:
			pass
	try:
		output_mode = settings.LOGGER_STDOUT
	except:
		pass
	try:
		log_file_path = os.path.join(
			os.path.join(os.getcwd(), settings.LOG_FILE_DIR),
			settings.LOG_FILE
		)
	except:
		pass
	LOG.set_output_mode(output_mode)
	LOG.set_file_path(log_file_path)
	LOG.register_logtypes(exclude=exclude)


def process_settings(settings):
	try:
		settings.TEMPLATES_DIR = os.path.join(os.getcwd(), settings.TEMPLATES_DIR)
		settings.registered_urls = registered_urls
		settings.DEBUG = True if settings.DEBUG.lower() == "true" else False
		settings.LOGGING = True if settings.LOGGING.lower() == "true" else False
	except AttributeError as e:
		raise NoSettingDefinedError(e)

	if settings.LOGGING:
		try:
			settings.DEFAULT_LOGGER = True if settings.DEFAULT_LOGGER.lower() == "true" else False
		except AttributeError as e:
			raise NoSettingDefinedError(e)

		if settings.DEFAULT_LOGGER:
			print("def")
			setup_logger()
		elif not settings.DEFAULT_LOGGER:
			print("not def")
			from application.logging import custom_logger


if __name__ == "__main__":
	process_settings(settings)

	if settings.DEBUG:
		if platform.system() == "Windows":
			print("\n\nWARNING!!! You are in Windows debug mode!\n")
			from windows_tester import environ_content, start_response

			for request in environ_content:
				print("-"*100)
				print(f"Processing request: {request}\n")
				result = MainEngine()(request, start_response)
				print(result)
				print("\nSuccessfully processed.")
				print("-" * 100)

			input("\nEND. Press any button.\n\n")
		else:
			engine = MainEngine()
	else:
		engine = MainEngine()




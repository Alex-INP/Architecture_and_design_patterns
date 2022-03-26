import sys
sys.path.append("..")
import os
import platform

from wsgi_framework.main import MainEngine
from wsgi_framework.exceptions import NoSettingDefinedError
from wsgi_framework.framework_logger import Logger

from config import settings
from urls.page_urls import registered_urls
from application.logging.custom_logger import setup_custom_logger


def setup_logger():
	LOG = Logger()
	exclude = []
	output_mode = None
	try:
		exclude = settings.DEFAULT_LOGGER_EXCLUDE
	except:
		pass
	try:
		output_mode = settings.LOGGER_STDOUT
	except:
		pass
	LOG.set_output_mode(output_mode)
	LOG.set_file_path(settings.APP_LOG_DIR_PATH)
	LOG.register_logtypes(exclude=exclude)


def process_settings():
	try:
		settings.APP_DIR_PATH = os.getcwd()
		settings.APP_LOGGER_DIR_PATH = os.path.join(settings.APP_DIR_PATH, "logging")
		settings.APP_LOG_DIR_PATH = os.path.join(
			os.path.join(settings.APP_DIR_PATH, settings.LOG_FILE_DIR),
			settings.LOG_FILE)
		settings.TEMPLATES_DIR = os.path.join(os.getcwd(), settings.TEMPLATES_DIR)

		settings.REGISTERED_URLS = registered_urls
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
			setup_logger()
		elif not settings.DEFAULT_LOGGER:
			setup_custom_logger()


process_settings()

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



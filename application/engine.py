import sys
sys.path.append("..")
import platform

from wsgi_framework.main import MainEngine
import variables
import urls


os_check = True

if os_check:
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




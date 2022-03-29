import os

from wsgi_framework.url_router import MainRouter

from config import settings
from wsgi_framework.framework_logger import Logger
from wsgi_framework.middleware_operator import MiddlewareOperator
from wsgi_framework.constants import CODE_200, CODE_500, CODE_401
from wsgi_framework.exceptions import NotAuthenticatedError


LOG = Logger()


def replace_hex(text):
    text = text.replace("+", " ")
    ind = 0
    for i in text:
        if i == "%":
            target = text[ind: ind + 3]
            text = text.replace(target, bytes.fromhex(target[1:]).decode(), 1)
            ind -= 1
            continue
        ind += 1
    return text


def extract_request_data(environ):
    result = {}

    data_length = environ.get("CONTENT_LENGTH")
    data_length = int(data_length) if data_length else 0
    data_bytes = environ["wsgi.input"].read(
        data_length) if data_length > 0 else b""

    data_decoded = data_bytes.decode()
    if data_decoded:
        data = data_decoded.split("&")
        for i in data:
            key, value = i.split("=")
            result[key] = replace_hex(value)
    return result

def load_default_template(path):
    with open(path, "rb") as file:
        return file.read()

class MainEngine:
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        try:
            MiddlewareOperator(environ)()

            router = MainRouter(settings.REGISTERED_URLS)
            url = environ["PATH_INFO"]
            method = environ["REQUEST_METHOD"]

            if LOG.is_type_enabled("Info"):
                LOG["Info"](f"Request registered on: {url}")

            if url[-1] == "/":
                url = url[:-1]

            if router.is_exist(url):
                controller = router.get_controller(url)()
                if LOG.is_type_enabled("Debug"):
                    LOG["Debug"](f"Controller '{controller.__class__.__name__}' extracted from router.")
            else:
                if LOG.is_type_enabled("ERROR"):
                    LOG["ERROR"](f"No route '{settings.SITE_ADR}:{settings.SITE_PORT}{url}' registered")
                return

            data = extract_request_data(environ)
            controller.set_data(data)
            controller.set_method(method)

            if LOG.is_type_enabled("Debug"):
                LOG["Debug"](f"Procedures finished. Controller '{controller.__class__.__name__}' ready.")
            try:
                result = [controller.execute()]
            except NotAuthenticatedError:
                LOG["ERROR"](f"Controller execution demands authorisation: {controller.__class__.__name__}.")
                raise
            except:
                LOG["ERROR"](f"Error while controller execution: {controller.__class__.__name__}.")
                raise
            start_response(CODE_200, [('Content-Type', 'text/html')])
            LOG["Info"]("Request successfully processed.")
            return result
        except NotAuthenticatedError:
            start_response(CODE_401, [("Content-Type", "text/html"),
                                      ("WWW-Authenticate", "Basic")])
            return []

        except Exception as e:
            LOG["CRITICAL"](e)
            if settings.DEBUG:
                raise

            framework_templates_dir = os.path.join(os.path.join(os.path.dirname(__file__), "framework_templates"))
            start_response(CODE_500, [('Content-Type', 'text/html')])
            return [load_default_template(os.path.join(framework_templates_dir, "internal_server_error.html"))]

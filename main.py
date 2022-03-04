from url_router import MainRouter
from urls.page_urls import *
import common.variables as vrb


def extract_request_data(environ):
    result = {}

    data_length = environ.get("CONTENT_LENGTH")
    data_length = int(data_length) if data_length else 0
    data_bytes = environ["wsgi.input"].read(data_length) if data_length > 0 else b""

    data_decoded = data_bytes.decode()
    if data_decoded:
        data = data_decoded.split("&")
        for i in data:
            key, value = i.split("=")
            result[key] = value
    return result


def application(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    """
    router = MainRouter(registered_urls)
    url = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]


    if url[-1] == "/":
        url = url[:-1]

    if router.is_exist(url):
        controller = router.get_controller(url)()
    else:
        print(f"No route '{vrb.SITE_ADR}:{vrb.SITE_PORT}{url}' registered")
        return

    data = extract_request_data(environ)
    controller.set_data(data)

    controller.set_method(method)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [controller.execute()]


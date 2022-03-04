from url_router import MainRouter
from urls.page_urls import *
import common.variables as vrb

def application(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    """
    router = MainRouter(registered_urls)
    url = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]
    query_params = environ['QUERY_STRING']
    print(query_params)

    if url[-1] == "/":
        url = url[:-1]

    if router.is_exist(url):
        controller = router.get_controller(url)()
    else:
        print(f"No route '{vrb.SITE_ADR}:{vrb.SITE_PORT}{url}' registered")
        return

    controller.set_method(method)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [controller.execute()]


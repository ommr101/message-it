from timeit import default_timer as timer

from app.core.status import StatusService


class RequestIncrementMiddleware:
    def __init__(self, app, status_service: StatusService):
        self._app = app
        self._status_service = status_service

    def __call__(self, environ, start_response):
        start = timer()
        res = self._app(environ, start_response)
        end = timer()
        self._status_service.increment_endpoint(environ['PATH_INFO'], end - start)
        return res
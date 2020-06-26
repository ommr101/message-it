from flask_restful import Resource

from app.core.status import StatusService
from app.entities import dto


class Status(Resource):
    def __init__(self, status_service: StatusService):
        self._status_service = status_service

    def get(self):
        requests_status: dto.RequestsStatus = self._status_service.get_endpoints_status()

        return requests_status.to_dict()

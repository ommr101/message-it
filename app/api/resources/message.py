from parser import ParserError
from typing import List

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app.core.message import MessageService
from app.entities import errors, dto


class Message(Resource):
    def __init__(self, message_service: MessageService):
        self._message_service: MessageService = message_service

    @jwt_required
    def get(self, message_id):
        request_sender_id = get_jwt_identity()

        message: dto.ReceivedMessage = self._message_service.get_one(request_sender_id, message_id)
        if not message:
            raise errors.MessageNotFound()

        return message.to_dict()

    @jwt_required
    def delete(self, message_id):
        request_sender_id = get_jwt_identity()

        has_deleted = self._message_service.delete(request_sender_id, message_id)
        if not has_deleted:
            raise errors.MessageNotFound()

        return {'success': True}


class Messages(Resource):
    def __init__(self, message_service: MessageService):
        self._message_service: MessageService = message_service

    @jwt_required
    def post(self):
        request_sender_id = get_jwt_identity()
        body = request.get_json()
        message_dto: dto.Message = dto.Message.from_dict(body)

        return {"message_id": self._message_service.create(request_sender_id, message_dto)}

    @jwt_required
    def get(self):
        request_sender_id = get_jwt_identity()

        message_filters = dto.GetAllMessagesFilters.from_dict(request.args)

        messages: List[dto.ReceivedMessage] = self._message_service.get_all(request_sender_id, message_filters.is_read)

        return [m.to_dict() for m in messages]
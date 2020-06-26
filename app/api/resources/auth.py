from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from config import conf
from app.core.user import UserService
from app.entities import errors, dto


class SignUp(Resource):
    def __init__(self, user_service: UserService):
        self._user_service: UserService = user_service

    def post(self):
        body = request.get_json()
        user_credentials: dto.User = dto.User.from_dict(body)

        user_id: str = self._user_service.create_new(user_credentials)

        return {'user_id': user_id}, 200


class SignIn(Resource):
    def __init__(self, user_service: UserService):
        self._user_service: UserService = user_service

    def post(self):
        body = request.get_json()
        user_credentials: dto.User = dto.User.from_dict(body)

        if not self._user_service.is_authorized:
            raise errors.InvalidCredentials()

        access_token = create_access_token(identity=str(user_credentials.id), expires_delta=conf.TOKEN_TTL)
        return {'token': access_token}, 200

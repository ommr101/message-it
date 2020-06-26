from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.api import middlewares
from app.api.extended_api import ExtendedAPI
from app.core.status import StatusSQLService
from config import conf
from app.core.message import MessageSQLService
from app.core.user import UserSQLService

status_service = StatusSQLService()
user_service = UserSQLService()
message_service = MessageSQLService()

messageit_app = Flask(__name__)
messageit_app.config.from_object(conf)
messageit_app.wsgi_app = middlewares.RequestIncrementMiddleware(messageit_app.wsgi_app, status_service)

api = ExtendedAPI(messageit_app)
bcrypt = Bcrypt(messageit_app)
jwt = JWTManager(messageit_app)

from app.api.resources.auth import SignIn, SignUp
from app.api.resources.message import Messages, Message
from app.api.resources.status import Status

api.add_resource(Messages, conf.MESSAGES_ENDPOINT, resource_class_kwargs={'message_service': message_service})
api.add_resource(Message, conf.MESSAGE_ENDPOINT,
                 resource_class_kwargs={'message_service': message_service})

api.add_resource(SignUp, conf.SIGNUP_ENDPOINT, resource_class_kwargs={'user_service': user_service})
api.add_resource(SignIn, conf.SIGNIN_ENDPOINT, resource_class_kwargs={'user_service': user_service})

api.add_resource(Status, conf.STATUS_ENDPOINT, resource_class_kwargs={'status_service': status_service})

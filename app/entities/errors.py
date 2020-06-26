class ApiError(Exception):
    status_code = 500

    def __init__(self, message):
        self.message = message


class MessageNotFound(ApiError):
    status_code = 404

    def __init__(self, message="Requested message not found"):
        self.message = message


class UnauthorizedReadMessage(ApiError):
    status_code = 401

    def __init__(self, message="You are not allowed to read this message"):
        self.message = message


class UnauthorizedWriteMessage(ApiError):
    status_code = 401

    def __init__(self, message="You are not allowed to write this message"):
        self.message = message


class SenderNotFound(ApiError):
    status_code = 404

    def __init__(self, message="Sender was not found"):
        self.message = message


class ReceiverNotFound(ApiError):
    status_code = 404

    def __init__(self, message="Receiver does not exist"):
        self.message = message


class InvalidCredentials(ApiError):
    status_code = 401

    def __init__(self, message="Email or password invalid"):
        self.message = message


class UsernameIsTaken(ApiError):
    status_code = 400

    def __init__(self, message="Username is taken"):
        self.message = message

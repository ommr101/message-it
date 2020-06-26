from flask_restful import Api

from app.entities import errors


class ExtendedAPI(Api):
    def handle_error(self, err):
        if isinstance(err, errors.ApiError):
            response = {
                'error': {
                    'type': err.__class__.__name__,
                    'message': err.message
                }
            }

            return response, err.status_code

        response = {
            'error': {
                'type': 'UnexpectedException',
                'message': 'An unexpected error has occurred.'
            }
        }

        return response, 500
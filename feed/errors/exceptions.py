from flask import current_app as app, jsonify


class BaseErrorResponse(Exception):
    """"""
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return {'message': self.message, 'payload': self.payload or {}}


class MissingRequiredParameter(BaseErrorResponse):
    pass


class UserExists(BaseErrorResponse):
    pass


class UnauthorizedAccess(BaseErrorResponse):
    pass


class FeedNotFound(BaseErrorResponse):
    pass


class FeedNotFollowed(BaseErrorResponse):
    pass


class FeedAlreadyFollowed(BaseErrorResponse):
    pass


@app.errorhandler(BaseErrorResponse)
def handle_error(error):
    """Constructs a flask.Response object in the event when an exception is raised"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def log_and_raise(logger, exc):
    logger.error(exc.message)
    raise exc

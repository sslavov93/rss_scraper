from flask import current_app as app, jsonify


class BaseErrorResponse(Exception):
    """Gathers data to be returned as an error response when an exception is raised"""
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
    """Constructs a flask.Response object in the event when an exception is raised

    :param error: The error object metadata to be wrapped
    :type error: BaseErrorResponse

    :returns: A flask response containing metadata around the exception that was raised
    :rtype: flask.Response
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def log_and_raise(logger, exc):
    """Logs a readable message from and re-raises the an exception

    :param logger: The application logger that logs the error message to the screen
    :type logger: flask.app.logger
    :param exc: The error object that is re-raised
    :type exc: BaseErrorResponse

    :raises Exception: Depending on what the error is
    """
    logger.error(exc.message)
    raise exc

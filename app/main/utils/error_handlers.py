from flask_restx import Api
from http import HTTPStatus
from .exceptions import NotFoundException, BadRequestException


def register_error_handlers(api: Api):
    @api.errorhandler(NotFoundException)
    def handle_not_found_exception(error: NotFoundException):
        return {"message": error.message}, HTTPStatus.NOT_FOUND

    @api.errorhandler(BadRequestException)
    def handle_bad_request_exception(error: BadRequestException):
        return {"message": error.message}, HTTPStatus.BAD_REQUEST

    @api.errorhandler(Exception)
    def handle_generic_exception(error):
        print(error)

        return (
            {"message": "Internal server error"},
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

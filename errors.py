import logging
from traceback import format_exc
from flask import jsonify, render_template
from schema import Response


def invalid_id(e):
    return error_hnd(code=400, type="INVALID_ID")


def not_found(e):
    return error_hnd(code=404, type='NOT_FOUND')


def invalid_input(e):
    return error_hnd(code=405, type="INVALID_INPUT")


def internal_server_error(e):
    return error_hnd(code=500, type='INTERNAL_SERVER_ERROR')


def error_hnd(code, type):
    logging.exception(format_exc())
    return jsonify(
        Response().dump({"code": code, "type": type, })), code

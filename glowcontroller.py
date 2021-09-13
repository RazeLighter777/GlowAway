from flask import Blueprint, abort
from flask import request
glowcontrol_api = Blueprint('glowcontrol_api', __name__)

@glowcontrol_api.before_request
def checkIfLocal():
    print(request.headers)

    if request.host == "127.0.0.1":
        return None
    abort(404)
@glowcontrol_api.route("/local")
def local():
    return "OK"
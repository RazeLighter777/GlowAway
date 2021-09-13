from flask import Blueprint

glowclient_api = Blueprint('glowclient_api', __name__)



@glowclient_api.route('/message')
def message():
    """Posts a message to the user.
    ---
    uuid : UUID of the server the user is on
    message: the message format
    signature : the signature of the alias + message
    pubkey : the public key of the user
    ---
    response "OK"/"BAD"
    """
    return "OK"
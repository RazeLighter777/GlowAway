import os
from configparser import ConfigParser
import subprocess
from datetime import time
from hashlib import sha256

import select
from ecdsa import ecdsa
from flask import Blueprint, request
from jsonschema import validate

from db import get_db, createUser
from validation import validateAlias

glowrouter_api = Blueprint('glowrouter_api', __name__)


# GlowRouting mode

@glowrouter_api.route('/users')
def users():
    """Returns list of users in room, and their addresses.
        ---
        uuid : UUID of the room the user is on
        signature : the signature of the message
        pubkey : the public key of the user
        ---
        Response : "OK"/"BAD"
        """
    return "OK"

@glowrouter_api.route('/register')
def register():
    """Registers on the server. Should be password protected.
        ---
        alias : the alias of the user
        signature : the signature of the message
        pubkey : the public key of the user
        password (optional) : The joincode of the server.
        ---
        Response : "OK"/"BAD"
        """
    schema = {
        "alias" : "string",
        "pubkey" : "string",
        "signature" : "string",
        "password" : "string",
        "required": ["alias", "pubkey", "signature"]
    }
    validate(request.json, schema=schema)
    if not validateAlias(request.json['alias']):
        return {"error" : "bad alias"}
    key = 0
    try:
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(request.json['pubkey']), curve=ecdsa.SECP256k1,
                                            hashfunc=sha256)  # the default is sha1
        vk.verify(bytes.fromhex(request.json['signature']), request.json['alias'])
    except:
        return {"error" : "bad key/signature"}
    return createUser(request.json['alias'],request.json['pubkey'])


@glowrouter_api.route('/join')
def join():
    """Attempts to join a room on this server.
        ---
        uuid : UUID of the server the user wishes to join
        alias : alias of the user.
        signature : the signature of the alias
        pubkey : the public key of the user
        password (optional) : The join code for the server
        address : The tor address for the user
        ---
        Response "OK"/"BAD"
    """
    return "OK"


@glowrouter_api.route('/logout')
def logout():
    """Leaves room on server.
        ---
        uuid : UUID of the server the user wishes to leave
        alias : alias of the user.
        signature : the signature of the alias
        pubkey : the public key of the user
        ---
        Response "OK"/"BAD"
    """
    return "OK"


@glowrouter_api.route('/list')
def list():
    """Lists rooms on this server.
        ---
        alias : alias of the user.
        signature : the signature of the alias
        pubkey : the public key of the user
        password (optional) : The list code for the server
        ---
        Response JSON encoding containing list of rooms and room metadata.
    """
    return {}


def init_glowrouter(config: ConfigParser):
    print("Initializing glowrouter . . . ")
    torrc = \
        """## Basic configuration
Log notice syslog
RunAsDaemon 0
DataDirectory ./tor

## Hidden service configuration
HiddenServiceDir ./tor/hiddenService
HiddenServicePort 80 {host}:{port}
    """.format(host = config["ROUTER"]["HOST"], port = config["ROUTER"]["PORT"])
    f = open(".torrc", "w")
    f.write(torrc)
    f.close()
    if os.name != "nt":
        cm = subprocess.Popen(["tor", "-f", ".torrc"],stdout=subprocess.DEVNULL)
    else:
        cm = subprocess.Popen(["torbin/Tor/tor.exe", "-f", ".torrc"],stdout=subprocess.DEVNULL)

import hashlib
import secrets
import sqlite3
from datetime import datetime
from uuid import UUID, uuid4

from flask import g

DATABASE = "glow.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def createSession(uuid: str, onion: str) -> dict:
    time = datetime.time()
    get_db().execute("INSERT INTO SESSIONS values (?,?,?)", (uuid, onion, str(time)))
    return {"user": uuid, "time": time}


def createUser(alias: str, pubkey: str) -> dict:
    uuid = createFingerprint(pubkey)
    if userExists(uuid):
        return {"error": "user exists"}
    get_db().execute("INSERT INTO USERS values (?,?,?)", (uuid, alias, pubkey))
    get_db().commit()
    return {"user": uuid}


def createFingerprint(pubkey: str) -> str:
    sha = hashlib.sha256()
    sha.update(pubkey.encode())
    return sha.hexdigest()

def generatePasswordHash(password : str) -> str:
    blake = hashlib.blake2s()
    blake.update(password.encode())
    salt = secrets.token_hex(8)
    blake.update(salt.encode())
    return blake.hexdigest() + ":" + salt

def verifyPasswordHash(password : str, passwordstore : str) -> bool:
    blake = hashlib.blake2s()
    blake.update(passwordstore.split(":")[0])
    blake.update(passwordstore.split(":")[1])
    return blake.hexdigest() == passwordstore.split(":")[0]

def createRoom(roomname : str, roompass : str = "") -> dict:
    uuid = uuid4()
    get_db().execute("INSERT INTO rooms values (?,?,?)", (str(uuid), roomname, generatePasswordHash(roompass) if roompass != "" else None))
    get_db().commit()
    return {"uuid" : str(uuid)}
def roomExists(uuid: str) -> bool:
    return len(get_db().execute("SELECT * FROM rooms WHERE roomId = ? ", (uuid,)).fetchall()) != 0

def getUsersInRoom(roomuuid : str) -> list:
    result = []
    for e in get_db().execute("SELECT userId FROM roomMemberships WHERE roomId = ?", (roomuuid,)).fetchall():
        result.append(e[0])
    return result

def getUserRole(roomuuid : str, useruuid : str) -> int:
    if not isUserInRoom(useruuid, roomuuid):
        return -1
    return get_db().execute("SELECT role FROM roomMemberships WHERE userId = ? AND roomId = ?", (useruuid, roomuuid)).fetchone()[0]
def userExists(uuid: str) -> bool:
    return len(get_db().execute("SELECT * FROM USERS WHERE userId = ? ", (uuid,)).fetchall()) != 0


def isUserInRoom(uuid: str, roomuuid: str) -> bool:
    return len(get_db().execute("SELECT * FROM roomMemberships WHERE userId = ? AND roomId = ?",
                                (uuid, roomuuid)).fetchall()) != 0


def addUserToRoom(uuid: str, roomuuid: str, role: int) -> bool:
    if isUserInRoom(uuid, roomuuid):
        return False
    get_db().execute("INSERT INTO roomMemberships values (?,?,?)", (uuid, roomuuid, role))
    get_db().commit()
    return True


def init_db():
    db = get_db()
    with open("schema.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def close_db():
    get_db().close()

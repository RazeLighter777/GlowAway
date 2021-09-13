import hashlib
import sqlite3
from datetime import datetime

from flask import g

DATABASE="glow.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def createSession(uuid : str, onion : str) -> dict:
    time = datetime.time()
    get_db().execute("INSERT INTO SESSIONS values (?,?,?)", (uuid, onion, str(time)))
    return {"user" : uuid, "time" : time}


def createUser( alias : str, pubkey : str) -> dict:
    uuid = createFingerprint(pubkey)
    if userExists(uuid):
        return {"error" : "user exists"}
    get_db().execute("INSERT INTO USERS values (?,?,?)", (uuid, alias, pubkey))
    get_db().commit()
    return {"user" : uuid}


def createFingerprint(pubkey : str) -> str:
    sha = hashlib.sha256()
    sha.update(pubkey.encode())
    return sha.hexdigest()


def userExists(uuid : str) -> bool:
    print(len(get_db().execute("SELECT * FROM USERS WHERE userId = ? ", (uuid,)).fetchall()))
    return len(get_db().execute("SELECT * FROM USERS WHERE userId = ? ", (uuid,)).fetchall()) != 0


def init_db():
    db = get_db()
    with open("schema.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
def close_db():
    get_db().close()
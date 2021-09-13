from flask import Flask

from db import *
from glowrouter import *
from glowclient import *
from glowcontroller import *

import configparser

app = Flask(__name__)
# Build Database
DATABASE = "glow.db"

# register all optional api

BUILD_VERSION = "0.0.0"


@app.route('/')
def version():
    """Returns version info of GlowAway client
    ---
    get:
      description: Get version string
      security:
      responses:
        200:
          content:
            application/text:
    """
    return "GlowAway " + BUILD_VERSION


configuration = configparser.ConfigParser()
configuration.read("config.ini")
print("Initializing GlowAway . . . ")
if configuration["MODULES"]["CLIENT"] == "yes":
    print("glow client")
    app.register_blueprint(glowclient_api)
if configuration["MODULES"]["ROUTER"] == "yes":
    app.register_blueprint(glowrouter_api)
    init_glowrouter(configuration)
if configuration["MODULES"]["CONTROLLER"] == "yes":
    app.register_blueprint(glowcontrol_api)
print("GOOD")
with app.app_context():
    init_db()
    print("role :" + str(getUserRole("52151382-aad8-4870-8198-0e3a2b8376f2", getUsersInRoom("52151382-aad8-4870-8198-0e3a2b8376f2")[0])))

@app.teardown_appcontext
def close_connection(exception):
    close_db()

if __name__ == "__main__":
    app.run(debug=True)

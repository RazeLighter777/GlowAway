import sys
import threading

from PySide2 import QtGui
from PySide2.QtWidgets import QApplication
from flask import Flask

from db import *
from glowrouter import *
from glowclient import *
from glowcontroller import *

import configparser

from gui import MainGui, MainWindow

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


def startGui():
    guiapp = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(guiapp.exec_())


with app.app_context():
    th = threading.Thread(target=startGui)
    th.start()
    init_db()


@app.teardown_appcontext
def close_connection(exception):
    close_db()


if __name__ == "__main__":

    app.run(debug=False, use_reloader=False)

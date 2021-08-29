# -*- coding: utf-8 -*-
import logging.handlers
import os

from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO
from redis import Redis

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/server.log", when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(FOLDER_ABSOLUTE_PATH, ".env"))

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["DEBUG"] = os.environ.get("IS_DEV", "false").lower() == "true"

# turn the flask app into a socket io app
socket_io = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# Redis client for NFS benchmark
REDIS_CLIENT = Redis(
    host=REDIS_HOST, password=REDIS_PASSWORD, db=0, charset="utf-8", decode_responses=True
)


@socket_io.on("connect", namespace="/socket")
def test_connect():
    """
    Socket connect
    Returns:

    """
    print("Client connected")


@socket_io.on("disconnect", namespace="/socket")
def test_disconnect():
    """
    Socket disconnected
    Returns:

    """
    print("Client disconnected")


if __name__ == "__main__":
    socket_io.run(app, port=80, host="0.0.0.0")

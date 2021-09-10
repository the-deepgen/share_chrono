# -*- coding: utf-8 -*-
import logging.handlers
import os
from typing import Dict

from dotenv import load_dotenv
from flask import Flask, render_template
from flask import request
from flask_socketio import SocketIO
from redis import Redis

from jwt_manager import JWTManager
from redis_timer import RedisTimer
from socket_timer import SocketTimer
from utils import api_response, get_utc_timestamp

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

jwt_manager = JWTManager(os.environ["JWT_SECRET_KEY"], RedisTimer(REDIS_CLIENT))

timers_pools: Dict[str, SocketTimer] = dict()


@app.route("/", methods=["GET"])
def index():
    """
    index ui
    Returns:

    """

    if len(timers_pools) > 0:
        key, timer = next(iter(timers_pools.items()))
        return render_template("index.html", data=key)
    # only by sending this page first will the client be connected to the socketio instance
    return render_template("index.html")


@app.route("/timer", methods=["POST"])
def creat_timer():
    """

    Returns:

    """
    res_dict = {}
    if request.form is not None:
        res_dict.update(request.form.to_dict())
    if request.json is not None:
        res_dict.update(request.json)

    pseudo = res_dict.get("pseudo")
    timer_name = res_dict.get("timer_name")

    if pseudo is None:
        return api_response(False, error_type="missing_parameter", name="pseudo"), 400

    if timer_name is None:
        return api_response(False, error_type="missing_parameter", name="timer_name"), 400

    if not isinstance(pseudo, str):
        return api_response(False, error_type="parameter_type", name="pseudo", parameter_type="str"), 400

    if not isinstance(timer_name, str):
        return api_response(False, error_type="parameter_type", name="timer_name", parameter_type="str"), 400

    # Creat a new timer into redis
    token, timer_body = jwt_manager.creat_timer(name=timer_name, pseudo=pseudo, utc_timestamp=get_utc_timestamp())
    # Update the timers pool thread
    timers_pools[token] = SocketTimer(key=token, timer=timer_body, socket_io=socket_io, jwt_manager=jwt_manager)
    return api_response(token=token, timer_body=timer_body.dict())


@app.route("/timer/start", methods=["POST"])
def start_timer():
    """

    Returns:

    """
    token = request.args.get("token")
    if token is None:
        return api_response(False, error_type="missing_parameter", name="token"), 400

    if token in timers_pools:
        return api_response(False, error_type="timer_already_exist"), 400

    timers_pools[token].on_start(None)


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


if __name__ == "__main__":
    socket_io.run(app, port=8080, host="0.0.0.0")

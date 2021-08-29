#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.handlers
import os
import sched
import time

from flask_socketio import Namespace
from flask_socketio import SocketIO

from jwt_manager import JWTManager
from models import Timer
from utils import api_response, get_utc_timestamp

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/socket_timer.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


class SocketTimer(Namespace):
    key: str
    timer: Timer
    socket_io: SocketIO
    jwt_manager: JWTManager

    def __init__(self, key: str, timer: Timer, socket_io: SocketIO, jwt_manager: JWTManager):
        """

        Args:
            key:
            timer:
            socket_io:
        """
        super().__init__()
        self.key = key
        self.timer = timer
        self.socket_io = socket_io
        self.jwt_manager = jwt_manager
        self.timer_stop = False
        self.sched = sched.scheduler(time.time, time.sleep)

    def on_connect(self, auth):
        """

        Returns:

        """
        PYTHON_LOGGER.info(f"{self.namespace} client connected")
        print(auth)

    def on_disconnect(self, auth):
        """

        Returns:

        """
        PYTHON_LOGGER.info(f"{self.namespace} client disconnected")
        print(auth)

    def _hearth_beat(self):
        """

        Returns:

        """
        if self.timer_stop:
            self.socket_io.emit("timer_stop", self.timer, namespace=self.namespace, broadcast=True)
            return

        # Set the new timestamp for the front page
        self.timer.time = get_utc_timestamp()
        self.socket_io.emit("hearth_beat", self.timer.dict(), namespace=self.namespace, broadcast=True)
        self.sched.enter(1, 1, self._hearth_beat)

    def on_start(self, data):
        """

        Args:
            data:

        Returns:

        """
        print(data)
        if self.timer.started_at > 0:
            self.socket_io.send("Timer already start", namespace=self.namespace)
            return

        # Update redis
        self.timer = self.jwt_manager.redis_timer.start_timer(self.key, get_utc_timestamp())
        # Creat event loop to update the timestamp every 1s
        self.sched.enter(1, 1, self._hearth_beat)
        self.sched.run(blocking=False)

    def on_checkpoint(self, data):
        """

        Args:
            data:

        Returns:

        """
        pseudo = data.get("pseudo")
        if pseudo is None:
            self.socket_io.send(api_response(success=False, error_type="missing_parameter", name="pseudo"),
                                json=True,
                                namespace=self.namespace)
            return
        # Add a new checkpoint
        checkpoint = self.jwt_manager.redis_timer.add_checkpoint(self.key, pseudo, get_utc_timestamp())
        # Update the model
        self.timer.history.append(checkpoint)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List, Optional

import redis
from redis import Redis

from models import Timer, Checkpoint


class RedisTimer:
    """
    Class to save and get information from timers
    """

    def __init__(self, redis_client: Redis):
        """
        Args:
            redis_client: Redis client for connection
        """
        self.redis_client = redis_client
        self.extra = {}

    @classmethod
    def get_redis_timer(cls, host: str, password: str, database_id=0, decode_responses=True, **kwargs):
        """
        Return an instant of a redis timer
        Args:
            host: redis host nam
            password: redis password
            database_id: db id (default: 0)
            decode_responses: if true decode the response to an python dict (default: true)
            **kwargs: extra parameters for Redis constructor

        Returns:
            a RedisTimer
        """
        client = redis.Redis(
            host=host, password=password, db=database_id, charset="utf-8", decode_responses=decode_responses, **kwargs
        )
        return cls(client)

    def creat_timer(self, key: str, name: str, pseudo: str, utc_timestamp: int) -> Timer:
        """
        Creat a new timer
        Args:
            key: Key of the timer (redis key)
            utc_timestamp: Timestamp of the creation
            pseudo: Ho creat the tiùer
            name: Name of the timer

        Returns:

        """
        body = {
            "pseudo": pseudo,
            "name": name,
            "created_at": utc_timestamp,
            "started_at": 0
        }
        self.redis_client.rpush(key, json.dumps(body))
        return Timer(**body)

    def start_timer(self, key: str, started_at: int) -> Timer:
        """
        Start the timer (set the started_at attribute with the timestamp)
        Args:
            key:
            started_at:

        Returns:

        """
        body = json.loads(self.redis_client.lpop(key))
        body["started_at"] = started_at
        self.redis_client.lpush(key, json.dumps(body))
        return Timer(**body)

    def get_timer(self, key: str) -> Optional[Timer]:
        """
        Get timer values
        Args:
            key: name of the metric to get

        Returns:
            Timer body
        """
        timer = [json.loads(v) for v in self.redis_client.lrange(key, 0, -1)]
        if len(timer) == 0:
            return None
        timer_information = Timer(**timer.pop(0))
        timer_information.history = [Checkpoint(**checkpoint) for checkpoint in timer]
        return timer_information

    def get_timer_keys(self) -> List[str]:
        """
        Get all timer names
        Returns:
            Keys list
        """
        return list(self.redis_client.keys())

    def delete_timer(self, key: str) -> Optional[Timer]:
        """
        Delete a timer and return the list
        Args:
            key: key to delete

        Returns:
            Metric List
        """
        response = self.get_timer(key)
        self.redis_client.delete(key)
        return response

    def add_checkpoint(self, key: str, name: str, utc_timestamp: int) -> Checkpoint:
        """
        Add a metric into redis
        Args:
            key: Key of the timer (redis key)
            name: Name of the user ho add the checkpoint,
            utc_timestamp: execution time timestamp


        Returns:
        """
        body = {"name": name, "timestamp": utc_timestamp, "extra": self.extra}
        self.redis_client.rpush(key, json.dumps(body))
        return Checkpoint(**body)

    def set_extra(self, **kwargs):
        """
        Add extra information about the metric (set extra attribute)
        Args:
            **kwargs: extra information to add
        """
        self.extra = kwargs

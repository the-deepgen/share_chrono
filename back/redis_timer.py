#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List, Optional

import redis
from redis import Redis


class RedisTimer:

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

    def creat_timer(self, key: str, name: str, utc_timestamp: int):
        """
        Creat a new timer
        Args:
            key: Key of the timer (redis key)
            utc_timestamp: Timestamp of the creation
            name: Name of the timer

        Returns:

        """
        body = {
            "name": name,
            "created_at": utc_timestamp,
            "time": 0
        }
        self.redis_client.rpush(key, body)
        return body

    def get_timer(self, key: str) -> Optional[dict]:
        """
        Get timer values
        Args:
            key: name of the metric to get

        Returns:
            Timer body
            {
                "name": (string)
                "created_at": (int) utc timestamp,
                "time": (int) timer duration in seconds,
                "history": (list of checkpoint)
            }
            Checkpoint Body
            {
                "name": (string) Name of the user ho add the checkpoint,
                "duration": (int) execution time in seconds,
                "extra": (dict) extra information
            }
        """
        timer = [json.loads(v) for v in self.redis_client.lrange(key, 0, -1)]
        if len(timer) == 0:
            return None
        timer_information = timer.pop(0)
        timer_information["history"] = timer
        return timer_information

    def get_timer_keys(self) -> List[str]:
        """
        Get all timer names
        Returns:
            Keys list
        """
        return list(self.redis_client.keys())

    def delete_timer(self, key: str) -> Optional[dict]:
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

    def add_checkpoint(self, key: str, name: str, duration: int):
        """
        Add a metric into redis
        Args:
            key: Key of the timer (redis key)
            name: Name of the user ho add the checkpoint,
            duration: execution time in seconds


        Returns:
        """
        self.redis_client.rpush(key, json.dumps({"name": name, "duration": duration, "extra": self.extra}))

    def set_extra(self, **kwargs):
        """
        Add extra information about the metric (set extra attribute)
        Args:
            **kwargs: extra information to add
        """
        self.extra = kwargs

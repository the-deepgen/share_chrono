#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional, Tuple

import jwt

from models import Timer
from redis_timer import RedisTimer

JWT_ALGORITHM = "HS256"


class JWTManager:
    """
    Create and managed JSON Web Token (JWT)
    """
    secret: str
    redis_timer: RedisTimer
    token_audience: str = "timer:auth"

    def __init__(self, secret: str, redis_timer: RedisTimer):
        """
        Args:
            secret: secret to encode the jwt token
            redis_timer: Redis timer client
        """
        self.secret = secret
        self.redis_timer = redis_timer

    def __call__(self, token: str) -> Optional[dict]:
        """
        Decrypt a JWT using the secret and verifies that the JWT his valid

        Args:
            token: kwt token

        Returns:
            Timer body

        Raises:
            HTTPException (with http code 401)
        """
        assert token is not None
        try:
            data = jwt.decode(token, self.secret, audience=self.token_audience, algorithms=[JWT_ALGORITHM])
            assert data.get("timestamp") is not None and data.get("name") is not None
        except (jwt.exceptions.ExpiredSignatureError, jwt.PyJWTError):
            return None
        return self.redis_timer.get_timer(token)

    def creat_timer(self, name: str, pseudo: str, utc_timestamp: int) -> Tuple[str, Timer]:
        """
        Encrypts the JWT

        Args:
            utc_timestamp: Timestamp of the creation
            pseudo: Ho creat the timer
            name: Name of the timer

        Returns:
            JWT token of the timer, timer body
        """
        token = jwt.encode({"name": name, "timestamp": utc_timestamp}, self.secret, algorithm=JWT_ALGORITHM)
        return token, self.redis_timer.creat_timer(key=token, pseudo=pseudo, name=name, utc_timestamp=utc_timestamp)

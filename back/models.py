#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List

from pydantic import BaseModel


class Checkpoint(BaseModel):
    """
    Checkpoint model
    {
        "name": (string) Name of the user ho add the checkpoint,
        "timestamp": (int) execution time timestamp,
        "extra": (dict) extra information
    }
    """
    name: str
    timestamp: int
    extra: Optional[dict] = {}


class Timer(BaseModel):
    """
    Timer model

    {
        "name": (string)
        "created_at": (int) utc timestamp,
        "started_at": (int) utc timestamp,
        "time": (int) Current value of the timer wen is started
        "history": (list of checkpoint)
    }
    """

    name: str
    pseudo: str
    created_at: int
    started_at: Optional[int] = 0
    time: Optional[int] = 0
    history: Optional[List[Checkpoint]] = []

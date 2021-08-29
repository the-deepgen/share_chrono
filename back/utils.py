#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import datetime


def get_utc_timestamp():
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple())


def api_response(success=True, **kwargs):
    return {
        "success": success,
        "response": kwargs
    }

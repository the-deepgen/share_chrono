#!/usr/bin/env python
# -*- coding: utf-8 -*-
import calendar
import datetime


def get_utc_timestamp():
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple())

#!/usr/bin/python
# -*- coding: utf-8 -*-


class Post:

    url = None
    ts = None
    shouted = False

    def __init__(self, url=None, ts=None, shouted=False):
        self.url = url
        self.ts = ts
        self.shouted = shouted

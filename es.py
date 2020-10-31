#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8

import io
import os
import sys
import time
import requests
import json
import uuid
from doc import Doc


class ES:
    def __init__(self, host):
        self.host = host
        self.saveUrl = "/blog/_create"
        self.searchUrl = "/blog/_search"

    def createIndex(self):
        return None

    def saveDoc(self, document):
        print("saving %s" % (document.title))
        id = uuid.uuid4().hex
        payload = {
            'title': document.title,
            'author': document.author,
            'link': str(document.link),
            'source': document.source,
            'sourceName': document.sourceName,
            'date': document.date,
            'content': document.content
        }
        url = self.host + self.saveUrl + "/" + id
        r = requests.post(url, json=payload)
        if r.status_code < 200 or r.status_code > 299:
            print("saveDoc error. status code:%d" % (r.status_code))
            return False
        print("saving result %s \n" % (r.content))
        return True

    def __repr__(self):
        return "ES: {host=%s}" % (self.host)

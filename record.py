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
import pymysql
import yaml


class Record:
    def getLatestRecord(self, source):
        return ""


class FileRecord(Record):
    def __init__(self):
        self.file = "record.yaml"
        recordYaml = open(self.file, "r")
        self.record = yaml.safe_load(recordYaml)
    def getLatestRecord(self, source):
        try:
            return self.record["records"][source]
        except Exception as e:
            print("getLatestRecord error", e)
            return ""


class DbRecord(Record):
    def __init__(self):
        self.db = pymysql.connect(
            host="127.0.0.1",
            user="admin",
            password="Admin_@123",
            database="test",
            charset="utf8"
        )
        self.cursor = self.db.cursor()

f = FileRecord()
print(f.getLatestRecord("meituan"))
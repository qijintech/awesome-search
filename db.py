#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8

import io
import os
import sys
import time
from config import Config
import pymysql


class DB:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.db =  pymysql.connect(self.host, self.username, self.password, self.database)

    def recordBlog(self, source, blogID):
        table = "awesome_search_blog"
        sql = "insert into %s (source, blog_id) values ('%s', '%s')" % (table, source, blogID)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("recordBlog error", e)
            self.db.rollback()
    
    def isBlogExist(self, source, blogID):
        table = "awesome_search_blog"
        sql = "select count(*) from %s where source='%s' and blog_id='%s'" % (table, source, blogID)
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if len(data) > 0 and data[0] > 0:
            return True
        return False


if __name__ == '__main__':
    config = Config(".")
    host=config.get("mysql", "host")
    username=config.get("mysql", "username")
    password=config.get("mysql", "password")
    database=config.get("mysql", "database")

    db = DB(host, username, password, database)
    print(db.isBlogExist("meituan", "asdfassdf"))
    source = "meituan"
    blogID = "asssss"
    db.recordBlog(source, blogID)


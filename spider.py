#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8

import io
import os
import sys
import time
import requests
import json
from bs4 import BeautifulSoup
from blog import WeChatBlog
from datetime import datetime
from config import Config


class WeChatSpider:
    def __init__(self, biz, token, key):
        self.biz = biz
        self.token = token
        self.key = key
        self.urlTemplate = "http://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={0}&f=json&offset={1}&count={2}&is_ok=1&scene=124&uin=MjM2MDI0OTIyMQ%3D%3D&key={3}&pass_ticket=&wxton=&appmsg_token={4}&x5=0&f=json HTTP/1.1"

    def getUrl(self, offset, count):
        return self.urlTemplate.format(self.biz, offset, count, self.key, self.token)

    def getBlogs(self, offset, count, recursive):
        allBlogs = []
        while(True):
            url = self.getUrl(offset, count)
            blogs = self.doQuery(url)
            print(blogs)
            allBlogs += blogs
            if len(blogs) == 0 or recursive is False:
                break
            offset = offset + count + 1
            time.sleep(2)
        return allBlogs

    def doQuery(self, url):
        msgList = self.getMsgList(url)
        if len(msgList) == 0:
            return []
        blogs = []
        for msg in msgList:
            blog = self.genBlog(msg)
            print(blog)
            if blog is not None:
                blogs.append(blog)
        return blogs

    def genBlog(self, msg):
        if msg is None:
            return None
        info = msg["app_msg_ext_info"]
        if info is None:
            return None
        ts = msg["comm_msg_info"]["datetime"]
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        return WeChatBlog(str(info["fileid"]), info["title"].strip(), info["content_url"].strip(), info["author"].strip(), date, info["cover"].strip())

    def getMsgList(self, url):
        print("WeChatSpider doQuery. url=%s" % (url))
        r = requests.get(url)
        if r.status_code < 200 or r.status_code >= 300:
            print("WeChatSpider doQuery error. url=%s, statusCode=%d" %
                  (url, r.status_code))
            return []
        resp = json.loads(r.content)
        if resp["ret"] < 0:
            print("WeChatSpider doQuery error. url=%s, msg=%s" %
                  (url, resp["errmsg"]))
            return []
        return json.loads(resp["general_msg_list"])["list"]


def exportToFile(blogs):
    fp = open("iqiyi.blog", "w")
    for blog in blogs:
        line = "%s, %s, %s, %s, %s\n" % (
            blog.id, blog.title, blog.link, blog.author, blog.date)
        print(line)
        fp.write(line)
    fp.close()

if __name__ == '__main__':
    config = Config(".")
    biz = config.get("wechat", "uin")
    key = config.get("wechat", "key")
    token = config.get("wechat", "token")
    wechatSpider = WeChatSpider(biz, token, key)
    blogs = wechatSpider.getBlogs(0, 10, True)
    exportToFile(blogs)

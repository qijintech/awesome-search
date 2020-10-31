#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8

import io
import os
import sys
import time
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from blog import Blog
from blog import WeChatBlog
from blog import MeituanBlog

from config import Config
from doc import Doc
from es import ES
from fetch import MeiTuanFetcher


class WeChatSpider:
    def __init__(self, biz, uin, token, key):
        self.biz = biz
        self.uin = uin
        self.token = token
        self.key = key
        self.urlTemplate = "http://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz={0}&f=json&offset={1}&count={2}&is_ok=1&scene=124&uin={3}&key={4}&pass_ticket=&wxton=&appmsg_token={5}&x5=0&f=json HTTP/1.1"

    def getUrl(self, offset, count):
        return self.urlTemplate.format(self.biz, offset, count, self.uin, self.key, self.token)

    def getBlogs(self, offset, count, recursive):
        allBlogs = []
        while(True):
            url = self.getUrl(offset, count)
            blogs = self.doQueryBlogs(url)
            allBlogs += blogs
            if len(blogs) == 0 or recursive is False:
                break
            offset = offset + count + 1
            time.sleep(2)
        return allBlogs

    def getBlogAndDoc(self, blog):
        if blog == None:
            return
        doc = self.doQueryDoc(blog)
        if doc is not None:
            blog.setDoc(doc)

    def doQueryDoc(self, blog):
        url = blog.link
        if url == "":
            return None
        print("WeChatSpider doQueryDoc. url=%s\n" % (url))
        r = requests.get(url)
        if r.status_code < 200 or r.status_code >= 300:
            print("WeChatSpider doQueryDoc error. url=%s, statusCode=%d\n" %
                  (url, r.status_code))
        bs = BeautifulSoup(r.content)
        return self.genDoc(blog, bs)

    def genDoc(self, blog, bs):
        content = ""
        contentList = bs.findAll(name="div", attrs={"class": "rich_media_content"})
        if len(contentList) > 0:
            content = contentList[0].text
        doc = Doc(blog.title, blog.link, blog.author, content, blog.date)
        print(doc)
        return doc
        
    def doQueryBlogs(self, url):
        msgList = self.getMsgList(url)
        if len(msgList) == 0:
            return []
        blogs = []
        for msg in msgList:
            blog = self.genBlog(msg)
            print(blog, "\n")
            if blog is not None:
                blogs.append(blog)
        return blogs
    
    def getMsgList(self, url):
            print("WeChatSpider getMsgList. url=%s" % (url))
            r = requests.get(url)
            if r.status_code < 200 or r.status_code >= 300:
                print("WeChatSpider getMsgList error. url=%s, statusCode=%d" %
                    (url, r.status_code))
                return []
            resp = json.loads(r.content)
            if resp["ret"] < 0:
                print("WeChatSpider getMsgList error. url=%s, msg=%s" %
                    (url, resp["errmsg"]))
                return []
            return json.loads(resp["general_msg_list"])["list"]

    def genBlog(self, msg):
        if msg is None:
            return None
        if "app_msg_ext_info" not in msg:
            return None
        info = msg["app_msg_ext_info"]
        ts = msg["comm_msg_info"]["datetime"]
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        title = info["title"].strip()
        if title == "":
            return None
        id = info["fileid"]
        if id == 0 and "comm_msg_info" in msg:
            id = msg["comm_msg_info"]["id"]
        return WeChatBlog(str(id), title, info["content_url"].strip(), info["author"].strip(), date, info["cover"].strip())


class MeiTuanSpider:
    urlTemplate = "https://tech.meituan.com//page/ID.html"
    def getBlogs(self, recursive):
        index = 1
        url = "https://tech.meituan.com/"
        allBlogs = []
        while True:
            index +=1
            print("meituan getBlogs url: %s \n" % (url))
            blogs = self.doQueryBlogs(url)
            allBlogs += blogs
            print(blogs)
            # docs = self.getDocs(blogs)
            if len(blogs) == 0 or recursive is False:
                break
            urlTmp = MeiTuanSpider.urlTemplate
            url = urlTmp.replace("ID", str(index))
        return allBlogs

    def doQueryBlogs(self, url):
        r = requests.get(url)
        content = BeautifulSoup(r.content)
        bsBlogs = content.findAll(name="div", attrs={"class" :"post-container"})
        blogs = []
        for bsBlog in bsBlogs:
            blog = self.genBlog(bsBlog)
            if blog is not None:
                blogs.append(blog)
        return blogs

    def genBlog(self, bsBlog):
        title, link = self.getTitleAndLink(bsBlog)
        id = self.getID(link)
        date = self.getDate(bsBlog)
        abstract = self.getAbstract(bsBlog)
        author = self.getAuthor(bsBlog)
        if title == "" or link == "" or author == "":
            return None
        return MeituanBlog(id, title, link, author, date, abstract)

    def getTitleAndLink(self, bsBlog):
        titleList = bsBlog.findAll(name="h2", attrs={"class": "post-title"})
        if len(titleList) > 0:
            tagA = titleList[0].findAll('a')
            if len(tagA) > 0:
                return tagA[0].text, tagA[0]["href"]
        return "", ""

    def getDate(self, paper):
        dateList = paper.findAll(name="span", attrs={"class": "m-post-date"})
        if len(dateList) > 0:
            return dateList[0].text
        return ""

    def getAbstract(self, paper):
        abstractList = paper.findAll(name="div", attrs={"class": "post-content post-expect"})
        if len(abstractList) > 0:
            return abstractList[0].text
        return ""
    
    def getAuthor(self, bsBlog):
        authorList = bsBlog.findAll(name="span", attrs={"class": "m-post-nick"})
        if len(authorList) > 0:
            return authorList[0].text
        return ""

    def getID(self, link):
        arr = link.split("/")
        if len(arr) > 0:
            return arr[len(arr) - 1]
        return link

    def doQueryDoc(self, blog):
        url = blog.link
        if url == "":
            return None
        print("MeiTuanSpider doQueryDoc. url=%s\n" % (url))
        r = requests.get(url)
        if r.status_code < 200 or r.status_code >= 300:
            print("MeiTuanSpider doQueryDoc error. url=%s, statusCode=%d\n" %
                  (url, r.status_code))
        bs = BeautifulSoup(r.content)
        return self.genDoc(blog, bs)
    
    def genDoc(self, blog, bs):
        content = ""
        contents = bs.findAll(name="div", attrs={"class": "post-content"})
        if len(contents) > 0:
            content = contents[0].text
        doc = Doc(blog.title, blog.link, blog.author, content, blog.date)
        print(doc)
        return doc

class DbKernalSpider:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def getBlogs(self, recursive):
        index = 1
        allBlogs = []
        retryTimes = 2
        while True:
            url = self.getUrl()
            print("kernal getBlogs url: %s \n" % (url))
            blogs = self.doQueryBlogs(url)
            allBlogs += blogs
            print(blogs)
            retryTimes -=1
            if retryTimes <= 0 and (len(blogs) == 0 or recursive is False):
                break
            self.preMonth()
        return allBlogs

    def preMonth(self):
        self.month -= 1
        if self.month <=0:
            self.year -= 1
            self.month = 12

    def getUrl(self):
        if self.month < 10:
            return "http://mysql.taobao.org/monthly/%d/0%d" % (self.year, self.month)
        return "http://mysql.taobao.org/monthly/%d/%d" % (self.year, self.month)

    def doQueryBlogs(self, url):
        r = requests.get(url)
        content = BeautifulSoup(r.content)
        bsContent = content.findAll(name="div", attrs={"class" :"content typo"})
        blogs = []
        if len(bsContent) > 0:
            bsAtags = bsContent[0].findAll(name='a')
            for bsBlog in bsAtags:
                blog = self.genBlog(bsBlog)
                print(blog)
                if blog is not None:
                    blogs.append(blog)
        return blogs

    def genBlog(self, bsBlog):
        href = bsBlog["href"]
        id = href
        link = "http://mysql.taobao.org" + href
        date = href.split("/monthly/")[1]
        title = bsBlog.text.strip()
        return Blog(id, title, link, "阿里云内核组", date)

    def doQueryDoc(self, blog):
        url = blog.link
        if url == "":
            return None
        print("DbKernalSpider doQueryDoc. url=%s\n" % (url))
        r = requests.get(url)
        if r.status_code < 200 or r.status_code >= 300:
            print("DbKernalSpider doQueryDoc error. url=%s, statusCode=%d\n" %
                  (url, r.status_code))
        bs = BeautifulSoup(r.content)
        return self.genDoc(blog, bs)

    def genDoc(self, blog, bs):
        content = ""
        contentList = bs.findAll(name="div", attrs={"id": "container"})
        if len(contentList) > 0:
            content = contentList[0].text
        doc = Doc(blog.title, blog.link, blog.author, content, blog.date)
        print(doc)
        return doc

if __name__ == '__main__':
    spider = DbKernalSpider(2020, 4)
    blogs = spider.getBlogs(False)
    for blog in blogs:
        doc = spider.doQueryDoc(blog)
        print(doc)

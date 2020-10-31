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
from fetch import MeiTuanFetcher
from fetch import TouTiaoFetcher
from es import ES

urlTemplate = "https://tech.meituan.com//page/ID.html"
sourceType = "toutiao"
sourceName = "字节跳动技术团队"

rowTemplate = '''
<div class="panel panel-default">
  <div class="panel-heading">
    <h1 class="panel-title"><a href="LINK">TITLE</a></h1>
  </div>
  <div class="panel-body">
    ABSTRACT
  </div>
  <div class="panel-footer">DATE</div>
</div>
'''

outputTemplate = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8" /><title>数据库内核月报</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<style type="text/css">
li{padding-top: 10px;font-size: 18px;}
.panel-title{font-size:20px; color: #337ab7;}
</style>
</head>
<body>
<div class="container">
CONTENT
</div>
</body>
</html>
'''


class Blog:
    def __init__(self, title, link, date, abstract):
        # self.title = title.encode("utf-8")
        # self.link = link.encode("utf-8")
        # self.date = date.encode("utf-8")
        # self.abstract = abstract.encode("utf-8")
        self.title = title
        self.link = link
        self.date = date
        self.abstract = abstract

    def __repr__(self):
        return "Blog: { title=%s, link=%s, date=%s }" % (self.title, self.link, self.date)


def doCrawl(isAll):
    url = "http://mp.weixin.qq.com/mp/homepage?__biz=MzI1MzYzMjE0MQ==&hid=3&sn=3bd0ff29471b05c97081adf7f7a3c9be&scene=18&begin=0&count=50&action=appmsg_list&f=json&r=0.9836782521999012&appmsg_token="
    blogs = getBlogsFromOnePage(url)
    # print(blogs)
    docs = getDocs(blogs)
    if len(docs) > 0:
        exportToES(docs)


def getBlogsFromOnePage(url):
    r = requests.post(url)
    resp = json.loads(r.content)
    blogs = []
    for paper in resp["appmsg_list"]:
        blog = parsePaper(paper)
        if blog is not None:
            blogs.append(blog)
    return blogs


def parsePaper(paper):
    # title && link
    # title, link = getTitleAndLink(paper)
    title = paper["title"]
    link = paper["link"]
    # date
    # date = getDate(paper)
    date = ""
    # abstract
    # abstract = getAbstract(paper)
    abstract = ""
    return Blog(title, link, date, abstract)


def getTitleAndLink(paper):
    title = None
    link = None
    titleList = paper.findAll(name="h2", attrs={"class": "post-title"})
    if len(titleList) > 0:
        tagA = titleList[0].findAll('a')
        if len(tagA) > 0:
            link = tagA[0]["href"]
            title = tagA[0].text
    return title, link


def getDate(paper):
    date = None
    dateList = paper.findAll(name="span", attrs={"class": "m-post-date"})
    if len(dateList) > 0:
        date = dateList[0].text
    return date


def getAbstract(paper):
    abstract = None
    abstractList = paper.findAll(
        name="div", attrs={"class": "post-content post-expect"})
    if len(abstractList) > 0:
        abstract = abstractList[0].text
    return abstract


def exportToFile(blogs):
    fp = open("meituan_blog.html", "w")
    content = ""
    for blog in blogs:
        row = rowTemplate
        row = row.replace("TITLE", str(blog.title))
        row = row.replace("LINK", str(blog.link))
        row = row.replace("DATE", str(blog.date))
        row = row.replace("ABSTRACT", str(blog.abstract))
        content += row
    output = outputTemplate.replace("CONTENT", str(content))
    fp.write(output)
    fp.close()
    print("success")


def getDocs(blogs):
    urls = []
    print("blog count: %d" % (len(blogs)))
    for blog in blogs:
        urls.append(blog.link)
    fetcher = TouTiaoFetcher(urls, sourceType, sourceName)
    return fetcher.doFetch()


def exportToES(docs):
    es = ES()
    for doc in docs:
        es.saveDoc(doc)
    print("exportToES finished")


if __name__ == '__main__':
    doCrawl(True)
    # print output

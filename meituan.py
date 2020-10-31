#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8

import io, os, sys, time
import requests, json
from bs4 import BeautifulSoup
from fetch import MeiTuanFetcher
from es import ES

urlTemplate = "https://tech.meituan.com//page/ID.html"
sourceType = "meituan"
sourceName = "美团点评技术博客"

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
    maxPage = 50
    if isAll is not True:
        maxPage = 1
    allBlogs = []
    for idx in range(1,maxPage+1):
        url = urlTemplate
        url = url.replace("ID", str(idx))
        if idx == 1:
            url = "https://tech.meituan.com/"
        print(url)
        blogs = getBlogsFromOnePage(url)
        docs = getDocs(blogs)
        if len(docs) > 0:
            exportToES(docs)
        allBlogs += blogs
    # exportToFile(allBlogs)

def getBlogsFromOnePage(url):
    r = requests.get(url)
    content = BeautifulSoup(r.content)
    papers = content.findAll(name="div", attrs={"class" :"post-container"})
    blogs = []
    for paper in papers:
        blog = parsePaper(paper)
        if blog is not None:
            blogs.append(blog)
    return blogs

def parsePaper(paper):
    # title && link
    title, link = getTitleAndLink(paper)
    # date
    date = getDate(paper)
    # abstract
    abstract = getAbstract(paper)
    if title is None:
        return None
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
    abstractList = paper.findAll(name="div", attrs={"class": "post-content post-expect"})
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
    fetcher = MeiTuanFetcher(urls, sourceType, sourceName)
    return fetcher.doFetch()

def exportToES(docs):
    es = ES()
    for doc in docs:
        es.saveDoc(doc)
    print("exportToES finished")
    

if __name__ == '__main__':
    doCrawl(True)
    # print output

#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8

import datetime
from es import ES
from db import DB
from config import Config
from spider import WeChatSpider
from spider import MeiTuanSpider
from spider import DbKernalSpider

def fetchWeChatBlogs(biz, source, sourceName, config, es, record, recursive):
    uin = config.get("wechat", "uin")
    key = config.get("wechat", "key")
    token = config.get("wechat", "token")
    print(biz, uin, key, token)
    wechatSpider = WeChatSpider(biz, uin, token, key)
    blogs = wechatSpider.getBlogs(0, 10, recursive)
    count = 0
    for blog in blogs:
        count+=1
        if record.isBlogExist(source, blog.id) is True:
            print("%s from source %s with id %s already exist" % (blog.title, source, blog.id))
            print("saveDoc process: ========= %d/%d =========\n" % (count, len(blogs)))
            continue
        doc = wechatSpider.doQueryDoc(blog)
        if doc is None:
            continue
        doc.setSource(source)
        doc.setSourceName(sourceName)
        es.saveDoc(doc)
        record.recordBlog(source, blog.id)
        print("saveDoc process: ========= %d/%d =========\n" % (count, len(blogs)))

def fetchMeiTuan(source, sourceName, config, es, record):
    print("fetching %s =========> \n" % (source))
    meituanSpider = MeiTuanSpider()
    blogs = meituanSpider.getBlogs(False)
    count = 0
    for blog in blogs:
        count+=1
        if record.isBlogExist(source, blog.id) is True:
            print("%s from source %s with id %s already exist" % (blog.title, source, blog.id))
            print("saveDoc process: ========= %d/%d =========\n" % (count, len(blogs)))
            continue
        doc = meituanSpider.doQueryDoc(blog)
        if doc is None:
            continue
        doc.setSource(source)
        doc.setSourceName(sourceName)
        es.saveDoc(doc)
        record.recordBlog(source, blog.id)
        print("saveDoc process: ========= %d/%d =========\n" % (count, len(blogs)))

def saveDoc(blogs, spider, source, sourceName, es, record):
    count = 0
    for blog in blogs:
        count+=1
        if record.isBlogExist(source, blog.id) is True:
            print("%s from source %s with id %s already exist" % (blog.title, source, blog.id))
            print("saveDoc process: ========= %d/%d =========\n" % (count, len(blogs)))
            continue
        doc = spider.doQueryDoc(blog)
        if doc is None:
            continue
        doc.setSource(source)
        doc.setSourceName(sourceName)
        es.saveDoc(doc)
        record.recordBlog(source, blog.id)
        print("saveDoc process: ========= %d/%d =========\n" % (count, len(blogs)))

def fetchIQiYi(source, sourceName, config, es, record):
    print("fetching %s =========> \n" % (source))
    biz = "MzI0MjczMjM2NA=="
    fetchWeChatBlogs(biz, source, sourceName, config, es, record, False)

def fetchTouTiao(source, sourceName, config, es, record):
    print("fetching %s =========> \n" % (source))
    biz = "MzI1MzYzMjE0MQ=="
    fetchWeChatBlogs(biz, source, sourceName, config, es, record, False)

def fetchDataFunTalk(source, sourceName, config, es, record):
    print("fetching %s =========> \n" % (source))
    biz = "MzU1NTMyOTI4Mw=="
    fetchWeChatBlogs(biz, source, sourceName, config, es, record, False)

def fetchXianYu(source, sourceName, config, es, record):
    print("fetching %s =========> \n" % (source))
    biz = "MzU4MDUxOTI5NA=="
    fetchWeChatBlogs(biz, source, sourceName, config, es, record, False)

def fetchDbKernal(source, sourceName, config ,es, record):
    print("fetching %s =========> \n" % (source))
    now = datetime.date.today()
    spider = DbKernalSpider(now.year, now.month - 1)
    blogs = spider.getBlogs(False)
    saveDoc(blogs, spider, source, sourceName, es, record)


if __name__ == '__main__':
    config = Config(".")

    mysqlHost=config.get("mysql", "host")
    username=config.get("mysql", "username")
    password=config.get("mysql", "password")
    database=config.get("mysql", "database")
    record = DB(mysqlHost, username, password, database)

    esHost = config.get("es", "host")
    es = ES(esHost)

    # fetchMeiTuan("meituan", "美团点评技术博客", config, es, record)
    # fetchIQiYi("iqiyi", "爱奇艺技术产品团队", config, es, record)
    # fetchTouTiao("toutiao", "爱奇艺技术产品团队", config, es, record)
    # fetchXianYu("xianyu", "闲鱼技术", config, es, record)
    # fetchDbKernal("dbkernal", "阿里云数据库内核月报", config, es, record)
    fetchDataFunTalk("toutiao", "DataFunTalk", config, es, record)

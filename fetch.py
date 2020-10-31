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
from doc import Doc


class Fetcher:
    def __init__(self, urls, source, sourceName):
        self.urls = urls
        self.source = source
        self.sourceName = sourceName

    def __repr__(self):
        return "Request: {" + self.urls + ", " + self.source + "}"

    def doFetch(self):
        docs = []
        for url in self.urls:
            doc = self.fetchUrl(url)
            if doc is not None:
                docs.append(doc)
        return docs

    def fetchUrl(self, url):
        print("fetching url: %s" % (url))
        r = requests.get(url)
        result = BeautifulSoup(r.content, "html.parser")
        return Doc(self.getTitle(result), url, self.getAuthor(result), self.getContent(result), self.source, self.sourceName, self.getDate(result))

    def getTitle(self, result):
        return ""

    def getAuthor(self, result):
        return ""

    def getDate(self, result):
        return ""

    def getContent(self, result):
        return ""


class MeiTuanFetcher(Fetcher):
    def getTitle(self, result):
        titles = result.findAll(name="h1", attrs={"class": "post-title"})
        if len(titles) > 0:
            return titles[0].text
        return ""

    def getAuthor(self, result):
        authors = result.findAll(name="span", attrs={"class": "m-post-nick"})
        author = ""
        if len(authors) > 0:
            author = authors[0].text
            arr = author.split(":")
            if len(arr) > 1:
                author = author.split(":")[1]
        return author

    def getDate(self, result):
        dates = result.findAll(name="span", attrs={"class": "m-post-date"})
        if len(dates) > 0:
            return dates[0].text
        return ""

    def getContent(self, result):
        contents = result.findAll(name="div", attrs={"class": "post-content"})
        if len(contents) > 0:
            return contents[0].text
        return ""


class TouTiaoFetcher(Fetcher):
    def getTitle(self, result):
        titles = result.findAll(name="h2", attrs={"id": "activity-name"})
        if len(titles) > 0:
            return titles[0].text.strip()
        return ""

    def getAuthor(self, result):
        authors = result.findAll(name="span", attrs={"class": "rich_media_meta rich_media_meta_text"})
        author = ""
        if len(authors) > 0:
            author = authors[0].text.strip()
        return author

    def getDate(self, result):
        dates = result.findAll(name="span", attrs={"class": "m-post-date"})
        if len(dates) > 0:
            return dates[0].text
        return ""

    def getContent(self, result):
        contents = result.findAll(name="div", attrs={"id": "js_content"})
        if len(contents) > 0:
            return contents[0].text
        return ""

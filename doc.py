
import io
import os
import sys
import time
import requests
import json


class Doc:
    def __init__(self, title, link, author, content, date):
        self.title = title
        self.author = author
        self.content = content
        self.link = str(link)
        self.date = date

    def setSource(self, source):
        self.source = source

    def setSourceName(self, sourceName):
        self.sourceName = sourceName

    def __repr__(self):
        return "Doc: {\ntitle=\t%s, \nauthor=\t%s, \ndate=\t%s, \nlink=\t%s\n}\n" % (self.title, self.author, self.date, self.link)

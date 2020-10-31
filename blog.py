#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8

class Blog:
    def __init__(self, id, title, link, author, date):
        self.id = id
        self.title = title
        self.link = link
        self.author = author
        self.date = date

    def setDoc(self, doc):
        self.doc = doc

    def getDoc(self):
        return self.doc

    def __repr__(self):
        return "Blog: { \nid:\t%s, \ntitle:\t%s, \nlink:\t%s, \nauthor:\t%s, \ndate:\t%s \n}\n" % (self.id, self.title, self.link, self.author, self.date)


class MeituanBlog(Blog):
    def __init__(self, id, title, link, author, date, abstract):
        super().__init__(id, title, link, author, date)
        self.abstract = abstract

    def getAbstract(self, abstract):
        return self.abstract


class WeChatBlog(Blog):
    def __init__(self, id, title, link, author, date, cover):
        super().__init__(id, title, link, author, date)
        self.cover = cover

    def getCover(self, cover):
        return self.cover

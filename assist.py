#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding=utf-8


url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzU4MDUxOTI5NA==&f=json&offset=70&count=10&is_ok=1&scene=124&uin=MjM2MDI0OTIyMQ%3D%3D&key=8c9049d0f83009fe9a43d1df6767427c5578959492e50b0cd35d96fbf72cdbe4b9acb894613e9b82db2a9165ecc211b2e0e0620cc0f6e6f817c04fa2db6f038d8263c7fb1fb95bff5d50a13318d55f9fe03e030a888cd1cc9f3818b4d8b32b20f9a3f71a11eb79f421e1ab9c31144d06acacac88b115f539ab4d95aaa32cb187&pass_ticket=ZiE%2B1WeCbK57frcKrrCmdUEu%2FkYuTEnfLWpgwwRez97rRDfB8d%2BDLDv8n2vvKisk&wxtoken=&appmsg_token=1078_e7optkDBlfb2GtVnX-sZGDhZOXOJjffQhbjfOA~~&x5=0&f=json"
arr = url.split("&")
for ele in arr:
    if "biz=" in ele:
        print("biz:\t %s" % (ele.split("biz=")[1]))
    if "key=" in ele:
        print("key:\t %s" % (ele.split("key=")[1]))
    if "appmsg_token=" in ele:
        print("appmsg_token:\t %s" % (ele.split("appmsg_token=")[1]))

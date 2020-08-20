#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8

import yaml

class Config:
    def __init__(self, configPath):
        self.loaded = False
        self.configPath = configPath
    def loadConfig(self):
        configFile = "%s/config.yaml" % (self.configPath)
        configYaml= open(configFile, "r")
        self.config = yaml.safe_load(configYaml)

    def getConfig(self):
        if self.loaded is False:
            self.loadConfig()
        return self.config

    def get(self, *tags):
        if len(tags) == 0:
            return ""
        config = self.getConfig()
        value = config
        try:
            for i in range(0, len(tags)):
                value = value[tags[i]]
                if i == len(tags) - 1:
                    return value
        except Exception as e:
            print("config get error.", e)

if __name__ == '__main__':
    config = Config(".")
    print(config.getConfig())
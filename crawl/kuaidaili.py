#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from time import sleep
import requests

class spider():

    def __init__(self, pageIndex):
        self.page       = ""
        self.ip         = []
        self.port       = []
        self.protocol   = []
        self.result     = []
        self.url = "http://www.kuaidaili.com/free/inha/" + str(pageIndex)
        self.getPage()

    def getPage(self):
        try:
            print(self.url)
            page = requests.get(self.url)
            if page.status_code == 200:
                page.encoding = "utf-8"
                self.page = page
        except:
            print("[E]: Can't get kuaidaili resource.")

    def getIp(self):
        try:
            pattern = re.compile("\d+\.\d+\.\d+\.\d+", re.S)
            items = re.findall(pattern, self.page.text)
            self.ip = items
            #print(self.ip)
        except:
            print("[E]: Can't get ip address.")

    def getPort(self):
        try:
            pattern = re.compile("RT\"\>(\d+)", re.S)
            items = re.findall(pattern, self.page.text)
            self.port = items
            #print(self.port)
        except:
            print("[E]: Can't get port address.")

    def getProtocol(self):
        try:
            pattern = re.compile(u"类型\"\>(.*?)\<", re.S)
            items = re.findall(pattern, self.page.text)
            for item in items:
                self.protocol.append(item.lower())
            #print(self.protocol)
        except:
            print("[E]: Can't get protocol address.")

    def getResult(self):
        self.getProtocol()
        self.getIp()
        self.getPort()
        protocol_size   = len(self.protocol)
        ip_size         = len(self.ip)
        port_size       = len(self.port)
        if protocol_size == ip_size == port_size:
            for index in range(ip_size):
                url = self.protocol[index] + "://" + self.ip[index]+ ":" + self.port[index]
                self.result.append(url)
            return self.result

if __name__ == "__main__":
    for index in range(1, 20):
        it = spider(index)
        sleep(3)
        print(it.getResult())
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import requests

class findHost():

    page, proxies, health, = "", "", ""
    http_url = "http://www.baidu.com/s?wd=我的ip"
    ip_msg = {
        "ip": "",
        "port": "",
        "address": "",
        "privacy": "",
        "health": ""
    }

    def __init__(self, proxies):
        findHost.proxies = proxies
        self.retPage()

    def retPage(cls):
        try:
            time0 = time.time()
            r = requests.get(cls.http_url, timeout=3, proxies=cls.proxies)
            if r.status_code == 200:
                time1 = time.time()
                r.encoding = "utf-8"
                cls.page =  r.text
                cls.health = "{0:.3f}".format(time1 - time0)
        except:
            print("[W]:" + cls.proxies["http"] + " not available.")

    def retRealIp(cls):
        try:
            pattern = re.compile("我的ip地址(.*?)。查ip", re.S)
            items = re.findall(pattern, cls.page)
            for item in items:
                pattern = re.compile("\d+\.\d+\.\d+\.\d+", re.S)
                it = re.findall(pattern, item)
                return it
        except:
            print("[E]: Content is not right.")

    def retRealAddress(cls):
        try:
            pattern = re.compile("属于(.*?)。查ip", re.S)
            items = re.findall(pattern, cls.page)
            for item in items:
                return item
        except:
            print("[E]: Content is not right.")

    def retProxyIp(cls):
        try:
            pattern = re.compile("\d+\.\d+\.\d+\.\d+", re.S)
            items = re.findall(pattern, cls.proxies["http"])
            for item in items:
                return item
        except:
            print("[E]: Can't get ip address.")

    def retPort(cls):
        try:
            pattern = re.compile(":\d+", re.S)
            items = re.findall(pattern, cls.proxies["http"])
            for item in items:
                return item[1:]
        except:
            print("[E]: Can't get ip address.")

    def retPrivacy(cls):
        ipArry = cls.retRealIp()
        if ipArry is None:
            return "-"
        elif cls.retProxyIp() == ipArry[0]:
            return "high"
        return "low"

    def retHealth(cls):
        return cls.health

    def retResult(cls):
        ip_msg = cls.ip_msg
        ip_msg["ip"]        = cls.retProxyIp()
        ip_msg["port"]      = cls.retPort()
        ip_msg["address"]   = cls.retRealAddress()
        ip_msg["privacy"]   = cls.retPrivacy()
        ip_msg["health"]    = cls.retHealth()
        return ip_msg

if __name__ == "__main__":
    proxies = {
        "http": "111.23.10.25:80"
    }
    it = findHost(proxies)
    print(it.retResult())



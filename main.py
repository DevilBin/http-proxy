#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from crawl import kuaidaili
from utils import host
from multiprocessing import Process
from time import sleep

def init():
    f = open("ip.txt", "w")
    for page_index in range(1, 20):
        kuaidali_instance = kuaidaili.spider(page_index)
        http_proxies = kuaidali_instance.getResult()
        for http_proxy_index in range(len(http_proxies)):
            p = Process(target=addresProxy, args=(http_proxies[http_proxy_index],))
            p.start()
        sleep(3)


def addresProxy(http_proxy):
    proxies = {
        "http": http_proxy[7:]
    }
    host_instance = host.findHost(proxies)
    proxy_json = host_instance.retResult()
    if proxy_json["address"] != None:
        print(proxy_json)
        f = open("ip.txt", "a")
        f.write(str(proxy_json) + "\n")
        f.close()

if __name__ == "__main__":
    init()
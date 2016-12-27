#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import requests

url = 'https://api.ipify.org/'

def getip_requests(url):
    print "(+) Sending request with plain requests..."
    r = requests.get(url)
    print "(+) IP is: " + r.text.replace("\n", "")


def getip_requesocks(url):
    print "(+) Sending request with requesocks..."
    proxies = {'http': 'socks5://122.192.32.77:7280',
                'https': 'socks5://122.192.32.77:7280'}
    r = requests.get(url, proxies = proxies)
    print "(+) IP is: " + r.text.replace("\n", "")


def main():
    print "Running tests..."
    getip_requests(url)
    getip_requesocks(url)
    os.system("""(echo authenticate ; echo signal newnym; echo quit) | nc localhost 9051""")
    getip_requesocks(url)


if __name__ == "__main__":
    main()
import requests
import re
from pymongo import *
from geoip import geolite2



#proxies = {'http':'socks5://127.0.0.1:9050',
#           'https':'socks5://127.0.0.1:9050'}
proxies = {'http':'socks5://180.153.87.22:10080',
           'https':'socks5://180.153.87.22:10080'}

dict = {'Proxy':'127.0.0.1:1080','Type':'socks5','Country':'US','_id':0}
types = ["socks5","socks4","http","https"]
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

#regex to find the proxy ip and port
reobj = re.compile("(?<=>)(?:\d{1,3}\.){3}\d{1,3}\:\d+(?=</a>)",re.IGNORECASE)
reobj_mimi_ip = re.compile("(?<=<td>)(?:\d{1,3}\.){3}\d{1,3}(?=</td>)")
reobj_mimi_port = re.compile("(?<=<td>)\d+(?=</td>)")


# connect mongodb
client = MongoClient()
db = client.proxyhub
collection = db.proxydb


def get_proxydb():
    offset = 0
    for type in types:
        dict['Type'] = type
        while (1):
            url = "http://proxydb.net/?protocol=" + type + "&offset=" + str(offset)
            print url
            page = requests.get(url, headers=headers, proxies=proxies)
            offset += 50
            if (("No proxies found" in page.text) == True):
                offset = 0
                break
            proxy = reobj.findall(page.text)
            print proxy
            for i in proxy:
                if (collection.count({'Proxy': i}) == 0):
                    dict['Proxy'] = i
                    dict['_id'] = collection.count() + 1
                    dict['Country'] = geolite2.lookup(i.split(':')[0]).country
                    print dict
                    collection.insert_one(dict)

def get_mimiip():
    dict['Type'] = 'http'
    for j in range(681):
        url = "http://www.mimiip.com/gngao/" + str(j)
        page = requests.get(url, headers=headers, proxies=proxies)
        proxy_ip = reobj_mimi_ip.findall(page.text)
        proxy_port = reobj_mimi_port.findall(page.text)
        print url
        for i in range(len(proxy_ip)):
            proxy = proxy_ip[i] + ":" + proxy_port[i]
            if (collection.count({'Proxy': proxy}) == 0):
                dict['Proxy'] = proxy
                dict['_id'] = collection.count() + 1
                if(geolite2.lookup(proxy_ip[i])):
                    dict['Country'] = geolite2.lookup(proxy_ip[i]).country
                else:
                    dict['Country'] = 'NA'
                collection.insert_one(dict)

def main():
    get_proxydb()
    #get_mimiip()

if __name__ == "__main__":
    main()
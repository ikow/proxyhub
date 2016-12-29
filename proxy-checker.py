from pymongo import *
import requests
url = 'https://api.ipify.org/'


# connect mongodb
client = MongoClient('192.168.0.16')
db = client.proxyhub
collection = db.proxydb

def getip_requests(url):
    print "(+) Sending request with plain requests..."
    r = requests.get(url)
    print "(+) IP is: " + r.text.replace("\n", "")

def getip_requesocks(url):
    print "(+) Sending request with requesocks..."
    proxies = {'http': 'socks5://127.0.0.1:9050',
               'https': 'socks5://127.0.0.1:9050'}
    for i in collection.find({'Type': 'https'}):
        proxy = i['Type']+"://"+i['Proxy']
        print "(+) check proxy : "+proxy
        proxies['http'] = proxy
        proxies['https'] = proxy
        try:
            r = requests.get(url, proxies = proxies)
            r.raise_for_status()
            if r != None:
                print "(+) IP is: " + r.text
            else:
                print "(-) Proxy is down!"
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            #print e
            print "(-) Proxy is down!"

def main():
    print "Running tests..."
    getip_requests(url)
    getip_requesocks(url)

if __name__ == "__main__":
    main()

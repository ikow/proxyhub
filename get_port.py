from pymongo import *
client = MongoClient('192.168.0.16')
db = client.proxyhub
collection = db.proxydb

portSet = set()
for i in collection.find():
    portSet.add(i['Proxy'].split(':')[1])
portFile = open("port.txt",'w')
for i in portSet:
    portFile.write(str(i)+'\n')
portFile.close()

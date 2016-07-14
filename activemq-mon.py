#!/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'qiuyongjie'

import string,xml.dom.minidom,sys, urllib2, base64, json, time,socket

ip = "127.0.0.1"
endpoint = socket.gethostname()
step = 60
ts = int(time.time())
tag = ''
keys = ('size','consumerCount','enqueueCount','dequeueCount')

request = urllib2.Request("http://%s:8161/admin/xml/queues.jsp" %ip)
base64string = base64.b64encode('admin:admin')
request.add_header("Authorization", "Basic %s" % base64string)   
result = urllib2.urlopen(request)

xmlStr = string.replace(result.read(),'\t', '')
xmlStr = string.replace(xmlStr,'\n', '')
data = xml.dom.minidom.parseString(xmlStr)
queues = root.getElementsByTagName( "queues" )[0]

p = []

for queue in queues.childNodes:
	for key in keys:
		q = {}
		q["endpoint"]	= endpoint
		q["timestamp"]	= ts
		q["step"]	= step
		q["counterType"]= "GAUGE"
		q["metric"]	= "activemq.%s" % key
		q["tags"]	= "queuename=%s,%s" % (queue.getAttribute('name'),tag)
		q["value"] 	= int(queue.getElementsByTagName("stats")[0].getAttribute(key))
		p.append(q)
#print json.dumps(p, indent=4)

method = "POST"
handler = urllib2.HTTPHandler()
opener = urllib2.build_opener(handler)
url = 'http://127.0.0.1:1988/v1/push'
request = urllib2.Request(url, data=json.dumps(p) )
request.add_header("Content-Type",'application/json')
request.get_method = lambda: method
try:
    connection = opener.open(request)
except urllib2.HTTPError,e:
    connection = e

# check. Substitute with appropriate HTTP code.
if connection.code == 200:
    print connection.read()
else:
    print '{"err":1,"msg":"%s"}' % connection
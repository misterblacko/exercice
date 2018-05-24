from urlparse import urlparse
from threading import Thread
import httplib, sys, datetime
from Queue import Queue

concurrent = 250

def doWork():
	while True:
		url = q.get()
		status, url = getStatus(url)
		doSomethingWithResult(status, url)
		q.task_done()

def getStatus(ourl):
	try:
		url = urlparse(ourl)
		conn = httplib.HTTPSConnection(url.netloc)   
		conn.request("GET", url.path)
		res = conn.getresponse()
		conn.close()
		return res.status, ourl
	except:
		return "error", ourl

def doSomethingWithResult(status, url):
	if status == "error":
		print status, url

print datetime.datetime.now()

urls = ['http://172.16.130.11/']*100000
q = Queue(concurrent * 2)
for i in range(concurrent):
	t = Thread(target=doWork)
	t.daemon = True
	t.start()
try:
	for url in urls:
		q.put(url.strip())
	q.join()
except KeyboardInterrupt:
	sys.exit(1)

print datetime.datetime.now()

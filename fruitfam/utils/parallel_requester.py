import json
import requests
import sys
from threading import Thread
from Queue import Queue

class ParallelRequester(object):
  """
  HTTP requests in parallel. Pass request params in the following format:
  [{
    'url' : 'https://api.clarifai.com/v2/models/123/outputs',
    'method' : 'POST'
    'data' : { 'param1': ['somedata1', 'somedata2'] },
    'headers' : { 'Content-Type': 'application/json' }
  }]
  
  The 'data' and 'headers' keys may be omitted.
  """
  def __init__(self, request_params, concurrent=5):
    self.request_params = request_params
    self.q = Queue(concurrent * 2)
    self.results = {}
    for i in range(concurrent):
      t = Thread(target=self.do_work)
      t.daemon = True
      t.start()
  
  def do_work(self):
    while True:
      request_param = self.q.get()
      resp = self.make_request(request_param)
      request_param = json.loads(request_param)
      url = request_param.get('url', '')
      self.results[url] = resp
      self.q.task_done()
  
  def make_request(self, request_param):
    request_param = json.loads(request_param)
    url = request_param.get('url', '')
    data = request_param.get('data', None)
    if data != None:
      data = json.dumps(data)
    headers = request_param.get('headers', None)
    if request_param['method'] == 'POST':
      resp = requests.post(
        url=url,
        data=data,
        headers=headers
      )
      return resp
    if request_param['method'] == 'GET':
      resp = requests.get(
        url=url,
        data=data,
        headers=headers
      )
      return resp
  
  def run(self):
    try:
      for request_param in self.request_params:
        self.q.put(json.dumps(request_param))
      self.q.join()
    except KeyboardInterrupt:
      sys.exit(1)


# request_params = [
#   {
#   'url' : 'https://www.google.com/',
#   'method' : 'GET',
#   }
# ]*10
# pr = ParallelRequester(request_params, 2)
# pr.run()
# pr.results
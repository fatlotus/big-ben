from gevent import monkey; monkey.patch_all()
from gevent.wsgi import WSGIServer
import gevent
import socket
import urllib2
import random
import json
import time
import logging

# Worker configuration.
TIME_FOR_TRIGGER = 23 # seconds past the last trigger time.
TRIGGER_INTERVAL = 60
TARGET_HOST = 'http://0.0.0.0:3000/'

# State variables.
start_time = time.time()
last_ten_requests = [ ]

def perform_invocation():
  delay = 10
  while True:
    
    # Trigger request to service
    request = urllib2.Request( 
      url = TARGET_HOST,
      data = '', # Ensure that we send a POST request.
      headers = {
        'User-Agent': 'Python REST Cron Service'
      }
    )
    
    # Process the response
    try:
      response = urllib2.urlopen(request, timeout = 15)
      
    except Exception, e:
      # Prepare status code information.
      status_code = e.code if hasattr(e, 'code') else str(e)
      
      # Ensure that we don't hit the service too often.
      delay *= random.uniform(1.5, 1.9)
      delay = min(delay, TRIGGER_INTERVAL)
      
      # Log failures
      last_ten_requests.append( dict(
        type = 'failure',
        failure_time = time.time(),
        status_code = e.code if hasattr(e, 'code') else 'unknown',
        exception = str(e),
        next_request = time.time() + delay
      ) )
      last_ten_requests[10:] = [ ]
      logging.error('POST {0!r} failed with error {1}'.format(TARGET_HOST, status_code))
      
      # Hibernate before making the next request.
      gevent.sleep(delay)
      
    else:
      # Log successes
      logging.info('POST {0!r} succeeded with code {1}'.format(TARGET_HOST, response.getcode()))
      
      # Ensure that our tracking serivce gets this information as well.
      last_ten_requests.append( dict(
        type = 'success',
        success_time = time.time(),
        status_code = response.getcode()
      ) )
      last_ten_requests[10:] = [ ]
      return

def background_thread():
  while True:
    # Trigger a POST request
    perform_invocation()
    
    # Wait until the next trigger period.
    delay = TRIGGER_INTERVAL - (time.time() - TIME_FOR_TRIGGER) % TRIGGER_INTERVAL
    gevent.sleep(delay)

def application(environ, start_response):
  # Display basic job status information.
  start_response('200 Okay', [ ('Content-type', 'application/json')])
  return [ json.dumps(dict(
    requests = last_ten_requests,
    url = TARGET_HOST,
    interval = TRIGGER_INTERVAL,
    uptime = time.time() - start_time,
    start_time = start_time
  )) ]

gevent.spawn(background_thread)

def main():
  from gevent.wsgi import WSGIServer
  
  http_server = WSGIServer(('', 13031), application)
  http_server.serve_forever()
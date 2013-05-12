#### BigBen: Time-Sensitive Networked Services Made Simpler

This is not an attempt to build the be-all end-all application services manager. Rather, this is one part of a much larger networked and evented whole. Ideally, this program would run as a daemon on several hosts, and those hosts would use round-robin DNS to trigger updates to a REST API.

The idea here is to isolate statefulness into the smallest components possible: in this case, we store a counter in memory that ensures that the server isn't losing requests. This means that BigBen depends on tasks being idempotent. If you need finer-grained locking, you will likely need something such as Apache Zookeeper to ensure that multiple requests don't happen at the same time.

##### Usage:

Testing it out:

```
% sudo pip install gunicorn gevent
# ....
% python cron_serve.py # with gevent
...
% gunicorn cron_service:application # with gunicorn
2013-05-12 01:37:06 [64155] [INFO] Starting gunicorn 0.17.4
2013-05-12 01:37:06 [64155] [INFO] Listening at: http://127.0.0.1:8000 (64155)
2013-05-12 01:37:06 [64155] [INFO] Using worker: sync
...
% 
```

You can also install this as a system service within Ubuntu's Upstart process manager. A sample Upstart configuration file is included in `big-ben.conf`.

#####  License

Copyright (c) 2013 Jeremy Archer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
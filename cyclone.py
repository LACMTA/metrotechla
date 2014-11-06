from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from app import app

class MainHandler(RequestHandler):
	def get(self):
		self.write("This message comes from Tornado ^_^")

tr = WSGIContainer(app)

application = Application([
	(r"/tornado", MainHandler),
	(r".*", FallbackHandler, dict(fallback=tr)),
])

if __name__ == "__main__":
	application.listen(8000)
	IOLoop.instance().start()

"""
; supervisor script
; This is where you run individual Tornado instances.
; We run four; one per processor core.
; In development, we ran as many as four per core with no issues.
; If you're looking to minimize cpu load, run fewer processes.
; BTW, Tornado processes are single threaded.
; To take advantage of multiple cores, you'll need multiple processes.
 
[program:tornado-8000]
command=/var/www/envs/metrotechla/bin/python /var/www/envs/metrotechla/cyclone.py
stderr_logfile = /var/log/supervisord/tornado_metrotechla-stderr.log
stdout_logfile = /var/log/supervisord/tornado_metrotechla-stdout.log
"""
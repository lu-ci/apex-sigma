import json
import logging
import threading

import tornado.ioloop
import tornado.web

from config import GitHubWebserverPort as gh_port


# GitHub event handlers and links
event_handlers = {}
channel_links = {}


class Payload():
    def __init__(self, payload):
        self.data = payload

    def repo_name(self):
        self.data['repository']['full_name']

    def sender_name(self):
        self.data['sender']['login']

    def issue(self):
        self.data['issue']

    def pull_request(self):
        self.data['pull_request']

    def small_issue(self):
        'Small issue'

    def small_pull_request(self):
        'Small pull request'

    def action(self):
        self.data['action']


def handle_event(evtype, payload):
    payload = Payload(payload)

    if event_handlers[evtype]:
        event_handlers[evtype].handle(payload)


# Web server stuff
class WebMainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write('Sigma<br>')

    async def post(self):
        event_type = self.request.headers.get('X-GitHub-Event')
        payload = json.loads(self.request.body.decode('utf-8'))
        repo_name = payload['repository']['full_name']

        channels = channel_links[repo_name]
        for channel in channels:
            response = handle_event(event_type, payload)
            if response:
                pass


class WebServer(object):
    def __init__(self, plugin):
        self.bot = plugin.client
        self.log = plugin.log
        self.server = tornado.web.Application([
            (r'/webhook', WebMainHandler)
        ])
        self.server.listen(gh_port)
        logging.getLogger('tornado.access').addHandler(self.log)
        logging.getLogger('tornado.general').addHandler(self.log)
        logging.getLogger('tornado.application').addHandler(self.log)

        self.webthread = threading.Thread(target=self.ioloop)
        self.webthread.daemon = True

    def ioloop(self):
        tornado.ioloop.IOLoop.current().start()

    def run(self):
        self.webthread.start()
        self.log.info('Serving at localhost:{:d}'.format(gh_port))
        return self.webthread

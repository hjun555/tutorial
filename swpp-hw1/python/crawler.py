import requests
import json
import threading
import time
from queue import Queue


# TODO: implement `handle_exception` decorator
from functools import wraps
def handle_exception(originalfunc):
    @wraps(originalfunc)
    def wrapper(*args, **kwargs):
        try:
            return originalfunc(*args, **kwargs)
        except:
            err = "Caught Exception: "
            err += "'"+args[0]+"'"
            print(err)
    return wrapper

class JsonCrawler(threading.Thread):
    crawlers = dict()

    def __init__(self, url, name, period=10., active=False):
        if name in self.crawlers:
            self.crawlers[name]._stop()
        super(JsonCrawler, self).__init__()
        self._stop_event = threading.Event()
        self.setDaemon(True)
        self.queue = Queue()

        # TODO: initialize instance variables
        self.name = name
        self.active = active
        self.url = url
        self.period = period
        self.crawlers[name] = self
        self.start()


    def _stop(self):
        self._stop_event.set()

    def kill(self):
        del self.crawlers[self.name]
        self._stop()

    def run(self):
        if self.active:
            while True:
                self.crawl()
                time.sleep(self.period)
        else:
            self.crawl()

    def __str__(self):
        return self.name

    # TODO: implement `get_by_name` as class method
    @handle_exception
    def get_by_name(self):
        return JsonCrawler.crawlers[self]

    @handle_exception
    def crawl(self):
        # Collect data from website
        response = requests.get(self.url)
        response.raise_for_status()
        data = response.json()
        self.queue.put(data)

    def get_data(self):
        return self.queue.get()

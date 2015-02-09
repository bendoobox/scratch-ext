#!/usr/bin/env python -u
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(name)s - %(message)s")

from array import array
import threading
import socket
import time
import sys
import importlib

PORT = 42001
HOST = '127.0.0.1'
BUFFER_SIZE = 512

print("Connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("Connected!")

# will hold all plugins
handlers = []

# start all plugins
import plugins
from plugins.base import PluginBase
import inspect

noload = ['__init__', 'base']
for plugin in plugins.__all__:
    if plugin in noload:
        continue

    module = importlib.import_module("plugins.%s" % plugin)
    pluginClassName = dir(module)[0]

    pluginClass = getattr(module, pluginClassName)
    if issubclass(pluginClass, PluginBase):
        handler = pluginClass(scratchSock)
        handlers.append(handler)

print 'Found plugins:', handlers

class ScratchListener(threading.Thread):
    socket = None
    plugins = []

    def __init__(self, socket, plugins):
        threading.Thread.__init__(self)
        self.socket = socket
        self.plugins = plugins

    def run(self):
        logging.debug("Started listening")
        while True:
            data = scratchSock.recv(BUFFER_SIZE).strip()
            logging.debug("Received: %s", data)
            for plugin in self.plugins:
                plugin.receive(data)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()



listener = ScratchListener(scratchSock, handlers)
listener.start()

try:
    while True:
        for plugin in handlers:
            plugin.tick()
        time.sleep(1)
except:
    listener.stop()
    # listener.join()
    sys.exit()

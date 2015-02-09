import threading

class PluginBase(object):
    available = False
    socket = None

    def __init__(cls, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        # do setup stuff
        pass

    def tick(self):
        pass

    def receive(self, message):
        pass

    def send(self, message):
        n = len(message)
        a = array('c')
        a.append(chr((n >> 24) & 0xFF))
        a.append(chr((n >> 16) & 0xFF))
        a.append(chr((n >>  8) & 0xFF))
        a.append(chr(n & 0xFF))
        self.socket.send(a.tostring() + message)


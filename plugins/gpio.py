from base import PluginBase
try:
    import RPi.GPIO as pyGPIO
    supported = True
except:
    supported = False
import re
import logging
logger = logging.getLogger(__name__)

class GPIOPlugin(PluginBase):
    available = False
    commands = ['gpio', 'pin']
    pins = {}
    socket = None
    available = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26]

    def __init__(cls, socket):
        logger.debug("Initializing...")
        if supported == False:
            logger.info("This CPU is not supported, ignoring messages")
        else:
            pyGPIO.setmode(pyGPIO.BOARD)
            pyGPIO.setwarnings(False)
            pyGPIO.cleanup()
            self.socket = socket
            logger.info("Initialized succesful")

    def _initpins():
        for pin in self.available:
            self.pins[pin] = {type: self.PUNUSED, state: None}

    def receive(self, message):
        if not supported:
            return False
        # check if we need to process this command
        if any(command in message for command in self.commands):
            logger.debug('acting on: %s' % message)
            message = message.replace('broadcast ', '')
            message = message.replace('"','')
            message = message.lower()
            matches = re.search('(pin|gpio).(?P<no>[0-9]+).(?P<value>on|1|off|0|high|low)', str(message.strip()))
            if matches:
                self.pin(no=matches.groupdict(0)['no'], value=matches.groupdict(0)['value'])
        else:
            logger.debug('ignoring: %s' % message)

    def tick(self):
        if not supported:
            return False
        # check all pin states
        for no, pin in self.pins.items():
            if pin.type != pyGPIO.OUT:
                cmd = 'sensor-update "pin %s" %s' % (no, self.pin(no))
                self.send(cmd)

    def send(cmd):
        n = len(cmd)
        b = (chr((n >> 24) & 0xFF)) + (chr((n >> 16) & 0xFF)) + (chr((n >>  8) & 0xFF)) + (chr(n & 0xFF))
        logger.debug('sending: %s' % cmd)
        return self.socket.send(b + cmd)

    def pin(self, no, value=None):
        no = int(no)
        if value:
            high = ['on','1', 'high']
            low = ['off','0','low']
            if value in high:
                value = True
            if value in low:
                value = False
            logger.debug("Setting Pin %s to %s" % (no, value))
            # if we're sending data, mark this channel as output
            pyGPIO.setup(no, pyGPIO.OUT)
            self.pins[no]['state'] = pyGPIO.OUT
            fooGPIO.output(no, value)
        else:
            self.pins[no]['state'] = pyGPIO.IN
            pyGPIO.setup(no, pyGPIO.IN)
            fooGPIO.input(no)

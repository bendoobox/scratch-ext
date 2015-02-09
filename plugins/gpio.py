from base import PluginBase
import re
import logging

class GPIOPlugin(PluginBase):
    available = False
    commands = ['gpio', 'pin']

    def __init__(cls, socket):
        logging.debug("GPIO initialized")

    def receive(self, message):
        if 'broadcast' in message and any(command in message for command in self.commands):
            message = message.replace('broadcast ', '')
            message = message.replace('"','')
            message = message.lower()
            matches = re.search('(pin|gpio)(?P<no>[0-9]+).(?P<value>on|1|off|0|high|low)', str(message))
            logging.debug(message)
            if matches:
                self.pin(no=matches.groupdict(0)['no'], value=matches.groupdict(0)['value'])


    def tick(self):
        pass

    def pin(self, no, value=None):
        high = ['on','1', 'high']
        low = ['off','0','low']
        if value in high:
            value = True
        if value in low:
            value = False

        logging.debug("Setting Pin %s to %s" % (no, value))

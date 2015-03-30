from base import PluginBase
try:
    import RPi.GPIO as pyGPIO
    supported = True
except:
    supported = False
import re
import logging
logger = logging.getLogger(__name__)

import smbus
import time
bus = None
try:
    bus = smbus.SMBus(1)
except:
    supported = False


class I2CPlugin(PluginBase):
    commands = ['i2c',]
    socket = None
    addresses = []

    def __init__(self, socket):
        logger.debug("Initializing...")
        if supported == False:
            logger.warn("This CPU is not supported, ignoring messages")
        else:
            pyGPIO.setmode(pyGPIO.BOARD)
            pyGPIO.setwarnings(False)
            pyGPIO.cleanup()
            self.socket = socket
            logger.info("Initialized succesful")

    def receive(self, message):
        if not supported:
            return False

        # check if we need to process this command
        if any(command in message for command in self.commands):
            logger.debug('acting on: %s' % message)
            message = message.replace('broadcast ', '')
            message = message.replace('"','')
            message = message.lower()
            matches = re.search('(i2c) ?(?P<device>[0-9]+) (?P<address>[0-9]+).?(?P<value>on|1|off|0|high|low)?', str(message.strip()))
            if matches:
                self.i2c(device=int(matches.groupdict(0)['device']), address=matches.groupdict(0)['address'], value=matches.groupdict(0)['value'])
        else:
            logger.debug('ignoring: %s' % message.strip())

    def tick(self):
        if not supported:
            return False
        # Loop through all device address which were read, and update
        for device, address in self.addresses.items():
            value = self.i2c(device, address)
            cmd = 'sensor-update "i2c %s %s" %s' % (device, address, value)
            self.send(cmd)

    def i2c(self, device, address, value=None):
        foo = int(str(device), 16)
        address = int(address)
        if not supported:
            return None
        if value:
            # write
            try:
                bus.write_byte_data(device, address, value)
                return True
            except:
                return False
        else:
            # read
            value = bus.read_byte_data(foo, address)
            time.sleep(0.5)
            self.devices.append((device, address))
            return value
            


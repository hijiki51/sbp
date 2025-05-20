import bluepy
from typing import Optional
from time import sleep
import logging
class Connector:
    connector: Optional[bluepy.btle.Peripheral]
    logger: logging.Logger
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    def connect(self, mac: str, delegator):
        is_connect = False
        connector = bluepy.btle.Peripheral()
        timeout = 10
        while not is_connect and timeout > 0:
            try:
                connector.connect(mac, bluepy.btle.ADDR_TYPE_RANDOM)
                self.logger.info(f"Connected to {mac}")
                is_connect = True
                connector.withDelegate(delegator)
                self.connector = connector
                return
            except bluepy.btle.BTLEDisconnectError:
                is_connect = False
                self.logger.info(f"Failed to connect: {mac}")
                sleep(1)
                timeout -= 1
                continue
            self.logger.error(f"Failed to connect: timeout: {mac}")
    def reconnect(self, mac: str, delegator):
        try:
            connector = bluepy.btle.Peripheral()
            connector.connect(mac, bluepy.btle.ADDR_TYPE_RANDOM)
            self.logger.info(f"Connected to {mac}")
            connector.withDelegate(delegator)
            self.connector = connector
        except bluepy.btle.BTLEDisconnectError:
            self.logger.info(f"Failed to connect: {mac}")
            return
        return 
    def disconnect(self):
        if self.connector:
            self.connector.disconnect()
        else:
            raise Exception("Not connected")
        return 
    def writeCharacteristic(self, handle, data):
        if self.connector:
            self.connector.writeCharacteristic(handle, data)
        else:
            raise Exception("Not connected")
        return
    def waitForNotifications(self, timeout):
        if self.connector:
            self.connector.waitForNotifications(timeout)
        else:
            raise Exception("Not connected")
        return
import bluepy
from typing import Optional
from time import sleep
class Connector:
    connector: Optional[bluepy.btle.Peripheral]
    def connect(self, mac: str, delegator):
        is_connect = False
        connector = bluepy.btle.Peripheral()
        while not is_connect:
            try:
                connector.connect(mac, bluepy.btle.ADDR_TYPE_RANDOM)
                print("Connected")
                is_connect = True
                connector.withDelegate(delegator)
                self.connector = connector
                return
            except bluepy.btle.BTLEDisconnectError:
                is_connect = False
                print("Failed to connect")
                sleep(1)
                continue
    def reconnect(self, mac: str, delegator):
        try:
            connector = bluepy.btle.Peripheral()
            connector.connect(mac, bluepy.btle.ADDR_TYPE_RANDOM)
            print("Connected")
            connector.withDelegate(delegator)
            self.connector = connector
        except bluepy.btle.BTLEDisconnectError:
            print("Failed to connect")
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
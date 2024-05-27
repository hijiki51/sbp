import bluepy
from typing import Optional

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
                continue
    def reconnect(self, mac: str, delegator):
        self.connector = self.connect(mac, delegator)
        return
    def disconnect(self):
        if self.connector:
            self.connector.disconnect()
        return 
    def writeCharacteristic(self, handle, data):
        if self.connector:
            self.connector.writeCharacteristic(handle, data)
        return
    def waitForNotifications(self, timeout):
        if self.connector:
            self.connector.waitForNotifications(timeout)
        return

def conn(mac: str, delegator): 
    is_connect = False
    connector = bluepy.btle.Peripheral()
    while not is_connect:
        try:
            connector.connect(mac, bluepy.btle.ADDR_TYPE_RANDOM)
            print("Connected")
            is_connect = True
            connector.withDelegate(delegator)
            return connector
        except bluepy.btle.BTLEDisconnectError:
            is_connect = False
            print("Failed to connect")
            continue

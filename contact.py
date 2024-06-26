import bluepy
from typing import Callable
from dataclasses import dataclass
import conn
# https://qiita.com/amax/items/512c35103350d3d33320#%E3%83%AB%E3%83%BC%E3%83%97%E5%87%A6%E7%90%86contact_loop_switchbot%E9%96%A2%E6%95%B0

# The device type is in the service data of SCAN_RSP.

# | Service data |          |                         |
# |--------------|----------|-------------------------|
# | Byte: 0      | Enc type | Bit[7] NC               |
# | Byte: 0      | Dev Type | Bit [6:0] – Device Type |

SBOTCON_HANDLE_NOTIFY = 0x000f
SBOTCON_HANDLE_WRITE = 0x000d

@dataclass
class SWContactStatus:
    status: int
    duration_time: int
    pir: bool
    light: bool
    door: bool

class SWContact(bluepy.btle.DefaultDelegate):
    mac: str
    handler: Callable
    error_handler: Callable
    def __init__(self, mac: str, handler: Callable,error_handler:Callable):
        bluepy.btle.DefaultDelegate.__init__(self)
        self.handler = handler
        self.error_handler = error_handler
        self.mac = mac
    def handleNotification(self, cHandle, data):
        self.handler(self.mac, data)
        pass
    def send_req(self, connector: conn.Connector):
        try:
            connector.writeCharacteristic(SBOTCON_HANDLE_NOTIFY+1, b'\x01\x00') 
            connector.writeCharacteristic(SBOTCON_HANDLE_WRITE, b'\x57\x00\x11') # https://github.com/OpenWonderLabs/SwitchBotAPI-BLE/blob/latest/devicetypes/contactsensor.md#0x11-get-device-status-data
            connector.waitForNotifications(1.0)
            return
        except:
            self.error_handler(self.mac)
            connector.reconnect(self.mac, self)
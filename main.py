import contact
import conn
import os
from time import sleep
from dotenv import load_dotenv
from struct import unpack
from prometheus_client import start_http_server, Enum


load_dotenv()
macs = (os.getenv("WINDOW_SENSORS") or "").split(",")
PROMETHEUS_WINDOW_STAT = Enum("switchbot_window_state","Window open or close",labelnames=("MAC",),states=["open","close","nodata"])

def contact_handler(mac, data):
    parsed = unpack(">BBi??B",data)
    status = contact.SWContactStatus(parsed[0],parsed[2],parsed[3],parsed[4],parsed[5])
    _stat = "close" if status.door == 0 else "open"
    PROMETHEUS_WINDOW_STAT.labels(mac).state(_stat)
    return
def contact_error_handler(mac, data):
    PROMETHEUS_WINDOW_STAT.labels(mac).state("nodata")
    return


if __name__ == "__main__":

    devices = []
    for m in macs:
        delegator = contact.SWContact(m,contact_handler,contact_error_handler)
        connector = conn.Connector()
        connector.connect(m,delegator)
        devices.append({"conn": connector, "delegate": delegator, "mac": m})
    start_http_server(8000)
    try:
        while True:
            for d in devices:
                connector = d["conn"]
                delegator = d["delegate"]
                delegator.send_req(connector)
            sleep(1)
    finally:
        connector.disconnect()
        pass

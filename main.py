import contact
import conn
import os
from time import sleep
from dotenv import load_dotenv
from struct import unpack
from prometheus_client import start_http_server, Enum


load_dotenv()
macs = (os.getenv("WINDOW_SENSORS") or "").split(",")
PROMETHEUS_WINDOW_STAT = Enum("switchbot_window_state","Window open or close",labelnames=("MAC"),states=["open","close"])

def contact_handler(mac, data):
    parsed = unpack(">BBi??B",data)
    status = contact.SWContactStatus(parsed[0],parsed[2],parsed[3],parsed[4],parsed[5])
    _stat = "close" if status.door == 0 else "open"
    PROMETHEUS_WINDOW_STAT.labels(mac).state(_stat)
    return


if __name__ == "__main__":

    devices = []
    for m in macs:
        delegator = contact.SWContact(contact_handler,m)
        connector = conn.conn(m,delegator)
        if connector is None:
            print("Failed to connect")
            exit(1)
        devices.append({"conn": connector, "delegate": delegator, "mac": m})
    start_http_server(8000)
    try:
        while True:
            for d in devices:
                connector = d["conn"]
                delegator = d["delegate"]
                delegator.send_req(connector, conn.conn)
            sleep(3)
    finally:
        connector.disconnect()
        pass

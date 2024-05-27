import contact
import conn
import os
from time import sleep
from dotenv import load_dotenv
from struct import unpack

latest_data = {}

def contact_handler(mac, data):
    parsed = unpack("cci??c",data)
    status = contact.SWContactStatus(parsed[0],parsed[2],parsed[3],parsed[4],parsed[5])
    latest_data[mac] = status
    pass    


if __name__ == "__main__":
    load_dotenv()
    macs = (os.getenv("WINDOW_SENSORS") or "").split(",")
    devices = []
    for m in macs:
        delegator = contact.SWContact(contact_handler,m)
        connector = conn.conn(m,delegator)
        if connector is None:
            print("Failed to connect")
            exit(1)
        devices.append({"conn": connector, "delegate": delegator, "mac": m})

    try:
        while True:
            for d in devices:
                connector = d["conn"]
                delegator = d["delegate"]
                delegator.send_req(connector, conn.conn)
            sleep(3)
            print(latest_data)
    finally:
        connector.disconnect()
        pass
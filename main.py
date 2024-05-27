import contact
import conn
import os
from time import sleep
from dotenv import load_dotenv
from struct import unpack


def contact_handler(data):
    parsed = unpack("cci??c",data)
    status = contact.SWContactStatus(parsed[0],parsed[2],parsed[3],parsed[4],parsed[5])
    print(status)
    pass    


if __name__ == "__main__":
    load_dotenv()
    mac = os.getenv("WINDOW_SENSOR1") or ""
    print(mac)
    delegator = contact.SWContact(contact_handler)
    connector = conn.conn(mac,delegator)
    if connector is None:
        print("Failed to connect")
        exit(1)

    try:
        while True:
            delegator.send_req(connector, conn.conn, mac)
            sleep(3)
    finally:
        connector.disconnect()
        pass
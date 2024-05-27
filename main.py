import contact
import conn
import os
from time import sleep
from dotenv import load_dotenv


def contact_handler(data):
    print(data)
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
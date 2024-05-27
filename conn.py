import bluepy

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

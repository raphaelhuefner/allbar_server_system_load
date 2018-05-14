import threading

payload_lock = threading.RLock()
payload = b'{"ttl":0,"indicators":["x"],"menu":[]}'

def get():
    global payload_lock, payload
    with payload_lock:
        return payload

def set(new_payload):
    global payload_lock, payload
    with payload_lock:
        payload = new_payload

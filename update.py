import json
import threading

import psutil

import minidiagram
import payload

timer = None
cpu_percent = [0] * 80

def record_data():
    global cpu_percent
    cpu_percent.append(psutil.cpu_percent())
    cpu_percent.pop(0)

def get_config():
    global cpu_percent
    diagram = minidiagram.MiniDiagram(bgcolor=(0.6,0.6,0.6))
    diagram.add_data(cpu_percent, (1,0,0))
    return {
        "ttl": 1,
        "indicators": [
            {
                "icon": diagram.get_data_uri(),
                "title": "{cpu: =5.1f}%".format(cpu=cpu_percent[-1])
            }
        ],
        "menu": [
            {
                "title": "Throttle!",
                "active": False,
                "open": "https://google.com"
            }
        ],
    }

def update():
    global timer
    record_data()
    payload.set(json.dumps(get_config()).encode())
    timer = threading.Timer(1.0, update)
    timer.start()

def run():
    global timer
    timer = threading.Timer(1.0, update)
    timer.start()

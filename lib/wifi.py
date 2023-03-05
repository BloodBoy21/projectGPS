import machine
import network
from time import sleep
import urequests
import readEnv as env
url = env.get_env('server_url')
token = None

def board_id():
    id = machine.unique_id()
    return "".join("{:02X}".format(b) for b in id)

def connect(ssid,password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def send_data(data):
    if token is None:
        print('No token')
        return
    urequests.post(f'{url}/location/{token}', json=data)

def login():
    global token
    id = board_id()
    print(f'Board id: {id}')
    res = urequests.get(f'{url}/login/{id}')
    data = res.json()
    print(data)
    token = data['token']
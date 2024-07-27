import time
import ubluetooth
from umqtt.simple import MQTTClient
import network

wifi_ssid = "ENTER SSID"
wifi_pwd = "ENTER PWD"
wifi_mac = ""
broker_adr = "test.mosquitto.org"
data_topic = "asdasdasd"
command_topic = "dsadsadsa"
port = "1883"
client_id = "ESP32 BLE Scanner"
cmd = ""
username = None
pwd = None
stopped = False

devices = {}

client = MQTTClient(client_id, broker_adr, port=port)
bt = ubluetooth.BLE()
bt.active(True)

def connect_wifi(ssid, pwd):
    global wifi_mac
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(wifi_ssid, wifi_pwd)
    while not wifi.isconnected():
        print('...')
        time.sleep(1)
    print('\nConnected to WiFi')
    wifi_mac = wifi.config('mac').hex().upper()
    print('Network config:', wifi.ifconfig())


def handle_scan(event, data):
    if event == 5:
        addr_type, addr, adv_type, rssi, adv_data = data
        address = bytes(addr).hex().upper()
        raw = "0x" + str(bytes(adv_data).hex().upper())
        main_topic = data_topic + "/" + wifi_mac + "/" + address
        if raw not in devices.values():
            devices[address] = {"raw_data": raw}
            print(address)
            print(raw)
            print("\n")
            client.publish(main_topic, raw)
        elif raw in devices.values():
            if address in devices.keys():
                devices[devices] = {"raw_data": raw}
    if event == 6:
        print("scan stopped")


def stop_scan():
    global client
    global broker_adr
    global data_topic
    global cmd
    bt.gap_scan(None)
    client.publish(command_topic, "waiting command...")
    client.subscribe(command_topic)
    client.wait_msg()
        
        
def on_message(topic,msg):
    global cmd
    global stopped
    cmd = msg.decode()
    topic = topic.decode()
    print(cmd)
    print(topic)
    if cmd == "stop" and topic == command_topic:
        print("scanning stop")
        stopped = True
        stop_scan()
    if stopped == False and "mqtt_set" or "wifi_set" in cmd:
        print("must be stopped first")
        client.publish(command_topic, "must be stopped first!")
        scan()
    if stopped == True and "mqtt_set" or "wifi_set" in cmd:
        handle_cmd()
        
def handle_cmd():
    global cmd
    global client
    global wifi_ssid
    global wifi_pwd
    global broker_adr
    global data_topic
    if "mqtt_set" in cmd:
        cmd = cmd.split("/")
        broker_adr = cmd[1]
        data_topic = cmd[2]
        client.publish(command_topic, "mqtt set!")
        client = MQTTClient(client_id, broker_adr, port=port)
        print("mqtt set!")
        client.connect()
        scan()
    if "wifi_set" in cmd:
        cmd = cmd.split("/")
        wifi_ssid = cmd[1]
        wifi_pwd = cmd[2]
        client_publish(command_topic, "wifi set!")
        print("wifi set!")
        connect_wifi(wifi_ssid, wifi_pwd)
        scan()
    
        

def scan():
    client.set_callback(on_message)
    bt.irq(handle_scan)
    print("scan start")
    bt.gap_scan()
    client.subscribe(command_topic)
    client.wait_msg()
    
connect_wifi(wifi_ssid, wifi_pwd)
client.connect()
scan()
    







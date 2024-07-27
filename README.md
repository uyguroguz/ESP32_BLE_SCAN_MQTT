# ESP32_BLE_SCAN_MQTT
This code starts a BLE scan and WIFI connection on ESP32. Publishes BLE raw data on specified MQTT topic. Also listens to another MQTT topic for wifi or mqtt setting changes.

## Requirements:

### For main.py:
Python 3.x

micropython (as the interpreter)

umqtt.simple

any esp32 board with BLE and WIFI support

### For listening.py:
Python 3.x

paho.mqtt.client


You can install the required libraries using pip:

pip install umqtt.simple paho-mqtt

## Files:

"main.py"
Scans for Bluetooth LE devices using the esp32 onboard BLE chip.
Connects to the specified WIFI network.
Connects to the specified MQTT server.
Publishes the raw BLE data to the specified MQTT topic.
Simultaneously listens to another pre-determined MQTT topic for mqtt_set and wifi_set commands.

"listening.py"
Subscribes to a given topic at the MQTT broker.
Stores the received information in a mqtt_data.txt file.

### Configuration for "main.py":
broker_adr: The default address of the MQTT broker.

port: The port number of the MQTT broker.

data_topic: The MQTT topic to publish the raw BLE data.

command_topic: The MQTT topic for WIFI and MQTT setting change commands.

client_id: The device id on the specified MQTT broker connection.

wifi_ssid: The default SSID of WIFI network.

wifi_pwd: The default password for the given SSID network.


### Configuration for "listening.py":
broker_address: The address of the MQTT broker.

port: The port number of the MQTT broker.

topic: The MQTT topic to subscribe to.

client_id: The device id on the specified MQTT broker connection.

## Usage:
Run the listening.py script to start listening to the MQTT topic and store the received information.

"python listening.py"

Load the "main.py" to ESP32 board through micropython and in boot it will start scanning itself.

In my case i used ESP32-C3-MINI-1 and it has RGB led onboard. And color codes for processes exist.
RED means wifi connection is not present. WHITE means wifi connection established. BLUE means bluetooth is scanning for device. GREEN means sending information to MQTT.

To change values from another MQTT server. Set the "command_topic".

For wifi changing use: "wifi_set/ENTER SSID HERE/ENTER PASSWORD HERE"

For mqtt changing use: "mqtt_set/ENTER MQTT BROKER ADDRESS/ENTER TOPIC FOR DATA"



## Note:
My board had RGB led and the code has RGB led utilization. I haven't tried with another board that doesn't have RGB led so it might give error about that part.

I suggest using Thonny as IDE since it is very easy and straightforward.

## License:
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing:
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.








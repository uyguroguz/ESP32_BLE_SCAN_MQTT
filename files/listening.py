import paho.mqtt.client as mqtt
import os

broker_address = "test.mosquitto.org"
port = 1883
client_id = "Bluetooth LE Scan Listening"
topic = "asdasdasd"
main_topic = topic + "/#"

mqtt_client =mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)

print(f"connecting to broker address '{broker_address}' with client id '{client_id}'")
mqtt_client.connect(broker_address)


print(f"starting to listen '{main_topic}'")
mqtt_client.subscribe(main_topic)

print("waiting on message")

TEXT_FILE = "mqtt_data.txt"

if os.path.exists(TEXT_FILE):
    os.remove(TEXT_FILE)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message: {message} on topic {msg.topic}")
    
    # Write received message to text file
    with open(TEXT_FILE, "a") as file:
        if message == "\n":
            file.write("\n")
        else:
            file.write(f"{msg.topic.lstrip(topic)}: {message} \n")
        
try:        
    mqtt_client.on_message = on_message

    mqtt_client.loop_forever()
    
except KeyboardInterrupt:
    print("program terminated")
    mqtt_client.disconnect()


from typing import Literal
from paho.mqtt import client as mqtt_client
from .constants import main_topic, realtime_weight_response_subtopic
from .mqtt_info import Mqtt_Info
from app.mqtt_client.constants import device_mac_address_response
import time

broker = 'broker.emqx.io'
port = 1883
msg_received = False
mqtt_info = Mqtt_Info()
response = (False, "")


def connect_mqtt():
    def on_connect(client, userdata, connect_flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", reason_code)
            
    def on_subscribe(client, userdata, mid, reason_code_list, properties):
        print(f"Subscribed to topic")
        
    def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
        print("Unsubscribed to topic")
        
    def on_message(client, userdata, msg):
        global mqtt_info
        global msg_received
        print(f"Received {msg.payload.decode()} from {msg.topic} topic")
        
        if msg.topic == f"{main_topic}/{realtime_weight_response_subtopic}":
            device_realtime_weight = float(msg.payload.decode())
            mqtt_info.weight = 0 if device_realtime_weight < 0 else device_realtime_weight
            unsubscribe(client, msg.topic)
            
        elif msg.topic == f"{main_topic}/{device_mac_address_response}":
            mqtt_info.mac_address = msg.payload.decode()
            unsubscribe(client, msg.topic)
            
        msg_received = True

    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client.Client, topic: str):
    client.subscribe(topic)
    
def unsubscribe(client: mqtt_client.Client, topic: str):
    client.unsubscribe(topic)

def run(topic: str):
    global msg_received
    global mqtt_info
    global response
    msg_received = False
    client = connect_mqtt()
    client.loop_start()
    subscribe(client, topic)
    subscribe_stop_counter = 0
    subscribe_stop_counter_max = 120 if topic == f"{main_topic}/{device_mac_address_response}" else 120
    while (subscribe_stop_counter <= subscribe_stop_counter_max) and (msg_received == False):
        time.sleep(0.5)
        subscribe_stop_counter += 1
    client.loop_stop()
    if (topic == f"{main_topic}/{device_mac_address_response}"):
        print(f"{topic} ====> {mqtt_info.get_mac_address()}/{msg_received}")
        response = (msg_received, mqtt_info.get_mac_address())
    elif topic == f"{main_topic}/{realtime_weight_response_subtopic}":
        print(f"{topic} ====> {mqtt_info.get_weight()}/{msg_received}")
        response = (msg_received, mqtt_info.get_weight())
    return response
    
if __name__ == '__main__':
    run()

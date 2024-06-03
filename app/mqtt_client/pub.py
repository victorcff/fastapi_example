from paho.mqtt import client as mqtt_client
from .constants import main_topic

broker = 'broker.emqx.io'
port = 1883

def connect_mqtt():
    def on_connect(client, userdata, connect_flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", reason_code)

    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client: mqtt_client, msg: str, topic: str):
    full_topic = f"{main_topic}/{topic}"
    result = client.publish(topic=full_topic, payload=msg, qos=1)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{full_topic}`")
    else:
        print(f"Failed to send message to topic {full_topic}")

def run(msg: str, topic: str):
    client = connect_mqtt()
    client.loop_start()
    publish(client, msg, topic)
    client.loop_stop()

if __name__ == '__main__':
    run()
